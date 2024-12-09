from config import *

class operationalSpaceControl:
    def __init__(self,k,out_min,out_max,thrs=0.1):
        self.kp = k[0]
        self.kd = k[1]
        self.thrs = thrs
        self.out_min = out_min
        self.out_max = out_max
        self.acc = np.array([0.,0.,0.])

        self.prvAcc = np.array([0.,0.,0.])
        self.tp = 0.
        self.prvErr = np.array([0.,0.,0.])
        self.prvPos = np.array([0.,0.,0.])
    
    def jtToOpVel(self,vel):
        x = r/2*(vel[1]+vel[0])*np.cos(self.pos[2])
        y = r/2*(vel[1]+vel[0])*np.sin(self.pos[2])
        theta = r/L*(vel[1]-vel[0])
        return np.array([x,y,theta])

    def opTojtAcc(self):
        wL = (np.linalg.norm(self.acc[:2]) - (L/2)*self.acc[2])/r
        wR = (np.linalg.norm(self.acc[:2]) + (L/2)*self.acc[2])/r
        return np.array([wL,wR])
    
    def targetVel(self,vel):
        if abs(self.qVel[0])-abs(self.qVel[1]) > self.thrs:
            self.trgtqVel = np.array([maxRv*RpS,maxRv*RpS])
        else:
            self.trgtqVel = vel*RpS

    def update(self,tc,trgtPos,pos,vel,qVel):
        self.trgtPos = trgtPos
        self.pos = pos
        self.qVel = qVel

        self.targetVel(vel)

        self.dt       = max(tc - self.tp,rr)
        err = trgtPos - pos     
        errDiff = self.jtToOpVel(self.trgtqVel) - self.jtToOpVel(qVel)
        
        if self.dt > rr:
            self.acc  = np.clip(self.kp * err - self.kd * errDiff, self.out_min, self.out_max)
            self.prvAcc = self.acc
            self.tp = tc
            self.prvErr = err
            self.prvPos = pos

    def out(self):
        accJoint = self.opTojtAcc()


        for i in range(len(self.qVel)):
            if abs(self.qVel[i]) > abs(self.trgtqVel[i]) :
                if accJoint[i]>0 and self.qVel[i]>self.trgtqVel[i]:
                    accJoint[i] = 0
                elif accJoint[i]<0 and self.qVel[i]<self.trgtqVel[i]:
                    accJoint[i] = 0
        print(accJoint,self.acc)
        return accJoint