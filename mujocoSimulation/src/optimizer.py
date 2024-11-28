from config import *

class optimizer:
    def __init__(self,simulation):
        self.bigCnt = 0
        self.torqueMultiplier = np.arange(1.,0.3,-0.1)
        self.velocities = np.arange(1.1,0.,-0.1)
        self.sim = simulation
        self.output = 0
        self.time = 0

    def step(self,tM,vel):
        
        pid = PID_ControllerClass(dim = 2, k_p = 1., k_d = 1.5*1./tM, out_min = -1.2*tM, out_max = 1.2*tM)
        pid.reset()

        if self.sim.run(pid,vel):
            return 1
        self.output = [tM,vel]
        self.time = self.sim.timeRun
        return 0
    


    def run(self):
        for tM in self.torqueMultiplier:
            if not(self.step(tM,self.velocities[0])):
                return self.output
            self.bigCnt = self.bigCnt + 1
        return 0