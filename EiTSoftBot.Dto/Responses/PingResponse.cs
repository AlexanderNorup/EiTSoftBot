namespace EiTSoftBot.Dto.Responses
{
    public class PingResponse : BaseMessage
    {
        public override string MessageName => nameof(PingResponse);
        public required string PingId { get; set; }
        public required string Source { get; set; }
    }
}
