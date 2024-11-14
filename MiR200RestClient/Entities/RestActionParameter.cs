using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestActionParameter
    {
        [JsonProperty("guid", NullValueHandling = NullValueHandling.Include)]
        public string Guid { get; set; }

        [JsonProperty("id", NullValueHandling = NullValueHandling.Include)]
        public string Id { get; set; }

        [JsonProperty("input_name", NullValueHandling = NullValueHandling.Include)]
        public object InputName { get; set; }

        [JsonProperty("value", NullValueHandling = NullValueHandling.Include)]
        public object Value { get; set; }
    }
}
