from config import *

import src.stanleyControl as SC

class optimizer:
    def __init__(self,simulation,controlType=0):
        self.controlType = controlType
        self.torqueMultiplier = np.arange(1.,0.3,-0.1)
        self.velocities = np.arange(1.1,0.,-0.1)
        self.sim = simulation
        self.output = []
        self.time = []

    def stepPID(self,tM,vel):
        
        pid = PID_ControllerClass(dim = 2, k_p = 1., k_d = 1.5*1./tM, out_min = -1.3*tM, out_max = 1.3*tM)
        pid.reset()

        if self.sim.run(pid,vel):
            return 1
        return 0
    
    def stepStanley(self,tM,vel):
        
        stanley = SC.stanleyController(k = 1., out_min = -1.3*tM, out_max = 1.3*tM)

        if self.sim.run(stanley,vel):
            return 1
        return 0
    
    def step(self,tM,vel):
        if self.controlType:
            return self.stepStanley(tM,vel)
        else:
            return self.stepPID(tM,vel)

    def run(self):
        for tM in self.torqueMultiplier:
            for vel in self.velocities:
                print(tM,vel)
                if not(self.step(tM,vel)):
                    self.output.append([tM,vel])
                    self.time.append(self.sim.timeRun)
                    if vel == self.velocities[0]:
                        if self.output:
                            return self.output[self.time.index(min(self.time))]
                        else :
                            return [0,0]
                    break
        return [0,0]
    
    def runGradientDescent(self):
        pass
    
    def runSpecific(self,tM,vel):
        self.step(tM,vel)