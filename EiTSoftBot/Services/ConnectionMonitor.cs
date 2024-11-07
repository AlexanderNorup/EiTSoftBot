using EiTSoftBot.Dto.Responses;

namespace EiTSoftBot.Services
{
    public class ConnectionMonitor : IDisposable
    {
        private readonly SimulatorClient client;
        private readonly System.Timers.Timer timer;
        public ConnectionMonitor(SimulatorClient client)
        {
            this.client = client;
            timer = new System.Timers.Timer(TimeSpan.FromSeconds(10));
            timer.Elapsed += async (sender, e) => await RefreshState();
            timer.Start();
        }

        public bool MirConnected { get; private set; }
        public bool SimulatorConnected { get; private set; }
        private bool IsRefreshing { get; set; }

        public async Task RefreshState()
        {
            if (IsRefreshing)
            {
                return;
            };
            IsRefreshing = true;
            try
            {
                (var newMir, var newSim) = await client.GetOtherClientConnectionStatus(TimeSpan.FromSeconds(1));

                if (newMir != MirConnected || newSim != SimulatorConnected)
                {
                    MirConnected = newMir;
                    SimulatorConnected = newSim;
                    client.SimulateRecieveMessage(new RefreshStateMessage());
                }
            }
            finally
            {
                IsRefreshing = false;
            }
        }

        public void Dispose()
        {
            timer.Stop();
            timer.Dispose();
        }
    }
}
