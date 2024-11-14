using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestSettingSet
    {
        [JsonProperty("value", NullValueHandling = NullValueHandling.Ignore)]
        public double Value { get; set; }
    }
}
