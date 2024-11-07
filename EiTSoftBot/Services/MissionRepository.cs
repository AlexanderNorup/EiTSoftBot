using EiTSoftBot.Dto;
using EiTSoftBot.Dto.Entities;
using EiTSoftBot.Dto.Responses;
using System.Text.Json;

namespace EiTSoftBot.Services
{
    public class MissionRepository : IDisposable
    {
        public static readonly string MissionCachePath = Path.Combine(AppContext.BaseDirectory, "cache", "missions.json");
        private List<Mission> _missions = new List<Mission>();
        public IReadOnlyList<Mission> Missions => _missions.AsReadOnly();

        private SimulatorClient _simulatorClient;
        private ILogger<MissionRepository> _logger;

        public MissionRepository(SimulatorClient simulatorClient, ILogger<MissionRepository> logger)
        {
            _logger = logger;
            _simulatorClient = simulatorClient;
            _simulatorClient.OnMessageRecieved += OnMessageRecieved;
        }

        private void OnMessageRecieved(BaseMessage message)
        {
            if (message is GetAllMissionsResponse response)
            {
                _missions = response.Missions;
            }
        }

        public async Task LoadFromCache()
        {
            try
            {
                if (File.Exists(MissionCachePath))
                {
                    var json = await File.ReadAllTextAsync(MissionCachePath);
                    _missions = JsonSerializer.Deserialize<List<Mission>>(json)
                        ?? throw new InvalidDataException("Json Deserialized to null");
                }
                else
                {
                    _logger.LogWarning("Mission cache not found");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to load missions from cache");
            }
        }

        public async Task PersistToCache()
        {
            var directory = Path.GetDirectoryName(MissionCachePath);
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory!);
            }
            try
            {
                var json = JsonSerializer.Serialize(_missions);
                await File.WriteAllTextAsync(MissionCachePath, json);
                _logger.LogInformation("Missions persisted to cache => {File}", MissionCachePath);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to persist missions to cache");
            }
        }

        public void Dispose()
        {
            _simulatorClient.OnMessageRecieved -= OnMessageRecieved;
        }
    }
}