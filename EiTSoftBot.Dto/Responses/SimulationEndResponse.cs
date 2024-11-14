using EiTSoftBot.Dto.Entities;

namespace EiTSoftBot.Dto.Responses
{
    public class SimulationEndResponse : BaseMessage
    {
        public override string MessageName => nameof(SimulationEndResponse);
        public required Mission Mission { get; set; }
        public double MaxAcceleration { get; set; } = 1.0d;
    }
}
