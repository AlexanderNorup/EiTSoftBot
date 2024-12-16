from config import *

import src.optimizer as optim
from src.boxesXmlWriter import *


def run_simulation(boxes, waypoints):

    writeBoxes(boxes,0.05) #0.032

    xml_path = "xmlFiles/mobile_platform.xml"

    env = MuJoCoParserClass(name='mir200',rel_xml_path=xml_path,verbose=True)
    env.model.opt.timestep = env.model.opt.timestep*20.
    env.model.geom('floor').priority = 1 # 0=>1

    numBox=len(boxes)

    visualize = os.getenv('VISUALIZE', "false").lower().strip() == "true"
    controlType = os.getenv('CONTROL', "false").lower().strip() == "true"

    print(f"Visualize enabled: {visualize}")

    optimizer = optim.optimizer(env,numBox,waypoints,visualize,controlType,maxTick)
    out=optimizer.runGridDescent()
    print(out)
    print(optimizer.grid)
    # for test puposes
    # out=optimizer.runSpecific(.4,.1)
    if out[0]>0 and out[1]>0:
        print(f"Accel={out[0]}, Velocity={out[1]}", flush=True)
    else:
        print("not possible")
    return out

if __name__ == '__main__':
    boxesReceived = [[[-0.055, 0.1, 0.442], [0.038, 0.092, 0.082], 0.612], [[-0.055, -0.087, 0.442], [0.038, 0.092, 0.082], 0.657], [[-0.035, -0.002, 0.588], [0.052, 0.092, 0.062], 0.64]]
    routeCoordinates = [[6.0, 2.5, 0.0], [6.9, 2.5, 0.0],[7.8, 2.5, 1.5707963267948966], [7.8, 14.7, 3.141592653589793]]
    run_simulation(boxesReceived, routeCoordinates)
    print("Simulation finished!")
