using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestStatus
    {
        [JsonProperty("position", NullValueHandling = NullValueHandling.Ignore)]
        public StatusPosition Position { get; set; }

        [JsonProperty("velocity", NullValueHandling = NullValueHandling.Ignore)]
        public StatusVelocity Velocity { get; set; }

        [JsonProperty("battery_time_remaining", NullValueHandling = NullValueHandling.Ignore)]
        public int BatteryTimeRemaining { get; set; }

        [JsonProperty("battery_percentage", NullValueHandling = NullValueHandling.Ignore)]
        public int BatteryPercentage { get; set; }

        [JsonProperty("moved", NullValueHandling = NullValueHandling.Ignore)]
        public int Moved { get; set; }

        [JsonProperty("mission_queue_id", NullValueHandling = NullValueHandling.Ignore)]
        public int MissionQueueId { get; set; }

        [JsonProperty("mission_queue_url", NullValueHandling = NullValueHandling.Ignore)]
        public string MissionQueueUrl { get; set; }

        [JsonProperty("mission_text", NullValueHandling = NullValueHandling.Ignore)]
        public string MissionText { get; set; }

        [JsonProperty("distance_to_next_target", NullValueHandling = NullValueHandling.Ignore)]
        public int DistanceToNextTarget { get; set; }

        [JsonProperty("robot_name", NullValueHandling = NullValueHandling.Ignore)]
        public string RobotName { get; set; }

        [JsonProperty("robot_model", NullValueHandling = NullValueHandling.Ignore)]
        public string RobotModel { get; set; }

        [JsonProperty("serial_number", NullValueHandling = NullValueHandling.Ignore)]
        public string SerialNumber { get; set; }

        [JsonProperty("session_id", NullValueHandling = NullValueHandling.Ignore)]
        public string SessionId { get; set; }

        [JsonProperty("state_id", NullValueHandling = NullValueHandling.Ignore)]
        public int StateId { get; set; }

        [JsonProperty("state_text", NullValueHandling = NullValueHandling.Ignore)]
        public string StateText { get; set; }

        [JsonProperty("mode_id", NullValueHandling = NullValueHandling.Ignore)]
        public int ModeId { get; set; }

        [JsonProperty("mode_text", NullValueHandling = NullValueHandling.Ignore)]
        public string ModeText { get; set; }

        [JsonProperty("joystick_web_session_id", NullValueHandling = NullValueHandling.Ignore)]
        public string JoystickWebSessionId { get; set; }

        [JsonProperty("map_id", NullValueHandling = NullValueHandling.Ignore)]
        public string MapId { get; set; }

        [JsonProperty("unloaded_map_changes", NullValueHandling = NullValueHandling.Ignore)]
        public bool UnloadedMapChanges { get; set; }

        [JsonProperty("safety_system_muted", NullValueHandling = NullValueHandling.Ignore)]
        public bool SafetySystemMuted { get; set; }

        [JsonProperty("joystick_low_speed_mode_enabled", NullValueHandling = NullValueHandling.Ignore)]
        public bool JoystickLowSpeedModeEnabled { get; set; }

        [JsonProperty("mode_key_state", NullValueHandling = NullValueHandling.Ignore)]
        public string ModeKeyState { get; set; }

        [JsonProperty("uptime", NullValueHandling = NullValueHandling.Ignore)]
        public int Uptime { get; set; }

        public class StatusPosition
        {
            [JsonProperty("x", NullValueHandling = NullValueHandling.Ignore)]
            public int X { get; set; }

            [JsonProperty("y", NullValueHandling = NullValueHandling.Ignore)]
            public int Y { get; set; }

            [JsonProperty("orientation", NullValueHandling = NullValueHandling.Ignore)]
            public int Orientation { get; set; }
        }

        public class StatusVelocity
        {
            [JsonProperty("linear", NullValueHandling = NullValueHandling.Ignore)]
            public int Linear { get; set; }

            [JsonProperty("angular", NullValueHandling = NullValueHandling.Ignore)]
            public int Angular { get; set; }
        }

    }
}
