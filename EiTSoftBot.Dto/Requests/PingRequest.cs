namespace EiTSoftBot.Dto.Requests
{
    public class PingRequest : BaseMessage
    {
        public override string MessageName => nameof(PingRequest);
        public required string PingId { get; set; }
    }
}
