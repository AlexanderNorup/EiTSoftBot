from config import *

class purePursuitController:
    def __init__(self,k,LD,out_min,out_max,thrs=0.1):
        self.kp = k[0]
        self.kd = k[1]
        self.thrs = thrs
        self.out_min = out_min
        self.out_max = out_max
        self.LD = LD # Lookout distance
        self.tp = 0
        self.v_trgt = 0.
        self.dt = 0.
        self.desVel = np.array([0.,0.])
        self.acc = np.array([0.,0.])
        self.angVel = 0.
        self.prevError = np.array([0.,0.])
        self.prevPos = np.array([0.,0.])

    def trajectory(self,startPos,endPos):
        self.startPos = np.array(startPos)
        self.endPos = np.array(endPos)
        self.a = (endPos[1]-startPos[1])/(endPos[0]-startPos[0])
        self.b = startPos[1]-self.a*startPos[0]

    def calculateLength(self,p1,p2):
        return np.sqrt(np.power(p1[0]-p2[0],2)+np.power(p1[1]-p2[1],2))
    
    def determineY(self,x):
        return self.a*x+self.b

    def maxVel(self,vel):
        if abs(self.angVel) > self.thrs:
            self.v_trgt = maxRv*RpS
        else:
            self.v_trgt = vel*RpS
        
    def calculateWheelVel(self,currentPos,desiredPos):
        descur = desiredPos[:2]-currentPos[:2]
        curprev = currentPos[:2]-self.prevPos
        self.angVel = (np.arctan2(descur[0],descur[1])-np.arctan2(curprev[0],curprev[1]))/(self.dt)
        print("angVel:",self.angVel) 
        self.linVel = np.clip(self.v_trgt-abs(self.angVel), 0, self.v_trgt)
        print("linVel:",self.linVel)
        self.desVel[0] = np.clip((self.linVel + self.angVel), -self.v_trgt, self.v_trgt)
        self.desVel[1] = np.clip((self.linVel - self.angVel), -self.v_trgt, self.v_trgt)
        self.prevPos = currentPos[:2]
        return 

    def determineDiffVel(self,currentPos):
        
        x = currentPos[0]
        y = currentPos[1]

        if self.calculateLength(currentPos,self.endPos) > self.LD:
            A=np.power(self.a,2)+1
            B=2*(self.a*self.b-self.a*y-x)
            C=np.power(y,2)-np.power(self.LD,2)+np.power(x,2)+np.power(self.b,2)-2*self.b*y
            d = np.power(B,2)-4*A*C

            if d < 0:
                self.calculateWheelVel(np.array(currentPos),self.startPos)
                return 
            elif d == 0:
                xe = (-B)/(2*A)
                ye = self.determineY(x)
                self.calculateWheelVel(np.array(currentPos),np.array([xe,ye]))
                return 
            else:
                xp=(-B+np.sqrt(d))/(2*A)
                xm=(-B-np.sqrt(d))/(2*A)
                ym=self.determineY(xm)
                yp=self.determineY(xp)
                if self.calculateLength([xp,yp],self.endPos) > self.calculateLength([xm,ym],self.endPos):
                    self.calculateWheelVel(np.array(currentPos),np.array([xm,ym]))
                    return 
                else:
                    self.calculateWheelVel(np.array(currentPos),np.array([xp,yp]))
                    return 
        else:
            self.calculateWheelVel(np.array(currentPos),self.endPos)
            return

    def update(self,tc,currentPos,qVel,vel): 
        self.dt = max(tc - self.tp,rr)
        self.maxVel(vel)
        
        if self.dt > rr:    
            self.determineDiffVel(currentPos)

            self.acc = np.clip(self.kp*(self.desVel-qVel)+self.kd*((self.desVel-qVel)-self.prevError)*self.dt,self.out_min,self.out_max)
            print("acc:",self.acc,"desVel:",self.desVel,"qvel:",qVel)

            self.tp = tc
            self.prevError = self.desVel-qVel

        for i in range(len(self.acc)):
            if abs(qVel[i]) > self.v_trgt:
                if self.acc[i]>0 and qVel[i]>self.v_trgt:
                    self.acc[i] = 0
                elif self.acc[i]<0 and qVel[i]<self.v_trgt:
                    self.acc[i] = 0

        return self.acc.copy()


        

