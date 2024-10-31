using MQTTnet;
using MQTTnet.Client;
using System.Text.Json;

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
            
            await _client.SubscribeAsync("PLACEHOLDER");

            _client.ApplicationMessageReceivedAsync += (e) =>
            {
                //_missions = e.ApplicationMessage.PayloadSegment
                // TODO: Pack and parse message

                var message = "hello world";
                OnMessageRecieved.Invoke(message);
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
                .WithTopic("PLACEHOLDER")
                .WithPayload("gib missions pls")
                .Build());
            }
        
        public event Action<string> OnMessageRecieved;
        public void Dispose()
        {
            _client?.Dispose();
        }
    }
}
