using EiTSoftBot.Dto.Entities;

namespace EiTSoftBot.Dto.Requests
{
    public class SetMissionRequest : BaseMessage
    {
        public override string MessageName => nameof(SetMissionRequest);
        public required Mission Mission { get; set; }
        public double? MaxAcceleration { get; set; }
    }
}
