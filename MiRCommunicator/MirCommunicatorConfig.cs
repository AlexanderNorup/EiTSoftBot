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

        [Required]
        public string MirApiEndpoint { get; set; } = "http://mir.com/api/v2.0.0";

        [Required]
        public string MirApiUsername { get; set; } = "admin";

        [Required]
        public string MirApipassword { get; set; } = "admin";

        [Required]
        public string MirSessionId { get; set; } = string.Empty;
    }
}
