using System.ComponentModel.DataAnnotations;

namespace MiRCommunicator
{
    public class MirCommunicatorConfig
    {
        [Required]
        public string MqttUsername { get; set; } = string.Empty;

        [Required]
        public string MqttPassword { get; set; } = string.Empty;

        [Required]
        public string MqttRequestTopic { get; set; } = string.Empty;

        [Required]
        public string MqttResponseTopic { get; set; } = string.Empty;

        [Required]
        public string MqttHost { get; set; } = string.Empty;

        public string? MirApiEndpoint { get; set; }
    }
}
