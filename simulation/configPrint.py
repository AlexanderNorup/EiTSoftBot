def writeConfig(path, i):
    f = open(path, "a")
    f.write("<?xml version=\"1.0\"?>")
    f.write("\n")
    f.write("\n")
    f.write("<model>")
    f.write("\n")
    f.write("  <name>box" + str(i) + "</name>")
    f.write("\n")
    f.write("  <version>1.0</version>")
    f.write("\n")
    f.write("  <sdf version=\"1.5\">model.sdf</sdf>")
    f.write("\n")
    f.write("\n")
    f.write("  <author>")
    f.write("\n")
    f.write("    <name>0</name>")
    f.write("\n")
    f.write("    <email>0</email>")
    f.write("\n")
    f.write("  </author>")
    f.write("\n")
    f.write("\n")
    f.write("  <description>")
    f.write("\n")
    f.write("    box")
    f.write("\n")
    f.write("  </description>")
    f.write("\n")
    f.write("</model>")
    f.close()