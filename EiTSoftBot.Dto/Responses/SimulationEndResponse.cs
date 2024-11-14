using EiTSoftBot.Dto.Entities;

namespace EiTSoftBot.Dto.Responses
{
    public class SimulationEndResponse : BaseMessage
    {
        public override string MessageName => nameof(SimulationEndResponse);
        public Mission? Mission { get; set; }
    }
}
