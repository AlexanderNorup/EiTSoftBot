using EiTSoftBot.Dto;
using EiTSoftBot.Dto.Entities;
using EiTSoftBot.Dto.Requests;
using EiTSoftBot.Dto.Responses;
using MiR200RestClient;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Protocol;
using System.Text;

namespace MiRCommunicator
{
    internal class RequestHandler(IMqttClient mqttClient, MirCommunicatorConfig config)
    {
        public async Task HandleRequestAsync(BaseMessage baseMessage)
        {
            switch (baseMessage)
            {
                case GetAllMissionsRequest getAllMissionsRequest:
                    await HandleGetAllMissionsRequest(getAllMissionsRequest);
                    break;
                default:
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"Unknown reques type: {baseMessage.GetType().Name}");
                    Console.ResetColor();
                    break;
            }
        }

        private async Task HandleGetAllMissionsRequest(GetAllMissionsRequest getAllMissionsRequest)
        {
            var missionClient = new MissionsClient();
            if (!string.IsNullOrWhiteSpace(config.MirApiEndpoint))
            {
                missionClient.BaseUrl = config.MirApiEndpoint;
            }

            var response = new GetAllMissionsResponse();
            // FOR TESTING, please ignore
            //response.Missions = new List<Mission>()
            //{
            //    new Mission(Guid.NewGuid().ToString(), "Best mission", new List<MirAction>()
            //    {
            //        new MirAction("Action1", "move", "I don't know what will be in this parameter"),
            //        new MirAction("Action2", "set_speed", "I don't know what will be in this parameter"),
            //        new MirAction("Action3", "move", "I don't know what will be in this parameter"),
            //    }),
            //    new Mission(Guid.NewGuid().ToString(), "Wow very nice mission", new List<MirAction>()
            //    {
            //        new MirAction("Action1", "move", "I don't know what will be in this parameter"),
            //        new MirAction("Action2", "set_speed", "I don't know what will be in this parameter"),
            //        new MirAction("Action3", "move", "I don't know what will be in this parameter"),
            //    }),
            //    new Mission(Guid.NewGuid().ToString(), "THE BEST MISSION", new List<MirAction>()
            //    {
            //        new MirAction("Action1", "go_home", "I don't know what will be in this parameter"),
            //    }),
            //};

            var allMissions = await missionClient.MissionsAll2Async(0, AcceptLanguage.En_US);
            foreach (var mission in allMissions)
            {
                List<MirAction> responseActions = new();
                var actions = await missionClient.ActionsAllAsync(0, AcceptLanguage.En_US, mission.Guid);
                foreach (var action in actions)
                {
                    responseActions.Add(new MirAction(action.Guid, action.Action_type, action.Parameters));
                }

                response.Missions.Add(new Mission(mission.Guid, mission.Name, responseActions));
            }

            await SendResponse(response);
        }


        private async Task SendResponse(BaseMessage response)
        {
            var responseJson = RequestSerializer.Serialize(response);
            var responseMessage = new MqttApplicationMessageBuilder()
                .WithTopic(config.MqttResponseTopic)
                .WithPayload(Encoding.UTF8.GetBytes(responseJson))
                .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.ExactlyOnce)
                .Build();

            Console.WriteLine($"Sending response of type: {response.GetType().Name}");
            await mqttClient.PublishAsync(responseMessage);
        }
    }
}
