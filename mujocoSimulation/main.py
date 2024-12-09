from config import *

import src.optimizer as optim
from src.boxesXmlWriter import *


def run_simulation(boxes, waypoints):
    writeBoxes(boxes,0.032) #0.032

    xml_path = "xmlFiles/mobile_platform.xml"

    env = MuJoCoParserClass(name='mir200',rel_xml_path=xml_path,verbose=True)
    env.model.opt.timestep = env.model.opt.timestep*20
    env.model.geom('floor').priority = 1 # 0=>1

    numBox=len(boxes)

    visualize = os.getenv('VISUALIZE', "false").lower().strip() == "true"
    controlType = os.getenv('CONTROL', "false").lower().strip() == "true"

    print(f"Visualize enabled: {visualize}")

    optimizer = optim.optimizer(env,numBox,waypoints,visualize,controlType,maxTick)
    out=optimizer.runGridDescent()
    # out=optimizer.runSpecific(1.,1.1)
    if out[0]>0 and out[1]>0:
        print(f"Accel={out[0]}, Velocity={out[1]}", flush=True)
        print(optimizer.grid)
    else:
        print("not possible")
    return out

if __name__ == '__main__':
    boxesReceived = [[["0.326","0.158","0.452"],[".0525",".0625",".0925"],".063"],[["-0.326","-0.158","0.452"],[".0525",".0625",".0925"],".063"]]
    routeCoordinates = [[6.,2.5,0],[6.9,2.5,0],[7.8,2.5,0],[7.8,14.7,0],[6.1,14.7,0],[6.1,9.6,0],[6.9,9.6,0]]
    run_simulation(boxesReceived, routeCoordinates)
    print("Simulation finished!")
