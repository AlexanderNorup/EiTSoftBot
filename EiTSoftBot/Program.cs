using EiTSoftBot.Components;
using EiTSoftBot.Services;
using MQTTnet;
using MQTTnet.Client;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddScoped<MirConfigJsInteropService>();

builder.Services.AddSingleton((s) =>
{
    var mqttClientOptions = new MqttClientOptionsBuilder()
        .WithTcpServer(builder.Configuration["MqttConfig:MqttHost"])
        .WithCredentials(builder.Configuration["MqttConfig:MqttUsername"], builder.Configuration["MqttConfig:MqttPassword"])
        .WithCleanSession()
        .Build();

    return mqttClientOptions;
});

builder.Services.AddScoped<SimulatorClient>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles(new StaticFileOptions()
{
    ServeUnknownFileTypes = true,
});
app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
