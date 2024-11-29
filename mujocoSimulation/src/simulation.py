from config import *


class simulation:
    def __init__(self,env,numBox,route,visualize=False,maxTick=50000):
        
        self.visualize = visualize
        self.maxTick = maxTick
        self.thrs = 0.1
        self.thrsBox = 0.1
        self.numbox = numBox
        self.route = route
        self.env = env
        self.timeRun = 0
    
    def reset(self):
        self.time = np.zeros(shape=(self.maxTick))
        self.v_trgt = np.array([0,0])
        self.q_trgt = np.array([0,0])
        self.qpostrgt = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.qveltrgt = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.qpos = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.qvel = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.torques = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.boxes = []
        for i in range(self.numbox):
            self.boxes.append("box" + str(i))
        self.boxz = np.zeros(shape=(self.maxTick,self.numbox))
        self.v_trgt = np.array([0,0])
        self.q_trgt = np.array([0,0])
        self.n = 0

        self.env.reset(step=True)
        if self.visualize:
            self.env.init_viewer(distance=3.0,lookat=[0,0,0])
    
    def show(self,tick=20):
        if self.env.loop_every(tick_every=tick):
            self.env.render()
    
    def closeSim(self):
        if self.visualize:
            self.env.close_viewer()

    def step(self,pid,vel):
        
        qpos = self.env.data.qpos[self.env.ctrl_qpos_idxs]
        qvel = self.env.data.qvel[self.env.ctrl_qvel_idxs]
        
        # Change PID target
        if abs(self.q_trgt[0]-qpos[0])<self.thrs and abs(self.q_trgt[1]-qpos[1])<self.thrs: #and abs(qvel[0])<self.thrs and abs(qvel[1])<self.thrs: 
            try:
                self.q_trgt,self.v_trgt = self.route.scheduler(vel,self.n)
            except:
                print("end point reached")
            self.n = self.n + 1
        
        # PID controller
        pid.update(x_trgt=self.q_trgt,t_curr=self.env.get_sim_time(),x_curr=qpos,v_trgt=self.v_trgt,v_curr=qvel,VERBOSE=False)
        
        # Update
        torque = pid.out()
        self.env.step(ctrl=torque) # update

        # Append
        self.time[self.env.tick-1] = self.env.get_sim_time()
        self.qpostrgt[self.env.tick-1,:] = pid.x_trgt
        self.qveltrgt[self.env.tick-1,:] = self.v_trgt
        self.qpos[self.env.tick-1,:] = qpos
        self.qvel[self.env.tick-1,:] = qvel
        self.torques[self.env.tick-1,:] = torque
        for i in range(self.numbox):
            self.boxz[self.env.tick-1,i] = self.env.get_p_body(self.boxes[i])[2]
        
        if self.visualize:
            self.show()

        for i in range(self.numbox):
            if abs(self.boxz[0,i]-self.boxz[self.env.tick-1,i])>self.thrsBox:
                return 1
        return 0
    
    def run(self,pid,vel):

        self.reset()

        while (self.env.tick < self.maxTick):
            if self.step(pid,vel):
                self.closeSim()
                return 1
            elif self.n > len(self.route.route):
                self.timeRun = self.env.tick
                self.closeSim()
                return 0
        self.closeSim()
        return 1