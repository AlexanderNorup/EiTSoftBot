﻿using MiR200RestClient;

namespace MiRCommunicator
{
    internal class MirMonitor : IDisposable
    {
        private readonly MiRRestClient client;
        private readonly System.Timers.Timer timer;
        public MirMonitor(MiRRestClient client)
        {
            this.client = client;
            timer = new System.Timers.Timer(TimeSpan.FromSeconds(10));
            timer.Elapsed += async (sender, e) => await RefreshState();
            timer.Start();
            _ = RefreshState();
        }

        public bool MirConnected { get; private set; }
        public int MirStatus { get; private set; } = -1;
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
                var status = await client.GetStatusAsync(TimeSpan.FromSeconds(1));

                if (status is not null)
                {
                    MirConnected = true;
                    MirStatus = status.StateId;
                }
            }
            catch (Exception e) when (e is OperationCanceledException or HttpRequestException)
            {
                MirConnected = false;
                MirStatus = -1;
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
