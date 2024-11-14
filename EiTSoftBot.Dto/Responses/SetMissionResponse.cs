using EiTSoftBot.Dto.Requests;

namespace EiTSoftBot.Dto.Responses
{
    public class SetMissionResponse : BaseMessage
    {
        public override string MessageName => nameof(SetMissionResponse);
        public bool Success { get; set; }
    }
}
