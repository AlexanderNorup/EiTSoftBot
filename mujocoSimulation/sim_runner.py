from config import *

import src.routeConverter as rC
import src.optimizer as optim
import src.simulation as sim
from src.boxesXmlWriter import *

def run_simulation(boxes, waypoints):
    if os.path.isfile("xmlFiles/boxes.xml"):
        os.remove("xmlFiles/boxes.xml")
    
    writeBoxes(boxes, 0.05)

    env = MuJoCoParserClass(name='mir200',rel_xml_path=xml_path,verbose=True)
    env.model.geom('floor').priority = 1 # 0=>1

    numBox=len(boxes)

    route = rC.routeConverter(waypoints)
    simulation = sim.simulation(env,numBox,route,True)
    out,sim_time=optim.optimizer.run()
    print(sim_time)
    return out