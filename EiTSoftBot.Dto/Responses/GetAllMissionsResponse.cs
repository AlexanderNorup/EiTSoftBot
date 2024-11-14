using EiTSoftBot.Dto.Entities;
using Newtonsoft.Json;

namespace EiTSoftBot.Dto.Responses
{
    public class GetAllMissionsResponse : BaseMessage
    {
        public override string MessageName => nameof(GetAllMissionsResponse);

        public List<Mission> Missions { get; set; } = new();
    }
}
