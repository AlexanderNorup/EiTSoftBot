namespace EiTSoftBot.Dto.Requests
{
    public class SetMirStatusRequest : BaseMessage
    {
        public override string MessageName => nameof(SetMirStatusRequest);
        public bool Ready { get; set; }
    }
}
