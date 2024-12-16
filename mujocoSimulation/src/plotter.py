from config import *

class plotter:
    def __init__(self,tick,time):
        self.time = time
        self.tick = tick
        
    def plotJointPos(self,qpos,trgtqpos):
        fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("Joint Position", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.tick],qpos[:self.tick,idxa],
                    '-',color='k',label='Current position')
            ax.plot(self.time[:self.tick],trgtqpos[:self.tick,idxa],
                    '--',color='b',label='Target position')
            ax.set_title('Joint [%d]'%(idxa),fontsize=8)
            if idxa == 0: ax.legend(fontsize=8)
        plt.show()

    def plotJointVel(self,qvel,trgtqvel):
        fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("Joint Velocity", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.tick],qvel[:self.tick,idxa],
                    '-',color='k',label='Current velocity')
            ax.plot(self.time[:self.tick],trgtqvel[:self.tick,idxa],
                    '--',color='r',label='Target position')
            ax.set_title('Joint [%d]'%(idxa),fontsize=8)
            if idxa == 0: ax.legend(fontsize=8)
        plt.show()

    def plotTorque(self,torques):
        fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("Joint Control", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.tick],torques[:self.tick,idxa],color='r')
            ax.set_title('Joint [%d]'%(idxa),fontsize=8)
        plt.show()


    def plotBoxPos(self,boxz):
        fig,axs = plt.subplots(nrows=1,ncols=boxz.shape[1],sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("box position", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.tick],boxz[:self.tick,idxa],color='b')
            ax.set_title('Box %d'%(idxa+1),fontsize=8)
        plt.show()

    def plotRoute(self,actualPath,desiredPath):
        actualPath = np.array(actualPath)
        desiredPath = np.array(desiredPath)
        f = open("../testData/pathPIDmin.csv", "w")
        f.write("i,x,y,theta")
        f.write("\n")
        for i,dat in enumerate(actualPath):
            f.write(str(i)+",")
            f.write(str(dat[0]+6.0)+",")
            f.write(str(dat[1]+2.5)+",")
            f.write(str(dat[2])+",")
            f.write("\n")
        f = open("../testData/desired.csv", "w")
        f.write("i,x,y,theta")
        f.write("\n")
        for i,dat in enumerate(desiredPath):
            f.write(str(i)+",")
            f.write(str(dat[0]+6.0)+",")
            f.write(str(dat[1]+2.5)+",")
            f.write(str(dat[2])+",")
            f.write("\n")
        plt.plot(actualPath[:,0],actualPath[:,1])
        plt.plot(desiredPath[:,0],desiredPath[:,1])
        plt.plot(desiredPath[:,0],desiredPath[:,1],".")
        plt.show()
        plt.plot(actualPath[:,0],actualPath[:,2],desiredPath[:,0],desiredPath[:,2])
        plt.show()