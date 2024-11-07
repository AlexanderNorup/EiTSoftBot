using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestSearchFilter
    {
        [JsonProperty("filters", NullValueHandling = NullValueHandling.Ignore)]
        public List<Filter> Filters { get; set; }

        public record Filter(
            [property: JsonProperty("fieldname", NullValueHandling = NullValueHandling.Ignore)] string Fieldname,
            [property: JsonProperty("operator", NullValueHandling = NullValueHandling.Ignore)] string Operator,
            [property: JsonProperty("value", NullValueHandling = NullValueHandling.Ignore)] string Value
        );
    }
}
