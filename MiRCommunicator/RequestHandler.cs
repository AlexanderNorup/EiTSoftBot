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
using System.Text;

namespace MiRCommunicator
{
    internal class RequestHandler(IMqttClient mqttClient, MirCommunicatorConfig config)
    {
        private MiRRestClient _mirClient = new MiRRestClient(config.MirApiEndpoint, config.MirApiUsername, config.MirApipassword);
        private SemaphoreSlim _positionSemaphore = new SemaphoreSlim(1, 1);
        private ConcurrentDictionary<string, RestPosition> _positionCache = new ConcurrentDictionary<string, RestPosition>();

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
                        Source = "MiRCommunicator"
                    });
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
            var response = new GetAllMissionsResponse();
            var allMissions = await _mirClient.GetMissionsForSessionAsync(config.MirSessionId).ConfigureAwait(false);
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
                        if (positionParam is null)
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("Position parameter missing in move action");
                            Console.ResetColor();
                            continue;
                        }
                        var position = await GetPositionAsync(positionParam.Value);
                        responseWaypoints.Add(new Waypoint(action.Guid, position.Name, position.PosX, position.PosY, position.Orientation, currentSpeed));
                    }
                    else if (action.ActionType == "planner_settings")
                    {
                        var speedParameter = action.Parameters.FirstOrDefault(x => x.Id == "desired_speed");
                        if (speedParameter is not null
                            && double.TryParse(speedParameter.Value, out var newCurrentSpeed))
                        {
                            currentSpeed = newCurrentSpeed;
                        }
                    }
                }

                response.Missions.Add(new Mission(mission.Guid, mission.Name, responseWaypoints));
            }

            await SendResponse(response);
        }


        private async Task SendResponse(BaseMessage response)
        {
            var responseJson = RequestSerializer.Serialize(response);
            var responseMessage = new MqttApplicationMessageBuilder()
                .WithTopic(config.MqttResponseTopic)
                .WithPayload(Encoding.UTF8.GetBytes(responseJson))
                .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.ExactlyOnce)
                .Build();

            Console.WriteLine($"Sending response of type: {response.GetType().Name}");
            await mqttClient.PublishAsync(responseMessage);
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

                var newPos = await _mirClient.GetPosition(positionId).ConfigureAwait(false);
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
