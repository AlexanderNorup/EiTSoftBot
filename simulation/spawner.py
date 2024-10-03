def spawnBox(path, i):
    f = open(path, "a")
    f.write("<?xml version=\"1.0\"?>")
    f.write("\n")
    f.write("<launch>")
    f.write("\n")
    for x in range(i):
        f.write("    <node name=\"box" + str(x+1) + "\" pkg=\"gazebo_ros\" type=\"spawn_model\" args=\"-sdf -file $(find mir_gazebo)/sdf/box" + str(x+1) + "/model.sdf -model box" + str(x+1) + "\" output=\"screen\" />")
        f.write("\n")
    f.write("</launch>")
    f.close()