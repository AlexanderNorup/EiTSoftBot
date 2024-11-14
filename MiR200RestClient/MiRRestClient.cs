using MiR200RestClient.Entities;
using Newtonsoft.Json;
using System.Net.Http.Headers;
using System.Text;

namespace MiR200RestClient
{
    /// <summary>
    /// We wanted to use the OpenAPI generated client, but the spec have some missing information
    /// which makes most of the generated code unusable (<see cref="MissionsClient.ActionsAllAsync"/> I'm looking at you..)<br/>
    /// So we just decided to make our own complimentary client for our narrow usecase. 
    /// </summary>
    public class MiRRestClient : IDisposable
    {
        private readonly HttpClient _httpClient;
        public MiRRestClient(string baseAddress, string token)
        {
            _httpClient = new HttpClient()
            {
                BaseAddress = new Uri(baseAddress),
                DefaultRequestHeaders = {
                    Authorization = new AuthenticationHeaderValue("Basic", token),
                }
            };
        }

        public async Task<List<RestMission>> GetMissionsForSessionAsync(string sessionId)
        {
            const string RequestUri = "missions/search?limit=10000&offset=0&only_data=false&whitelist=name,group_id,guid,session_id,created_by_name,hidden,description,valid,is_template&sort_by=name,asc";
            const string SessionIdField = "session_id";

            var response = await _httpClient.PostAsync(RequestUri, Serialize(new RestSearchFilter()
            {
                Filters = new List<RestSearchFilter.Filter>()
                {
                    new(SessionIdField, "=", sessionId)
                }
            })).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return await DeserializeAsync<List<RestMission>>(response.Content);
        }

        public async Task<List<RestMissionAction>> GetActionsForMissionAsync(string missionId)
        {
            string requestUri = $"missions/{missionId}/actions";

            var response = await _httpClient.GetAsync(requestUri).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return await DeserializeAsync<List<RestMissionAction>>(response.Content);
        }

        public async Task<bool> AddActionToMissionAsync(string missionId, RestMissionAction newAction)
        {
            string requestUri = $"missions/{missionId}/actions";
            var response = await _httpClient.PostAsync(requestUri, Serialize(newAction)).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> DeleteActionFromMission(string missionId, string actionId)
        {
            string requestUri = $"missions/{missionId}/actions/{actionId}";
            var response = await _httpClient.DeleteAsync(requestUri).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return response.IsSuccessStatusCode;
        }

        public async Task<RestPosition> GetPositionAsync(string positionId)
        {
            string requestUri = $"positions/{positionId}";
            var response = await _httpClient.GetAsync(requestUri).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return await DeserializeAsync<RestPosition>(response.Content);
        }

        public async Task<RestStatus> GetStatusAsync(TimeSpan? timeout = null)
        {
            string requestUri = $"status";
            var cts = new CancellationTokenSource();
            if (timeout is not null)
            {
                cts.CancelAfter(timeout.Value);
            }
            var response = await _httpClient.GetAsync(requestUri, cts.Token).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return await DeserializeAsync<RestStatus>(response.Content);
        }

        public async Task<RestStatus> SetStatusAsync(RestStatusSet newStatus)
        {
            string requestUri = $"status";
            var response = await _httpClient.PutAsync(requestUri, Serialize(newStatus)).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return await DeserializeAsync<RestStatus>(response.Content);
        }

        public async Task<bool> SetAccelerationAsync(RestSettingSet newAccel)
        {
            const string requestUri = "settings/2076";
            var response = await _httpClient.PutAsync(requestUri, Serialize(newAccel)).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> AddMissionToQueueAsync(RestMissionQueueEntry newEntry)
        {
            const string requestUri = "mission_queue";
            var response = await _httpClient.PostAsync(requestUri, Serialize(newEntry)).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> ClearMissionQueueAsync()
        {
            const string requestUri = "mission_queue";
            var response = await _httpClient.DeleteAsync(requestUri).ConfigureAwait(false);
            await EnsureSuccessAndLog(response);
            return response.IsSuccessStatusCode;
        }

        private async static Task<T> DeserializeAsync<T>(HttpContent content)
        {
            await content.LoadIntoBufferAsync().ConfigureAwait(false); // So we can potentially read the content multiple times in case of exceptions (where we'd like logging)
            try
            {
                using var reader = new StreamReader(await content.ReadAsStreamAsync().ConfigureAwait(false));
                using var jsonReader = new JsonTextReader(reader);
                return new JsonSerializer().Deserialize<T>(jsonReader) ??
                    throw new InvalidDataException("Deserialized JSON data was null.");
            }
            catch (Exception e)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"Failed to deserialize JSON-body to {typeof(T).FullName}. Error: {e.Message}.\nFull JSON-body:");
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine(await content.ReadAsStringAsync());
                Console.ResetColor();
                throw;
            }
        }

        private async static Task EnsureSuccessAndLog(HttpResponseMessage response)
        {
            if (!response.IsSuccessStatusCode)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"Got {response.StatusCode} on request {response.RequestMessage?.Method} {response.RequestMessage?.RequestUri}: {response.ReasonPhrase}");
                Console.ForegroundColor = ConsoleColor.Gray;
                Console.WriteLine(await response.Content.ReadAsStringAsync());
                Console.ResetColor();
            }
            response.EnsureSuccessStatusCode();
        }

        private static HttpContent Serialize(object o)
        {
            return new StringContent(
                JsonConvert.SerializeObject(o),
                Encoding.UTF8,
                "application/json");
        }

        public void Dispose()
        {
            ((IDisposable)_httpClient).Dispose();
        }
    }
}