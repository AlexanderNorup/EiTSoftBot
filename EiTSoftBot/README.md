# Blazor Server Web-UI

This WEB-UI for making box-configurations and sending them off to the Simulation and the finalized missions back to the MiR.

## Getting started

1. Have .NET Core 8.0 or higher installed
    - https://dotnet.microsoft.com/en-us/download/dotnet/8.0
2. Configure `appsettings[.Development].json` or your user-secrets to point to your MQTT broker (Under the `MqttConfig` section). 
    - Required fields:
        - `MqttHost`
        - `MqttUsername`
        - `MqttPassword`
        - `MqttTopic` - Topic the simulation uses
        - `MqttResponseTopic` - Response topic for both Simulation and MiRCommunicator
        - `MqttRequestTopic` - Topic the MiRCommunicator uses
3. Start it using `dotnet run`
