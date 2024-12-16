from config import *

class routeConverterPID:
    def __init__(self,routeLst):
        self.n = 0
        self.thrs = 1e-6
        self.route = self.coorToRadians(routeLst)

    def coorToRadians(self,routeLst):
        route = []
        leftTotal = 0.
        rightTotal = 0.
        for i,pos in enumerate(routeLst):
            try:
                x=pos[0]-prvPos[0]
                y=pos[1]-prvPos[1]
                sec=np.sqrt(np.power(x,2)+np.power(y,2))*RpS
                o=normAngle(pos[2]-prvPos[2])
                thi=(o*L)/(2*r)
            except:
                sec = 0.0
                thi = 0.0
            try:
                nxtPos = routeLst[i+1]
                pPP = prvPos-pos
                nPP = nxtPos-pos
                fir=normAngle(np.arctan2(nPP[1]*pPP[0]-nPP[0]*pPP[1],nPP[0]*pPP[0]+nPP[1]*pPP[1])+np.pi-o)
                pos[2] = normAngle(pos[2]+fir)
                fir=(fir*L)/(2*r)
            except:
                fir = 0.0
            if i>0:
                if abs(sec) > self.thrs:
                    leftTotal=leftTotal+sec
                    rightTotal=rightTotal+sec
                    route.append([leftTotal,rightTotal,0])
                if abs(thi) > self.thrs:
                    leftTotal=leftTotal-thi
                    rightTotal=rightTotal+thi
                    route.append([leftTotal,rightTotal,1])
                if abs(fir) > self.thrs:
                    leftTotal=leftTotal-fir
                    rightTotal=rightTotal+fir
                    route.append([leftTotal,rightTotal,1])
            prvPos = pos.copy()
        return np.array(route)
    
    def scheduler(self,vel,n):
        if self.route[n,2]==0:
            return np.array([self.route[n,0],self.route[n,1]]), np.array([vel*RpS,vel*RpS])
        else:
            return np.array([self.route[n,0],self.route[n,1]]), np.array([maxRv*RpS,maxRv*RpS])
        
class routeConverterOC:
    def __init__(self,routeLst):
        self.n = 0
        self.thrs = 1e-6
        self.route = self.coorToWorld(routeLst)

    def coorToWorld(self,routeLst):
        route = []
        worldAngle = 0.0
        worldAngleEnd = 0.0
        prvPos=np.array([0.,0.,0.])
        prvprvPos=np.array([0.,0.,0.])
        for i,pos in enumerate(routeLst):
            if i > 1:
                pPP = pos-prvPos
                ppPP = prvprvPos-prvPos
                lam=normAngle(np.arctan2(pPP[1]*ppPP[0]-pPP[0]*ppPP[1],pPP[0]*ppPP[0]+pPP[1]*ppPP[1])+np.pi+prvPos[2]-theta) 
            else:
                lam = prvPos[2]
            x=pos[0]
            y=pos[1]
            theta=pos[2]
            if lam != theta:
                route.append([x,y,lam,1])
            route.append([x,y,theta,0])
            prvprvPos = prvPos.copy()
            prvPos = pos.copy()
        return np.array(route)
    
    def scheduler(self,n):
        return np.array([self.route[n,0],self.route[n,1],self.route[n,2]])