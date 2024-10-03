using MQTTnet;
using MQTTnet.Client;
using System.Text.Json;

namespace EiTSoftBot.Services
{
    public class SimulatorClient(MqttClientOptions _mqttClientOptions,
        IConfiguration _config)
    {
        public async Task SendGazeboBoxesAsync(List<GazeboBox> boxes)
        {
            using var mqttClient = new MqttFactory().CreateMqttClient();
            await mqttClient.ConnectAsync(_mqttClientOptions);
            await mqttClient.PublishAsync(new MqttApplicationMessageBuilder()
                .WithTopic(_config["MqttConfig:MqttTopic"])
                .WithPayload(JsonSerializer.Serialize(boxes))
                .Build());
        }
    }
}
