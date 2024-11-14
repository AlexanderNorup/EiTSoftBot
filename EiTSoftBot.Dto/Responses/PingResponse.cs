namespace EiTSoftBot.Dto.Responses
{
    public class PingResponse : BaseMessage
    {
        public override string MessageName => nameof(PingResponse);
        public required string PingId { get; set; }
        public required string Source { get; set; }

        /// <summary>
        /// When the MiRCcommunicator responds, we want to know if a MiR is actually connected
        /// </summary>
        public bool? MiRConnected { get; set; }
    }
}
