from config import *

import src.routeConverter as rC
import src.optimizer as optim
import src.simulation as sim
import src.plotter as plot
from src.boxesXmlWriter import *


def run_simulation(boxes, waypoints, controlType=0):
    writeBoxes(boxes,0.135)

    xml_path = "xmlFiles/mobile_platform.xml"

    env = MuJoCoParserClass(name='mir200',rel_xml_path=xml_path,verbose=True)
    env.model.geom('floor').priority = 1 # 0=>1

    numBox=len(boxes)

    visualize = os.getenv('VISUALIZE', "true").lower().strip() == "true"

    print(f"Visualize enabled: {visualize}")

    if controlType:
        waypoints = np.asarray(waypoints)
        waypoints = waypoints-waypoints[0]
        simulation = sim.simulationStanley(env,numBox,waypoints,visualize)
    else:
        route = rC.routeConverter(waypoints)
        simulation = sim.simulation(env,numBox,route,visualize)

    optimizer = optim.optimizer(simulation,controlType)
    out=optimizer.run()
    # plt = plot.plotter(env.tick,simulation.time)
    # plt.plotJointPos(simulation.qpos,simulation.qpostrgt)
    if out[0]>0 and out[1]>0:
        print(f"Accel={out[0]}, Velocity={out[1]}", flush=True)
        print(optimizer.output)
        print(optimizer.time)
    else:
        print("not possible")
    return out

if __name__ == '__main__':
    boxesReceived = [[["0.158","0.326","0.452"],[".0525",".0625",".0925"],".063"],[["-0.158","-0.326","0.452"],[".0525",".0625",".0925"],".063"]]
    routeCoordinates = [[6.,2.5,0],[6.9,2.5,0],[7.8,2.5,np.pi/2],[7.8,14.7,np.pi],[6.1,14.7,-np.pi/2],[6.1,9.6,0],[6.9,9.6,-np.pi/2]]
    controlType = os.getenv('CONTROL', "false").lower().strip() == "true"
    run_simulation(boxesReceived, routeCoordinates, controlType)
    print("Simulation finished!")
