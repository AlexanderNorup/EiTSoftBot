import os

while True:
    print("input linear velocity -1.0-1.0[m/s]")
    x = input()

    print("input angular velocity -1.5-1.5[m/s]")
    z = input()

    os.system("rostopic pub /cmd_vel geometry_msgs/Twist -r 1 -- '[" + x + ",0.0,0.0]' '[0.0,0.0," + z + "]'")

    print("stops movement")
