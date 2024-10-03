import os
import shutil
import configPrint
import sdfPrint
import spawner

x = 0
i = 0
mirz = 0.352

mainPath = "../../../catkin_ws/src/mir_robot/mir_gazebo"

while x < 2:
    print('Add box enter 1, load to simulator enter 2, exit enter 3')
    x = int(input())

    if x == 1:
        i+=1
        if os.path.isdir(mainPath + "/sdf/box" + str(i)):
            shutil.rmtree(mainPath + "/sdf/box" + str(i))
        os.makedirs(mainPath + "/sdf/box" + str(i)) # add own path
        configPrint.writeConfig(mainPath + "/sdf/box" + str(i) + "/model.config",i)

        print('enter box weight')
        w = input()

        print('enter box size (x,y,z)')
        s0_data = input() #x mir driving direction
        s1_data = input() #y
        s2_data = input() #z
        s = [s0_data,s1_data,s2_data]

        print('enter box placement')
        p0_data = input() #x
        p1_data = input() #y
        p2_data = float(input()) + mirz #z
        p = [p0_data,p1_data,p2_data]

        mu1=0.54
        mu2=0.32

        sdfPrint.writeSdf(mainPath + "/sdf/box" + str(i) + "/model.sdf",p,w,s,mu1,mu2)

    if x == 2:
        if os.path.isfile(mainPath + "/launch/includes/spawn_box.launch.xml"):
            os.remove(mainPath + "/launch/includes/spawn_box.launch.xml")
        
        print('Program will now open simulation')
        spawner.spawnBox(mainPath + "/launch/includes/spawn_box.launch.xml", i)
        os.system("roslaunch mir_gazebo mir_empty_world.launch")

print('Something went wrong or you exited the program')