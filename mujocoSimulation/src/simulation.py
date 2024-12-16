from config import *


class simulationPID:
    def __init__(self,env,numBox,route,visualize=False,maxTick=5000):
        self.visualize = visualize
        self.maxTick = maxTick
        self.thrs = 0.1
        self.thrsBox = 0.1
        self.numbox = numBox
        self.route = route
        self.env = env
        self.posPlot = []
        self.timeRun = 0
    
    def reset(self):
        self.time = np.zeros(shape=(self.maxTick))
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
            self.env.init_viewer()
    
    def show(self,tick=20):
        if self.env.loop_every(tick_every=tick):
            # Update the camera to always look at the mir
            mir200_pos = self.env.get_x_y_yaw_body("mir200")
            self.env.viewer.cam.lookat = [mir200_pos[0], mir200_pos[1], 0.6]
            # Render the scene
            self.env.render()
    
    def closeSim(self):
        if self.visualize:
            self.env.close_viewer()

    def step(self,pid,vel):
        
        self.posPlot.append(self.env.get_x_y_yaw_body("mir200"))
        qpos = self.env.data.qpos[self.env.ctrl_qpos_idxs]
        qvel = self.env.data.qvel[self.env.ctrl_qvel_idxs]
        
        # Change PID target
        if abs(self.q_trgt[0]-qpos[0])<self.thrs and abs(self.q_trgt[1]-qpos[1])<self.thrs and abs(qvel[0])<self.thrs and abs(qvel[1])<self.thrs: 
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

        start = time.time()

        while (self.env.tick < self.maxTick):
            if self.step(pid,vel):
                print(time.time()-start,self.env.tick)
                self.closeSim()
                return 1
            elif self.n > len(self.route.route):
                print(time.time()-start,self.env.tick)
                self.timeRun = self.env.tick
                self.closeSim()
                return 0
        print(time.time()-start,self.env.tick)
        self.closeSim()
        return 1
    

class simulationOC:
    def __init__(self,env,numBox,route,visualize=False,maxTick=5000):     
        self.visualize = visualize
        self.maxTick = maxTick
        self.thrs = 0.1
        self.thrsBox = 0.1
        self.numbox = numBox
        self.route = route
        self.posPlot = []
        self.env = env
        self.timeRun = 0
    
    def reset(self):
        self.time = np.zeros(shape=(self.maxTick))
        self.postrgt = np.zeros(shape=(self.maxTick,3))
        self.qveltrgt = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.pos = np.zeros(shape=(self.maxTick,3))
        self.qvel = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.torques = np.zeros(shape=(self.maxTick,self.env.n_ctrl))
        self.boxes = []
        for i in range(self.numbox):
            self.boxes.append("box" + str(i))
        self.boxz = np.zeros(shape=(self.maxTick,self.numbox))
        self.trgtVel = np.array([0.,0.])
        self.trgtPos = np.array([0.,0.,0.])
        self.prvTrgt = np.array([0.,0.,0.])
        self.n = 1

        self.env.reset(step=True)
        if self.visualize:
            self.env.init_viewer()
    
    def show(self,tick=20):
        if self.env.loop_every(tick_every=tick):
            # Update the camera to always look at the mir
            mir200_pos = self.env.get_x_y_yaw_body("mir200")
            self.env.viewer.cam.lookat = [mir200_pos[0], mir200_pos[1], 0.6]
            # Render the scene
            self.env.render()
    
    def closeSim(self):
        if self.visualize:
            self.env.close_viewer()

    def step(self,OC):
        
        currentPos = np.array(self.env.get_x_y_yaw_body("mir200"))
        self.posPlot.append(currentPos)
        qvel = self.env.data.qvel[self.env.ctrl_qvel_idxs]
        
        # Change target
        if abs(self.trgtPos[0]-currentPos[0])<self.thrs and abs(self.trgtPos[1]-currentPos[1])<self.thrs and (self.trgtPos[2]-currentPos[2])<self.thrs*0.1 and abs(qvel[0])<self.thrs and abs(qvel[1])<self.thrs: 
            try:
                self.trgtPos = self.route.scheduler(self.n)
                self.prvTrgt = self.route.scheduler(self.n-1)
            except:
                print("end point reached")
            self.n = self.n + 1
            print(self.n)
        
        OC.update(self.env.get_sim_time(),self.prvTrgt,self.trgtPos,currentPos,self.trgtVel,qvel)

        # Update
        torque = OC.out()
        self.env.step(ctrl=torque) # update

        # Append
        self.time[self.env.tick-1] = self.env.get_sim_time()
        self.postrgt[self.env.tick-1,:] = self.trgtPos
        self.qveltrgt[self.env.tick-1,:] = self.trgtVel
        self.pos[self.env.tick-1,:] = currentPos
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
    
    def run(self,OC,vel):

        self.reset()
        self.trgtVel = np.array([vel,vel])

        while (self.env.tick < self.maxTick):
            if self.step(OC):
                self.closeSim()
                return 1
            elif self.n > len(self.route.route):
                self.timeRun = self.env.tick
                self.closeSim()
                return 0
        self.closeSim()
        return 1