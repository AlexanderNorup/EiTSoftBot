using Newtonsoft.Json;

namespace EiTSoftBot.Dto
{
    public static class RequestSerializer
    {
        private static JsonSerializerSettings JsonSerializerSettings = new JsonSerializerSettings()
        {
            TypeNameHandling = TypeNameHandling.Objects,
        };

        public static string Serialize(object request)
        {
            return JsonConvert.SerializeObject(request, JsonSerializerSettings);
        }

        public static BaseMessage Deserialize(string request)
        {
            return JsonConvert.DeserializeObject<BaseMessage>(request, JsonSerializerSettings)!;
        }
    }
}
