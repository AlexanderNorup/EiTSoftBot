using EiTSoftBot.Dto.Entities;

namespace EiTSoftBot.Dto.Requests
{
    public class SimulationStartRequest : BaseMessage
    {
        public override string MessageName => nameof(SimulationStartRequest);
        public List<MujocoBox> Boxes { get; set; } = new();
        public required Mission Mission { get; set; }
    }
}
