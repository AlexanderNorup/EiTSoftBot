using EiTSoftBot.Dto;
using Microsoft.Extensions.Configuration;
using MQTTnet;
using MQTTnet.Client;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace MiRCommunicator
{
    internal class Program
    {
        private static RequestHandler? _requestHandler;
        static async Task Main(string[] args)
        {
            var builder = new ConfigurationBuilder()
               .SetBasePath(AppContext.BaseDirectory)
               .AddJsonFile("appsettings.json")
               .AddEnvironmentVariables()
               .AddUserSecrets<Program>();

            var configuration = builder.Build();

            var config = new MirCommunicatorConfig();
            configuration.Bind("MirCommunicatorConfig", config);
            EnsureValid(config);

            var mqttClientOptions = new MqttClientOptionsBuilder()
                .WithTcpServer(config.MqttHost)
                .WithCredentials(config.MqttUsername, config.MqttPassword)
                .WithCleanSession()
                .Build();

            var mqttClient = new MqttFactory().CreateMqttClient();
            await mqttClient.ConnectAsync(mqttClientOptions);
            await mqttClient.SubscribeAsync(config.MqttRequestTopic);

            _requestHandler = new RequestHandler(mqttClient, config);
            mqttClient.ApplicationMessageReceivedAsync += MqttMessageRecieved;

            Console.CancelKeyPress += async delegate
            {
                Console.WriteLine("Shutting down...");
                await mqttClient.DisconnectAsync();
                mqttClient.Dispose();
                Console.WriteLine("Good bye :(");
                await Task.Delay(100);
                Environment.Exit(0);
            };
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("MirCommunicator is ready!");
            Console.ResetColor();
            Console.WriteLine("Press CTRL+C to exit");
            await Task.Delay(-1);
        }

        private static async Task MqttMessageRecieved(MqttApplicationMessageReceivedEventArgs arg)
        {
            if (_requestHandler is null)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("Message recieved without a request handler set!");
                Console.ResetColor();
                return;
            }

            try
            {
                var jsonRaw = Encoding.UTF8.GetString(arg.ApplicationMessage.PayloadSegment);
                var message = RequestSerializer.Deserialize(jsonRaw);
                Console.WriteLine($"Recieved message of type: {message.GetType().Name}");
                await _requestHandler.HandleRequestAsync(message);
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"Handling request failed: {ex.Message}");
                Console.ResetColor();
            }
        }

        private static void EnsureValid(object o)
        {
            var validationErrors = new List<ValidationResult>();
            Validator.TryValidateObject(o, new ValidationContext(o), validationErrors, true);

            if (validationErrors.Any())
            {
                var message = $"Configuration invalid:\n" + string.Join("\n", validationErrors.Select(e => e.ErrorMessage));
                throw new InvalidOperationException(message);
            }
        }
    }
}
