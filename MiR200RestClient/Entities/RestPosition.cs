using Newtonsoft.Json;

namespace MiR200RestClient.Entities
{
    public class RestPosition
    {
        [JsonProperty("allowed_methods", NullValueHandling = NullValueHandling.Ignore)]
        public List<string> AllowedMethods { get; set; }

        [JsonProperty("created_by", NullValueHandling = NullValueHandling.Ignore)]
        public string CreatedBy { get; set; }

        [JsonProperty("created_by_id", NullValueHandling = NullValueHandling.Ignore)]
        public string CreatedById { get; set; }

        [JsonProperty("created_by_name", NullValueHandling = NullValueHandling.Ignore)]
        public string CreatedByName { get; set; }

        [JsonProperty("docking_offsets", NullValueHandling = NullValueHandling.Ignore)]
        public string DockingOffsets { get; set; }

        [JsonProperty("guid", NullValueHandling = NullValueHandling.Ignore)]
        public string Guid { get; set; }

        [JsonProperty("help_positions", NullValueHandling = NullValueHandling.Ignore)]
        public string HelpPositions { get; set; }

        [JsonProperty("map", NullValueHandling = NullValueHandling.Ignore)]
        public string Map { get; set; }

        [JsonProperty("map_id", NullValueHandling = NullValueHandling.Ignore)]
        public string MapId { get; set; }

        [JsonProperty("name", NullValueHandling = NullValueHandling.Ignore)]
        public string Name { get; set; }

        [JsonProperty("orientation", NullValueHandling = NullValueHandling.Ignore)]
        public double Orientation { get; set; }

        [JsonProperty("parent", NullValueHandling = NullValueHandling.Ignore)]
        public object Parent { get; set; }

        [JsonProperty("parent_id", NullValueHandling = NullValueHandling.Ignore)]
        public object ParentId { get; set; }

        [JsonProperty("pos_x", NullValueHandling = NullValueHandling.Ignore)]
        public double PosX { get; set; }

        [JsonProperty("pos_y", NullValueHandling = NullValueHandling.Ignore)]
        public double PosY { get; set; }

        [JsonProperty("type", NullValueHandling = NullValueHandling.Ignore)]
        public string Type { get; set; }

        [JsonProperty("type_id", NullValueHandling = NullValueHandling.Ignore)]
        public int TypeId { get; set; }
    }
}
