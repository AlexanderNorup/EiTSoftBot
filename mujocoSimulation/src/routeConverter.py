from config import *

class routeConverter:
    def __init__(self,routeLst):
        self.n = 0
        self.route = self.coorToRadians(routeLst)

    def coorToRadians(self,routeLst):
        prvPos = [0,0,0]
        route = np.zeros(shape=((len(routeLst)-1),2))
        leftTotal = 0.
        rightTotal = 0.
        for i,pos in enumerate(routeLst):
            x=pos[0]-prvPos[0]
            y=pos[1]-prvPos[1]
            d=np.sqrt(np.power(x,2)+np.power(y,2))*RpS
            o=(pos[2]-prvPos[2])
            if abs(o)>np.pi:
                o=2*np.pi+o
            o=(o*L)/(2*r)
            if i>0:
                leftTotal=leftTotal+d
                route[(i-1),0]=leftTotal
                leftTotal=leftTotal-o
                route[(i-1),0]=leftTotal
                rightTotal=rightTotal+d
                route[(i-1),1]=rightTotal
                rightTotal=rightTotal+o
                route[(i-1),1]=rightTotal
            prvPos=pos
        return route
    
    def scheduler(self,vel,n):
        return np.array([self.route[n,0],self.route[n,1]]), np.array([vel*RpS,vel*RpS])