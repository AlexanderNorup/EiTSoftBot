from config import *

class purePursuitController:
    def __init__(self,k,LD,out_min,out_max,thrs=0.01) -> None:
        self.kp = k[0]
        self.kd = k[1]
        self.thrs = thrs
        self.out_min = out_min
        self.out_max = out_max
        self.LD = LD # Lookout distance
        self.tp = 0
        self.yawl = 0
        self.yawr = 0
        self.ep = np.array([0,0])
        self.out_val = np.array([0,0])

    def trajectory(self,startPos,endPos):
        self.startPos = startPos
        self.endPos = endPos
        self.a = (endPos[1]-startPos[1])/(endPos[0]-startPos[0])
        self.b = startPos[1]-self.a*startPos[0]
        self.angle = endPos[2]-startPos[2]

    def calculateLength(self,p1,p2):
        return np.sqrt(np.power(p1[0]-p2[0],2)+np.power(p1[1]-p2[1],2))
    
    def determineY(self,x):
        return self.a*x+self.b
    
    def calculateAngle(self,p1,p2):
        return np.arctan2(p2[0]-p1[0],p2[1]-p1[1])

    def determineError(self,currentPos):
        x = currentPos[0]
        y = currentPos[1]

        if self.calculateLength(currentPos,self.endPos) > self.LD:
            A=np.power(self.a,2)+1
            B=2*(self.a*self.b-self.a*y-x)
            C=np.power(y,2)-np.power(self.LD,2)+np.power(x,2)+np.power(self.b,2)-2*self.b*y
            d = np.power(B,2)-4*A*C

            if d < 0:
                theta = self.calculateAngle(currentPos,self.startPos)
                return [self.startPos[0],self.startPos[1],theta]
            elif d == 0:
                xe = (-B)/(2*A)
                ye = self.determineY(x)
                theta = self.calculateAngle(currentPos,[xe,ye])
                return [xe,ye,theta]
            else:
                xp=(-B+np.sqrt(d))/(2*A)
                xm=(-B-np.sqrt(d))/(2*A)
                ym=self.determineY(xm)
                yp=self.determineY(xp)
                if self.calculateLength([xp,yp],self.endPos) > self.calculateLength([xm,ym],self.endPos):
                    theta = self.calculateAngle(currentPos,[xm,ym])
                    return [xm,ym,theta]
                else:
                    theta = self.calculateAngle(currentPos,[xp,yp])
                    return [xp,yp,theta]
        else:
            theta = self.calculateAngle(currentPos,self.endPos)
            return [self.endPos[0],self.endPos[1],theta]

    def update(self,tc,currentPos,qvel,vel): 
        dt = max(tc - self.tp,rr)
        if dt > rr:    
            [x,y,theta] = self.determineError(currentPos)
            print(currentPos,[x,y,theta])
            
            thetal = theta - self.yawl
            thetar = theta - self.yawr

            d=self.LD*RpS
            if abs(theta)>np.pi:
                theta=2*np.pi+theta
            xRot = (theta*L)/(2*r)  
            ec = np.array([d-xRot,d+xRot])
            # R = self.LD/(2*np.sin(theta))
            # ld = ((R-L/2)*2*theta)*RpS
            # rd = ((R+L/2)*2*theta)*RpS
            # ec = np.array([ld,rd])
            ed = ec - self.ep
        
            self.out_val = np.clip(a = self.kp * ec + self.kd * ed/dt, a_min = self.out_min, a_max = self.out_max)

            R = self.LD/(np.sin(theta)*2.)
            self.yawl += self.out_val[0]*dt
            self.yawr += self.out_val[1]*dt

            self.tp = tc
            self.ep = ec

        if abs(abs(self.out_val[0])-abs(self.out_val[1])) > self.thrs:
            v_trgt = maxRv*RpS
        else:
            v_trgt = vel*RpS

        for i in range(len(self.out_val)):
            if abs(qvel[i]) > v_trgt:
                if self.out_val[i]>0 and qvel[i]>v_trgt:
                    self.out_val[i] = 0
                elif self.out_val[i]<0 and qvel[i]<v_trgt:
                    self.out_val[i] = 0
                else:
                    self.out_val[i] = self.out_val[i]

        return self.out_val.copy()


        

