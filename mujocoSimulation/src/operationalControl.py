from config import *

class operationalSpaceControl:
    def __init__(self,k,out_min,out_max,thrs=0.1):
        self.kp = k[0]
        self.kd = k[1]
        self.thrs = thrs
        self.out_min = out_min
        self.out_max = out_max
        self.acc = np.array([0.,0.,0.])

        self.tp = 0.
        self.prvErr = np.array([0.,0.,0.])
        self.err = np.zeros(3)
        self.lam = 0.
    
    def jtToOpVel(self,vel):
        x = r/2*(vel[1]+vel[0])*np.cos(self.pos[2])
        y = r/2*(vel[1]+vel[0])*np.sin(self.pos[2])
        theta = r/L*(vel[1]-vel[0])
        return np.array([x,y,theta])

    def opTojtAcc(self):
        self.linear = np.clip(np.sign(self.acc[0]+self.acc[1])*self.out_max, self.out_min, self.out_max)
        wL = np.clip((self.linear - ((L/2)*self.acc[2])/r), self.out_min, self.out_max)
        wR = np.clip((self.linear + ((L/2)*self.acc[2])/r), self.out_min, self.out_max)
        return np.array([wL,wR])
    
    def targetVel(self,vel):
        if abs(abs(self.qVel[0])-abs(self.qVel[1])) > self.thrs*10.:
            self.trgtqVel = np.array([maxRv*RpS,maxRv*RpS])
        else:
            self.trgtqVel = vel*RpS

    def update(self,tc,prvTrgt,trgtPos,pos,vel,qVel):

        self.qVel = qVel
        self.pos = pos
        self.trgtPos = trgtPos
        self.targetVel(vel)

        self.dt = max(tc - self.tp,rr)
        
        if self.dt > rr:

            curVel = self.jtToOpVel(self.qVel)
            errDiff = [0.,0.,0.] - curVel

            pPP = pos-trgtPos
            ppPP = prvTrgt-trgtPos
            self.lam=normAngle(np.arctan2(ppPP[1]*pPP[0]-ppPP[0]*pPP[1],pPP[0]*ppPP[0]+pPP[1]*ppPP[1])) 

            if np.any(np.abs(prvTrgt[:2]-trgtPos[:2])>self.thrs*0.1):
                if np.linalg.norm(pos[:2]-prvTrgt[:2])>self.thrs and np.linalg.norm(pos[:2]-trgtPos[:2])>self.thrs:
                    pos[2] += self.lam
                    pos[2] = normAngle(pos[2])
            
            
            self.err[:2] = np.abs(self.trgtPos)[:2] - np.abs(self.pos)[:2]
            self.err[2] = normAngle(self.trgtPos[2]-self.pos[2])

            self.acc  = self.kp * self.err + self.kd * errDiff
            self.tp = tc

    def out(self):
        accJoint = self.opTojtAcc()

        for i in range(len(self.qVel)):
            if abs(self.qVel[i]) > abs(self.trgtqVel[i]) :
                if accJoint[i]>0 and self.qVel[i]>self.trgtqVel[i]:
                    accJoint[i] = 0.
                elif accJoint[i]<0 and self.qVel[i]<self.trgtqVel[i]:
                    accJoint[i] = 0.
        
        return accJoint