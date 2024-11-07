using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestActionParameter
    {
        [JsonProperty("guid", NullValueHandling = NullValueHandling.Ignore)]
        public string Guid { get; set; }

        [JsonProperty("id", NullValueHandling = NullValueHandling.Ignore)]
        public string Id { get; set; }

        [JsonProperty("input_name", NullValueHandling = NullValueHandling.Ignore)]
        public object InputName { get; set; }

        [JsonProperty("value", NullValueHandling = NullValueHandling.Ignore)]
        public string Value { get; set; }
    }
}
