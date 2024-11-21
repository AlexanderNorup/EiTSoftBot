from config import *


class simulation:
    def __init__(self,env,numBox,visualize=False,maxTick=100000):
        
        self.cnt = 0
        self.visualize = visualize
        self.maxTick = maxTick
        self.time = np.zeros(shape=(maxTick))
        self.qpostrgt = np.zeros(shape=(maxTick,env.n_ctrl))
        self.qveltrgt = np.zeros(shape=(maxTick,env.n_ctrl))
        self.qpos = np.zeros(shape=(maxTick,env.n_ctrl))
        self.qvel = np.zeros(shape=(maxTick,env.n_ctrl))
        self.torques = np.zeros(shape=(maxTick,env.n_ctrl))
        self.numbox = numBox
        self.boxes = []
        for i in range(numBox):
            self.boxes.append("box" + str(i+1))
        self.boxz = np.zeros(shape=(maxTick,numBox))
        self.v_trgt = np.array([0,0])
        self.q_trgt = np.array([0,0])
        self.thrs = 0.1
        self.thrsBox = 0.1
    
    def show(self,env):
        if env.loop_every(tick_every=20):
            env.render()

    def step(self,env,scheduler,jointRoute,pid):
        
        qpos = env.data.qpos[env.ctrl_qpos_idxs]
        qvel = env.data.qvel[env.ctrl_qvel_idxs]
        
        # Change PID target
        if abs(self.q_trgt[0]-qpos[0])<self.thrs and abs(self.q_trgt[1]-qpos[1])<self.thrs and abs(qvel[0])<self.thrs and abs(qvel[1])<self.thrs: 
            self.q_trgt,self.v_trgt = scheduler(jointRoute,self.cnt,1.1)
            self.cnt = self.cnt+1
        
        # PID controller
        pid.update(x_trgt=self.q_trgt,t_curr=env.get_sim_time(),x_curr=qpos,v_trgt=self.v_trgt,v_curr=qvel,VERBOSE=False)
        
        # Update
        torque = pid.out()
        env.step(ctrl=torque) # update

        # Append
        self.time[self.env.tick-1] = env.get_sim_time()
        self.qpostrgt[self.env.tick-1,:] = pid.x_trgt
        self.qveltrgt[self.env.tick-1,:] = self.v_trgt
        self.qpos[self.env.tick-1,:] = qpos
        self.qvel[self.env.tick-1,:] = qvel
        self.torques[self.env.tick-1,:] = torque
        for i in range(self.numbox):
            self.boxz[self.env.tick-1,i] = env.get_p_body(self.boxes[i])[2]
        
        if self.visualize:
            self.show()

        for i in range(self.numbox):
            if abs(self.boxz[0,i]-self.boxz[self.env.tick-1,i])>self.thrsBox:
                return 1
        return 0
    
    def run(self,env,pid,scheduler,jointRoute):
        
        self.v_trgt = np.array([0,0])
        self.q_trgt = np.array([0,0])

        while (env.tick < self.maxTick) and self.cnt<len(jointRoute):
            if self.step(env,scheduler,jointRoute,pid):
                return 1
        return 0