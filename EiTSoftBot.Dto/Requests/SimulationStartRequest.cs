using EiTSoftBot.Dto.Entities;

namespace EiTSoftBot.Dto.Requests
{
    public class SimulationStartRequest : BaseMessage
    {
        public override string MessageName => nameof(SimulationStartRequest);
        public List<GazeboBox> Boxes { get; set; } = new();
    }
}
