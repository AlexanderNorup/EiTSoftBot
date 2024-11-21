from config import *
import src.simulation as sim

class optimizer:
    def __init__(self,simulation,vel):
        self.bigCnt = 0
        self.torqueMultiplier = np.arange(1.,0.3,-0.1)
        self.sim = simulation
        self.vel = vel

    def step(self,env,tM):
        
        pid = PID_ControllerClass(dim = 2, k_p = 1., k_d = 1.5*1./tM, out_min = -1.2*tM, out_max = 1.2*tM)

        env.reset(step=True)
        env.init_viewer(distance=3.0,lookat=[0,0,0])
        pid.reset()

        if self.sim.run(pid,self.vel):
            return 1
        
        return 0

    
    def run(self,env):
        
        for tM in self.torqueMultiplier:
            if not(self.step(env,tM)):
                return 1
            env.close_viewer() 
            self.bigCnt = self.bigCnt + 1