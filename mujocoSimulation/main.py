from config import *

import src.routeConverter as rC
import src.optimizer as optim
from src.boxesXmlWriter import *

boxesReceived = [[["-0.326","-0.158","0.452"],[".0525",".0625",".0925"],".063"]]
writeBoxes(boxesReceived,0.035)

xml_path = "xmlFiles/mobile_platform.xml"

env = MuJoCoParserClass(name='mir200',rel_xml_path=xml_path,verbose=True)
env.model.geom('floor').priority = 1 # 0=>1

numBox=4
vel=1.1

routeCoordinates = [[6.,2.5,0],[6.9,2.5,0],[7.8,2.5,math.pi/2],[7.8,14.7,math.pi],[6.1,14.7,-math.pi/2],[6.1,9.6,0],[6.9,9.6,-math.pi/2]]
route = rC.routeConverter(routeCoordinates)

optimizer = optim.optimizer(env,numBox,route.scheduler(vel),route.route,visualize=True)
optimizer.run(env)