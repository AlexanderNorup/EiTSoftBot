# MiRCommunicator

This .NET Core Console Application bridges the gap between the MQTT broker and MiR200's REST API.

## Getting started

1. Have .NET Core 8.0 or higher installed
    - https://dotnet.microsoft.com/en-us/download/dotnet/8.0
2. Configure `appsettings[.Development].json` or your user-secrets to point to your MQTT broker (Under the `MirCommunicatorConfig` section). 
    - Required fields:
        - `MqttHost`
        - `MqttUsername`
        - `MqttPassword`
        - `MqttResponseTopic` - Make sure it matches the value configured in the Web-UI
        - `MqttRequestTopic` - Make sure it matches the value configured in the Web-UI
        - `MirApiEndpoint` - MiR endpont with version. I.e. `http://mir.com/api/v2.0.0/`
        - `MirApiToken` - Can be copied from the MiR's interface under "Help" and "API Documentation"
        - `MirSessionId` - The ID of the map session. This will be used to filter which missions are sent back to the UI.
3. Start it using `dotnet run`
