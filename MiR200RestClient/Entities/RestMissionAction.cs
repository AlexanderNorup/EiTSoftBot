using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestMissionAction
    {
        [JsonProperty("action_type", NullValueHandling = NullValueHandling.Ignore)]
        public string ActionType { get; set; }

        [JsonProperty("guid", NullValueHandling = NullValueHandling.Ignore)]
        public string Guid { get; set; }

        [JsonProperty("mission_id", NullValueHandling = NullValueHandling.Ignore)]
        public string MissionId { get; set; }

        [JsonProperty("parameters", NullValueHandling = NullValueHandling.Ignore)]
        public List<RestActionParameter> Parameters { get; set; }

        [JsonProperty("priority", NullValueHandling = NullValueHandling.Ignore)]
        public int Priority { get; set; }

        [JsonProperty("url", NullValueHandling = NullValueHandling.Ignore)]
        public string Url { get; set; }
    }
}
