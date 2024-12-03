from config import *

class stanleyController:
    def __init__(self,k,out_min,out_max,thrs=0.01) -> None:
        self.k = k
        self.thrs = thrs
        self.out_min = out_min
        self.out_max = out_max
        self.RpS = 16 # 1m/s = 16 Radians/s
        self.maxRv = 0.6 # the maximum experienced rotational velocity [m/s]

    def trajectory(self,startPos,endPos):
        self.startPos = startPos
        self.endPos = endPos
        self.a = (endPos[1]-startPos[1])/(endPos[0]-startPos[0])
        self.b = startPos[1]-self.a*startPos[0]
        self.angle = endPos[2]-startPos[2]

    def closestPointError(self,currentPos):
        x1 = currentPos[0]
        y1 = currentPos[1]
        x2 = (y1-self.b)/self.a
        y2 = self.a*x1+self.b
        x = (x1+x2)/2
        y = (y1+y2)/2

        x=self.endPos[0]
        y=self.endPos[1]

        return np.sqrt(np.power(x1-x,2)+np.power(y1-y,2))
    
    def yawError(self,currentPos):
        yaw = self.angle-currentPos[2]
        if abs(yaw)>np.pi:
            yaw=2*np.pi+yaw
        return yaw

    def update(self,env,currentPos,qvel,vel):
        currentVel = env.get_sensor_value("velo")[0]
        e = self.closestPointError(currentPos)
        Theta = self.yawError(currentPos)
        wheelTheta = np.array([Theta,-Theta])
        print(e,wheelTheta)
        delta = wheelTheta + np.arctan(self.k*e/(currentVel))
        print(delta)
        out_val = np.clip(
                    a     = self.k * delta,
                    a_min = self.out_min,
                    a_max = self.out_max)
        
        if abs(abs(delta[0])-abs(delta[1])) > self.thrs:
            v_trgt = np.array([self.maxRv*self.RpS,self.maxRv*self.RpS])
        else:
            v_trgt = np.array([vel*self.RpS,vel*self.RpS])

        for i in range(len(delta)):
            if abs(qvel[i]) > v_trgt[i]:
                if out_val[i]>0 and qvel[i]>0:
                    out_val[i] = -out_val[i]
                elif out_val[i]<0 and qvel[i]<0:
                    out_val[i] = -out_val[i]
                else:
                    out_val[i] = out_val[i]

        print(out_val)

        return out_val.copy()


        

