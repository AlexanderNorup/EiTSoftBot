using System.Text;
using MQTTnet;
using MQTTnet.Client;
using System.Text.Json;
using EiTSoftBot.Dto;
using EiTSoftBot.Dto.Requests;
using EiTSoftBot.Dto.Responses;
using EiTSoftBot.Dto.Entities;

namespace EiTSoftBot.Services
{
    public class SimulatorClient(MqttClientOptions _mqttClientOptions,
        IConfiguration _config, ILogger<SimulatorClient> logger) : IDisposable
    {
        private IMqttClient _client;
        public async Task OpenConnectionAsync()
        {
            if (_client != null && _client.IsConnected) return;
            _client = new MqttFactory().CreateMqttClient();
            await _client.ConnectAsync(_mqttClientOptions);

            await _client.SubscribeAsync(_config["MqttConfig:MqttResponseTopic"]);

            _client.ApplicationMessageReceivedAsync += (e) =>
            {
                try
                {
                    var rawMessage = Encoding.UTF8.GetString(e.ApplicationMessage.PayloadSegment);
                    var message = RequestSerializer.Deserialize(rawMessage);
                    OnMessageRecieved.Invoke(message);
                }
                catch (Exception ex)
                {
                    logger.LogError(ex, "Failed to deserialize message");
                }
                return Task.CompletedTask;
            };
        }

        public async Task StartSimulationAsync(Mission mission, List<GazeboBox> boxes)
        {
            var simulationStartRequest = new SimulationStartRequest()
            {
                Mission = mission,
                Boxes = boxes
            };
            await OpenConnectionAsync();
            await _client.PublishAsync(new MqttApplicationMessageBuilder()
                .WithTopic(_config["MqttConfig:MqttTopic"])
                .WithPayload(RequestSerializer.Serialize(simulationStartRequest))
                .Build());
        }

        public async Task RequestMissionsAsync()
        {
            await OpenConnectionAsync();
            await _client.PublishAsync(new MqttApplicationMessageBuilder()
                .WithTopic(_config["MqttConfig:MqttRequestTopic"])
                .WithPayload(RequestSerializer.Serialize(new GetAllMissionsRequest()))
                .Build());
        }

        public async Task SetMissionAsync(Mission adjustedMission, int? newMaxAccel)
        {
            var setMissionRequest = new SetMissionRequest()
            {
                Mission = adjustedMission,
                MaxAcceleration = newMaxAccel,
            };
            await OpenConnectionAsync();
            await _client.PublishAsync(new MqttApplicationMessageBuilder()
                .WithTopic(_config["MqttConfig:MqttRequestTopic"])
                .WithPayload(RequestSerializer.Serialize(setMissionRequest))
                .Build());
        }

        public async Task SetMirStatusAsync(bool ready)
        {
            await OpenConnectionAsync();
            await _client.PublishAsync(new MqttApplicationMessageBuilder()
                .WithTopic(_config["MqttConfig:MqttRequestTopic"])
                .WithPayload(RequestSerializer.Serialize(new SetMirStatusRequest() { Ready = ready }))
                .Build());
        }

        public async Task<ConnectionStatus> GetOtherClientConnectionStatus(TimeSpan timeout)
        {
            var waitingFor = Guid.NewGuid().ToString();
            bool mirConnectorAlive = false;
            bool mirAlive = false;
            int? mirStatus = null;
            bool simAlive = false;
            Action<BaseMessage> listener = (e) =>
            {
                if (e is PingResponse ping
                    && ping.PingId == waitingFor)
                {
                    if (ping.Source == "MiRCommunicator")
                    {
                        mirConnectorAlive = true;
                        mirAlive = ping.MiRConnected == true;
                        mirStatus = ping.MirStatus;
                    }
                    else if (ping.Source == "Simulation")
                    {
                        simAlive = true;
                    }

                    logger.LogInformation("Got response from {Source}", ping.Source);
                }
            };
            OnMessageRecieved += listener;
            try
            {
                logger.LogInformation("Sending ping signal with PingId: {PingId}", waitingFor);
                var pingPayload = RequestSerializer.Serialize(new PingRequest() { PingId = waitingFor });
                await OpenConnectionAsync();
                var pingRequests = new Task[]
                {
                    _client.PublishAsync(new MqttApplicationMessageBuilder()
                        .WithTopic(_config["MqttConfig:MqttRequestTopic"]) // MirCommunicators topic
                        .WithPayload(pingPayload)
                        .Build()),
                    _client.PublishAsync(new MqttApplicationMessageBuilder()
                        .WithTopic(_config["MqttConfig:MqttTopic"]) // Simulators topic
                        .WithPayload(pingPayload)
                        .Build())
                };
                await Task.WhenAll(pingRequests).ConfigureAwait(false);
                using var cts = new CancellationTokenSource();
                cts.CancelAfter(timeout);
                while (!cts.IsCancellationRequested)
                {
                    if (mirConnectorAlive && simAlive)
                    {
                        logger.LogDebug("Both Mir and Sim alive!");
                        return new ConnectionStatus(true, mirAlive, mirStatus, true);
                    }
                    await Task.Delay(100).ConfigureAwait(false);
                }
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Failed to get other clients");
            }
            finally
            {
                OnMessageRecieved -= listener;
            }

            logger.LogDebug("MiR Connector Alive: {MirConnectorAlive}, MiR Alive: {MirAlive} , Sim Alive: {SimAlive}", mirConnectorAlive, mirAlive, simAlive);
            return new ConnectionStatus(mirConnectorAlive, mirAlive, mirStatus, simAlive);
        }

        internal void SimulateRecieveMessage(BaseMessage msg)
        {
            OnMessageRecieved.Invoke(msg);
        }

        public event Action<BaseMessage> OnMessageRecieved;
        public void Dispose()
        {
            _client?.Dispose();
        }
    }

    public record ConnectionStatus(bool mirConnectorConnected,
        bool mirConnected,
        int? mirStatus,
        bool simulationConnected);
}
