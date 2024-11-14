using MiR200RestClient.Entities;

namespace MiRCommunicator
{
    internal static class MirActionFactory
    {
        internal static RestMissionAction GetSpeedActionParameter(int priority, double newSpeed)
        {
            return new RestMissionAction()
            {
                Priority = priority,
                Guid = Guid.NewGuid().ToString(),
                ActionType = "planner_settings",
                Parameters = new()
                {
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "planner_params",
                        Value = "desired_speed_key"
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "desired_speed",
                        Value = newSpeed
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "path_timeout",
                        Value = "5"
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "path_deviation",
                        Value = "5"
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "obstacle_history",
                        Value = null!
                    }
                }
            };
        }

        internal static RestMissionAction GetMoveActionParameter(int priority, string posId)
        {
            return new RestMissionAction()
            {
                Priority = priority,
                ActionType = "move",
                Guid = Guid.NewGuid().ToString(),
                Parameters = new()
                {
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "position",
                        Value = posId
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "cart_entry_position",
                        Value = null!
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "main_or_entry_position",
                        Value = null!
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "marker_entry_position",
                        Value = null!
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "blocked_path_timeout",
                        Value = 60d
                    },
                    new RestActionParameter()
                    {
                        Guid = Guid.NewGuid().ToString(),
                        Id = "distance_threshold",
                        Value = 0.1d
                    }
                }
            };
        }
    }
}
