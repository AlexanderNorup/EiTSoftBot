using System.Text;
using MQTTnet;
using MQTTnet.Client;
using System.Text.Json;
using EiTSoftBot.Dto;
using EiTSoftBot.Dto.Requests;

namespace EiTSoftBot.Services
{
    public class SimulatorClient(MqttClientOptions _mqttClientOptions,
        IConfiguration _config): IDisposable
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
                catch (Exception exception)
                {
                }
                return Task.CompletedTask;
            };
        }
        
        public async Task SendGazeboBoxesAsync(List<GazeboBox> boxes)
        {
            await OpenConnectionAsync();
            await _client.PublishAsync(new MqttApplicationMessageBuilder()
                .WithTopic(_config["MqttConfig:MqttTopic"])
                .WithPayload(JsonSerializer.Serialize(boxes))
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
        
        public event Action<BaseMessage> OnMessageRecieved;
        public void Dispose()
        {
            _client?.Dispose();
        }
    }
}
