using Newtonsoft.Json;

namespace EiTSoftBot.Dto.Requests
{
    [JsonObject(ItemTypeNameHandling = TypeNameHandling.All)]
    public class GetAllMissionsRequest : BaseMessage
    {
        public override string MessageName => nameof(GetAllMissionsRequest);
    }
}
