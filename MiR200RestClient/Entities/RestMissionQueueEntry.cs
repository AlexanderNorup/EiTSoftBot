using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestMissionQueueEntry
    {
        [JsonProperty("mission_id", NullValueHandling = NullValueHandling.Ignore)]
        public string MissionId { get; set; }

        [JsonProperty("parameters", NullValueHandling = NullValueHandling.Ignore)]
        public List<object> Parameters { get; set; } = new();
    }
}
