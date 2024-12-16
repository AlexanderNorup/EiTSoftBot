from config import *

import src.operationalControl as OC
import src.simulation as sim
import src.routeConverter as rC
import src.plotter as plot

class optimizer:
    def __init__(self,env,numBox,waypoints,visualize,controlType=0,maxTick=5000):
        self.controlType = controlType
        self.maxTick = maxTick
        self.env = env
        self.maxAcc = 2.
        self.accMultiplier = np.arange(0.4,1.1,0.1)
        self.velocities = np.arange(0.1,1.2,0.1)
        self.grid = []
        self.waypoints = np.asarray(waypoints)-np.asarray(waypoints)[0]
        if controlType:
            route = rC.routeConverterOC(self.waypoints)
            print(route.route)
            self.simulation = sim.simulationOC(self.env,numBox,route,visualize,maxTick)
        else:
            route = rC.routeConverterPID(self.waypoints)
            self.simulation = sim.simulationPID(self.env,numBox,route,visualize,maxTick)

    def stepPID(self,tM,vel):
        
        pid = PID_ControllerClass(dim = 2, k_p = 1., k_d = 3.*1./tM, out_min = -self.maxAcc*tM, out_max = self.maxAcc*tM)
        pid.reset()

        if self.simulation.run(pid,vel):
            return 1
        return 0
    
    def stepPP(self,tM,vel):
        
        PPctrl = OC.operationalSpaceControl(k = [1.,6.], out_min = -self.maxAcc*tM, out_max = self.maxAcc*tM)

        if self.simulation.run(PPctrl,vel):
            return 1
        return 0
    
    def step(self,tM,vel):
        if self.controlType:
            return self.stepPP(tM,vel)
        else:
            return self.stepPID(tM,vel)

    def runBruteForce(self):
        output = []
        runTime = []
        start = time.time()
        for tM in self.accMultiplier:
            for vel in self.velocities:
                if not(self.step(tM,vel)):
                    output.append([tM,vel])
                    runTime.append(self.simulation.timeRun)

        if output:
            print(time.time()-start,min(runTime))
            return output[runTime.index(min(runTime))]
        else :
            return [0,0] 
    
    def cost(self,boxstate):
        if boxstate:
            return self.simulation.timeRun + self.maxTick
        else:
            return self.simulation.timeRun

    def runGridDescent(self):
        start = time.time()
        if self.step(self.accMultiplier[0],self.velocities[0]):
            return [0,0]
        else:
            runTime = self.simulation.timeRun
            output = [self.accMultiplier[0],self.velocities[0]]
            # print(runTime,[0,0])
            cnttM = 0
            cntvel = 0
            while True:
                self.grid.append([cnttM,cntvel])
                try:
                    if self.cost(self.step(self.accMultiplier[cnttM+1],self.velocities[cntvel])) <= runTime:
                        runTime = self.simulation.timeRun
                        try:
                            if self.cost(self.step(self.accMultiplier[cnttM],self.velocities[cntvel+1])) <= runTime:
                                runTime = self.simulation.timeRun
                                output = [self.accMultiplier[cnttM],self.velocities[cntvel+1]]
                                cntvel = cntvel + 1
                                # print(runTime,[cnttM,cntvel])
                            else:
                                output = [self.accMultiplier[cnttM+1],self.velocities[cntvel]]
                                cnttM = cnttM + 1
                                # print(runTime,[cnttM,cntvel])
                        except:
                            output = [self.accMultiplier[cnttM+1],self.velocities[cntvel]]
                            cnttM = cnttM + 1
                            # print(runTime,[cnttM,cntvel])
                    elif self.cost(self.step(self.accMultiplier[cnttM],self.velocities[cntvel+1])) <= runTime:
                        runTime = self.simulation.timeRun
                        output = [self.accMultiplier[cnttM],self.velocities[cntvel+1]]
                        cntvel = cntvel + 1
                        # print(runTime,[cnttM,cntvel])
                    else:
                        break
                except:
                    try: 
                        if self.cost(self.step(self.accMultiplier[cnttM],self.velocities[cntvel+1])) <= runTime:
                            runTime = self.simulation.timeRun
                            output = [self.accMultiplier[cnttM],self.velocities[cntvel+1]]
                            cntvel = cntvel + 1
                            # print(runTime,[cnttM,cntvel])
                        else:
                            break
                    except:
                        break
        print(time.time()-start)
        return output
    
    def runSpecific(self,tM,vel):
        output = self.step(tM,vel)
        plt = plot.plotter(self.env.tick,self.simulation.time)
        # plt.plotTorque(self.simulation.torques)
        plt.plotRoute(self.simulation.posPlot,self.waypoints)
        return [tM,vel]