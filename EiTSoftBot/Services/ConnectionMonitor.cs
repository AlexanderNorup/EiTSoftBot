using EiTSoftBot.Dto.Responses;
using MQTTnet.Client;

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
            _ = RefreshState();
        }

        public bool MirConnectorConnected { get; private set; }
        public bool MirConnected { get; private set; }
        public int MirStatus { get; private set; } = -1;
        public bool SimulatorConnected { get; private set; }
        private bool IsRefreshing { get; set; }

        public string MirStatusString => MirStatus switch
        {
            3 => "Ready",
            4 => "Paused",
            5 => "Running",
            10 => "Emergency Stop",
            12 => "Manual Control",
            _ => "Unknown"
        };

        public async Task RefreshState()
        {
            if (IsRefreshing)
            {
                return;
            };
            IsRefreshing = true;
            try
            {
                var status = await client.GetOtherClientConnectionStatus(TimeSpan.FromSeconds(1));

                if (status.mirConnectorConnected != MirConnectorConnected
                    || status.mirConnected != MirConnected
                    || status.mirStatus != MirStatus
                    || status.simulationConnected != SimulatorConnected)
                {
                    MirConnectorConnected = status.mirConnectorConnected;
                    MirConnected = status.mirConnected;
                    MirStatus = status.mirStatus ?? -1;
                    SimulatorConnected = status.simulationConnected;
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
