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
        self.maxAcc = 1.
        self.accMultiplier = np.arange(1.,0.3,-0.1)
        self.velocities = np.arange(1.1,0.,-0.1)
        self.grid = []
        self.waypoints = np.asarray(waypoints)-np.asarray(waypoints)[0]
        if controlType:
            self.simulation = sim.simulationOC(self.env,numBox,self.waypoints,visualize,maxTick)
        else:
            route = rC.routeConverter(self.waypoints)
            self.simulation = sim.simulationPID(self.env,numBox,route,visualize,maxTick)

    def stepPID(self,tM,vel):
        
        pid = PID_ControllerClass(dim = 2, k_p = 1., k_d = 2.*1./tM, out_min = -self.maxAcc*tM, out_max = self.maxAcc*tM)
        pid.reset()

        if self.simulation.run(pid,vel):
            return 1
        return 0
    
    def stepPP(self,tM,vel):
        
        PPctrl = OC.operationalSpaceControl(k = [1.,1.*1./tM], out_min = -self.maxAcc*tM, out_max = self.maxAcc*tM)

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
        for tM in self.accMultiplier:
            for vel in self.velocities:
                if not(self.step(tM,vel)):
                    output.append([tM,vel])
                    runTime.append(self.simulation.timeRun)
                    if vel == self.velocities[0]:
                        if output:
                            return output[runTime.index(min(runTime))]
                        else :
                            return [0,0]
                    break
        return [0,0]
    
    def cost(self,boxstate):
        if boxstate:
            return self.simulation.timeRun + self.maxTick
        else:
            return self.simulation.timeRun

    def runGridDescent(self):
        tM = np.flip(self.accMultiplier)
        vel = np.flip(self.velocities)
        if self.step(tM[0],vel[0]):
            return [0,0]
        else:
            runTime = self.simulation.timeRun
            output = [tM[0],vel[0]]
            cnttM = 0
            cntvel = 0
            while True:
                self.grid.append([cnttM,cntvel])
                try:
                    if self.cost(self.step(tM[cnttM+1],vel[cntvel])) < runTime:
                        runTime = self.simulation.timeRun
                        try:
                            if self.cost(self.step(tM[cnttM],vel[cntvel+1])) < runTime:
                                runTime = self.simulation.timeRun
                                output = [tM[cnttM],vel[cntvel+1]]
                                cntvel = cntvel + 1
                            else:
                                output = [tM[cnttM+1],vel[cntvel]]
                                cnttM = cnttM + 1
                        except:
                            output = [tM[cnttM+1],vel[cntvel]]
                            cnttM = cnttM + 1
                    elif self.cost(self.step(tM[cnttM],vel[cntvel+1])) < runTime:
                        runTime = self.simulation.timeRun
                        output = [tM[cnttM],vel[cntvel+1]]
                        cntvel = cntvel + 1
                    else:
                        break
                except:
                    try: 
                        if self.cost(self.step(tM[cnttM],vel[cntvel+1])) < runTime:
                            runTime = self.simulation.timeRun
                            output = [tM[cnttM],vel[cntvel+1]]
                            cntvel = cntvel + 1
                        else:
                            break
                    except:
                        break
        return output
    
    def runSpecific(self,tM,vel):
        output = self.step(tM,vel)
        plt = plot.plotter(self.env.tick,self.simulation.time)
        # plt.plotTorque(self.simulation.torques)
        plt.plotRoute(self.simulation.posPlot,self.waypoints)
        return [tM,vel]