from config import *

class plotter:
    def __init__(self,env,time):
        self.time = time
        self.env = env
        
    def plotJointPos(self,qpos,trgtqpos):
        fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("Joint Position", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.env.tick],qpos[:self.env.tick,idxa],
                    '-',color='k',label='Current position')
            ax.plot(self.time[:self.env.tick],trgtqpos[:self.env.tick,idxa],
                    '--',color='b',label='Target position')
            ax.set_title('Joint [%d]'%(idxa),fontsize=8)
            if idxa == 0: ax.legend(fontsize=8)
        plt.show()

    def plotJointVel(self,qvel,trgtqvel):
        fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("Joint Velocity", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.env.tick],qvel[:self.env.tick,idxa],
                    '-',color='k',label='Current velocity')
            ax.plot(self.time[:self.env.tick],trgtqvel[:self.env.tick,idxa],
                    '--',color='r',label='Target position')
            ax.set_title('Joint [%d]'%(idxa),fontsize=8)
            if idxa == 0: ax.legend(fontsize=8)
        plt.show()

    def plotTorque(self,torques):
        fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("Joint Control", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.env.tick],torques[:self.env.tick,idxa],color='r')
            ax.set_title('Joint [%d]'%(idxa),fontsize=8)
        plt.show()


    def plotBoxPos(self,boxz):
        fig,axs = plt.subplots(nrows=1,ncols=boxz.shape[1],sharex=False,sharey=False,figsize=(11,3))
        fig.subplots_adjust(hspace=0.4)
        fig.suptitle("box position", fontsize=10)
        for idxa,ax in enumerate(axs.ravel()):
            ax.plot(self.time[:self.env.tick],boxz[:self.env.tick,idxa],color='b')
            ax.set_title('Box %d'%(idxa+1),fontsize=8)
        plt.show()