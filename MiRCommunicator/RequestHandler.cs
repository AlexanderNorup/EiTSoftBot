using EiTSoftBot.Dto;
using EiTSoftBot.Dto.Entities;
using EiTSoftBot.Dto.Requests;
using EiTSoftBot.Dto.Responses;
using MiR200RestClient;
using MiR200RestClient.Entities;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Protocol;
using System.Collections.Concurrent;
using System.Globalization;
using System.Text;

namespace MiRCommunicator
{
    internal class RequestHandler
    {
        private IMqttClient _mqttClient;
        private MirCommunicatorConfig _config;
        private MiRRestClient _mirClient;
        private MirMonitor _monitor;
        private SemaphoreSlim _positionSemaphore = new SemaphoreSlim(1, 1);
        private ConcurrentDictionary<string, RestPosition> _positionCache = new ConcurrentDictionary<string, RestPosition>();

        internal RequestHandler(IMqttClient mqttClient, MirCommunicatorConfig config)
        {
            _mqttClient = mqttClient ?? throw new ArgumentNullException(nameof(mqttClient));
            _config = config ?? throw new ArgumentNullException(nameof(config));
            _mirClient = new MiRRestClient(config.MirApiEndpoint, config.MirApiToken);
            _monitor = new MirMonitor(_mirClient);
        }

        public async Task HandleRequestAsync(BaseMessage baseMessage)
        {
            switch (baseMessage)
            {
                case GetAllMissionsRequest getAllMissionsRequest:
                    await HandleGetAllMissionsRequest(getAllMissionsRequest);
                    break;
                case PingRequest pingRequest:
                    await SendResponse(new PingResponse()
                    {
                        PingId = pingRequest.PingId,
                        MiRConnected = _monitor.MirConnected,
                        MirStatus = _monitor.MirStatus,
                        Source = "MiRCommunicator"
                    });
                    break;
                case SetMissionRequest setMissionRequest:
                    await HandleSetMissionRequest(setMissionRequest);
                    break;
                case SetMirStatusRequest statusRequest:
                    var newStateId = statusRequest.Ready ? MirState.Ready : MirState.Paused;
                    await _mirClient.SetStatusAsync(new RestStatusSet() { StateId = newStateId });
                    await _monitor.RefreshState();
                    break;
                default:
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"Unknown reques type: {baseMessage.GetType().Name}");
                    Console.ResetColor();
                    break;
            }
        }

        private async Task HandleGetAllMissionsRequest(GetAllMissionsRequest getAllMissionsRequest)
        {
            if (!_monitor.MirConnected)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("MiR is not connected, cannot get missions");
                Console.ResetColor();
                return;
            }
            var response = new GetAllMissionsResponse();
            var allMissions = await _mirClient.GetMissionsForSessionAsync(_config.MirSessionId).ConfigureAwait(false);
            foreach (var mission in allMissions)
            {
                List<Waypoint> responseWaypoints = new();
                var actions = await _mirClient.GetActionsForMissionAsync(mission.Guid).ConfigureAwait(false);
                double? currentSpeed = null;
                foreach (var action in actions.OrderBy(x => x.Priority))
                {
                    if (action.ActionType == "move")
                    {
                        var positionParam = action.Parameters.FirstOrDefault(x => x.Id == "position");
                        if (positionParam is null
                            || positionParam.Value is not string)
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("Position parameter missing in move action");
                            Console.ResetColor();
                            continue;
                        }

                        var position = await GetPositionAsync((string)positionParam.Value);
                        responseWaypoints.Add(new Waypoint(position.Guid, position.Name, position.PosX, position.PosY, position.Orientation, currentSpeed));
                    }
                    else if (action.ActionType == "planner_settings")
                    {
                        var speedParameter = action.Parameters.FirstOrDefault(x => x.Id == "desired_speed");
                        if (speedParameter is not null
                            && speedParameter.Value is double newCurrentSpeed)
                        {
                            currentSpeed = newCurrentSpeed;
                        }
                    }
                }

                response.Missions.Add(new Mission(mission.Guid, mission.Name, responseWaypoints));
            }

            await SendResponse(response);
        }

        private async Task HandleSetMissionRequest(SetMissionRequest setMissionRequest)
        {
            try
            {
                if (!_monitor.MirConnected)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("MiR is not connected, cannot set mission");
                    Console.ResetColor();
                    return;
                }

                Console.WriteLine("Starting new Mission Set Request. Pausing MiR");
                await _mirClient.SetStatusAsync(new RestStatusSet()
                {
                    StateId = MirState.Paused
                }).ConfigureAwait(false);
                _ = _monitor.RefreshState();

                var mission = setMissionRequest.Mission;
                var actions = await _mirClient.GetActionsForMissionAsync(mission.Id).ConfigureAwait(false);
                Console.WriteLine("Found mission on MiR. Deleting old actions");
                foreach (var action in actions)
                {
                    // If this goes well, this can be done concurrently
                    await _mirClient.DeleteActionFromMission(mission.Id, action.Guid).ConfigureAwait(false);
                }
                Console.WriteLine("Writing new actions");

                int i = 0;
                foreach (var waypoint in mission.Waypoints)
                {
                    if (waypoint.Speed is { } speed)
                    {
                        var speedAction = MirActionFactory.GetSpeedActionParameter(i++, speed);
                        await _mirClient.AddActionToMissionAsync(mission.Id, speedAction).ConfigureAwait(false);
                    }

                    var moveAction = MirActionFactory.GetMoveActionParameter(i++, waypoint.Id);
                    await _mirClient.AddActionToMissionAsync(mission.Id, moveAction).ConfigureAwait(false);
                }

                Console.WriteLine($"Wrote {i} actions to MiR");

                if (setMissionRequest.MaxAcceleration is { } maxAccel)
                {
                    Console.WriteLine($"Setting max acceleration to {maxAccel}");
                    await _mirClient.SetAccelerationAsync(new RestSettingSet()
                    {
                        Value = maxAccel.ToString(CultureInfo.InvariantCulture)
                    }).ConfigureAwait(false);
                }

                Console.WriteLine("Clearing Mission Queue");
                await _mirClient.ClearMissionQueueAsync().ConfigureAwait(false);

                Console.WriteLine("Adding our Mission to the mission queue");
                await _mirClient.AddMissionToQueueAsync(new RestMissionQueueEntry()
                {
                    MissionId = mission.Id,
                }).ConfigureAwait(false);

                await SendResponse(new SetMissionResponse()
                {
                    Success = true
                });
            }
            catch (Exception e)
            {
                await SendResponse(new SetMissionResponse()
                {
                    Success = false
                });
                throw;
            }
        }
        private async Task SendResponse(BaseMessage response)
        {
            var responseJson = RequestSerializer.Serialize(response);
            var responseMessage = new MqttApplicationMessageBuilder()
                .WithTopic(_config.MqttResponseTopic)
                .WithPayload(Encoding.UTF8.GetBytes(responseJson))
                .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.ExactlyOnce)
                .Build();

            Console.WriteLine($"Sending response of type: {response.GetType().Name}");
            await _mqttClient.PublishAsync(responseMessage);
        }

        private async Task<RestPosition> GetPositionAsync(string positionId)
        {
            if (_positionCache.TryGetValue(positionId, out var position))
            {
                return position;
            }

            await _positionSemaphore.WaitAsync().ConfigureAwait(false);
            try
            {
                if (_positionCache.TryGetValue(positionId, out position))
                {
                    return position;
                }

                var newPos = await _mirClient.GetPositionAsync(positionId).ConfigureAwait(false);
                _positionCache.TryAdd(positionId, newPos);
                return newPos;
            }
            finally
            {
                _positionSemaphore.Release();
            }
        }
    }
}
