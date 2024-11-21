using EiTSoftBot.Dto.Entities;
using Microsoft.JSInterop;

namespace EiTSoftBot.Services
{
    public class MirConfigJsInteropService
    {
        private IJSRuntime _jsRuntime;
        public MirConfigJsInteropService(IJSRuntime jsRuntime)
        {
            _jsRuntime = jsRuntime ?? throw new ArgumentNullException(nameof(jsRuntime));
        }

        public async Task Initialize3DScene(string containerId)
        {
            await _jsRuntime.InvokeVoidAsync("init3DScene", containerId);
        }

        public async Task Is3DSceneInitialized()
        {
            await _jsRuntime.InvokeVoidAsync("is3DInitialized");
        }

        public async Task<List<JsBox>> GetBoxConfiguration()
        {
            return await _jsRuntime.InvokeAsync<List<JsBox>>("getAll2DBoxes").ConfigureAwait(false);
        }

        public async Task Set3DMission(Mission mission)
        {
            await _jsRuntime.InvokeVoidAsync("loadMission", mission);
        }
        
        public async Task Clear3DMission()
        {
            await _jsRuntime.InvokeVoidAsync("clearMission");
        }
    }
}
