from config import *

class routeConverter:
    def __init__(self,routeLst):
        self.n = 0
        self.route = self.coorToRadians(routeLst)
        self.RpS = 16 # 1m/s = 16 Radians/s
        self.maxRv = 0.6 # the maximum experienced rotational velocity [m/s]

    def coorToRadians(self,routeLst):
        prvPos = [0,0,0]
        route = np.zeros(shape=((len(routeLst)-1)*2,2))
        distToRad = 16
        leftTotal = 0.
        rightTotal = 0.
        for i,pos in enumerate(routeLst):
            x=pos[0]-prvPos[0]
            y=pos[1]-prvPos[1]
            d=math.sqrt(math.pow(x,2)+math.pow(y,2))*distToRad
            o=(pos[2]-prvPos[2])
            if abs(o)>math.pi:
                o=2*math.pi+o
            o=o*4
            if i>0:
                leftTotal=leftTotal+d
                route[(i-1)*2,0]=leftTotal
                leftTotal=leftTotal-o
                route[(i-1)*2+1,0]=leftTotal
                rightTotal=rightTotal+d
                route[(i-1)*2,1]=rightTotal
                rightTotal=rightTotal+o
                route[(i-1)*2+1,1]=rightTotal
            prvPos=pos
        return route
    
    def scheduler(self,vel):
        if self.n%2==0:
            return np.array([self.route[self.n,0],self.route[self.n,1]]), np.array([vel*self.RpS,vel*self.RpS])
        else:
            return np.array([self.route[self.n,0],self.route[self.n,1]]), np.array([self.maxRv*self.RpS,self.maxRv*self.RpS])