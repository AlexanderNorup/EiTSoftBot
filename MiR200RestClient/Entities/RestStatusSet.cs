using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestStatusSet
    {
        [JsonProperty("state_id", NullValueHandling = NullValueHandling.Ignore)]
        public MirState StateId { get; set; }
    }
}
