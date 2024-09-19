using Microsoft.JSInterop;

namespace EiTSoftBot.Services
{
    public class ThreeJsService
    {
        private IJSRuntime _jsRuntime;
        public ThreeJsService(IJSRuntime jsRuntime)
        {
            _jsRuntime = jsRuntime ?? throw new ArgumentNullException(nameof(jsRuntime));
        }

        public async Task Initialize(string containerId)
        {
            await _jsRuntime.InvokeVoidAsync("init3DScene", containerId);
        }

        public async Task IsInitialized()
        {
            await _jsRuntime.InvokeVoidAsync("is3DInitialized");
        }
    }
}
