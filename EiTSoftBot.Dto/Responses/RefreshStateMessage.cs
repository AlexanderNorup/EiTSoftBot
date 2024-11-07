namespace EiTSoftBot.Dto.Responses
{
    /// <summary>
    /// A hacky event for triggering a side-wide refresh of the state.
    /// </summary>
    public class RefreshStateMessage : BaseMessage
    {
        public override string MessageName => nameof(RefreshStateMessage);
    }
}
