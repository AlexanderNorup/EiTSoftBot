import mujoco
import mediapy as media
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import itertools
import math

sys.path.append('helper/')
sys.path.append('mujoco_usage/')
from mujoco_parser import *
from slider import *
from utility import *

from src.boxesXmlWriter import *

boxesReceived = [[["-0.326","-0.158","0.452"],[".0525",".0625",".0925"],".063"]]
writeBoxes(boxesReceived,0.035)

xml_path = "xmlFiles/mobile_platform.xml"

env = MuJoCoParserClass(name='mir200',rel_xml_path=xml_path,verbose=True)

env.model.geom('floor').priority = 1 # 0=>1
print ("Floor priority:%s"%(env.model.geom('floor').priority))

def route(lst):
    prvPos = [0,0,0]
    route = np.zeros(shape=((len(lst)-1)*2,2))
    distToRad = 16
    leftTotal = 0.
    rightTotal = 0.
    for i,pos in enumerate(lst):
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

coordinates = [[6.,2.5,0],[6.9,2.5,0],[7.8,2.5,math.pi/2],[7.8,14.7,math.pi],[6.1,14.7,-math.pi/2],[6.1,9.6,0],[6.9,9.6,-math.pi/2]]
jointRoute = route(coordinates)

def scheduler(route,n,vel):
    if n%2==0:
        return np.array([route[n,0],route[n,1]]), np.array([vel*16,vel*16])
    else:
        return np.array([route[n,0],route[n,1]]), np.array([9.6,9.6])

# Buffer
max_tick    = 1000000
t_list      = np.zeros(shape=(max_tick))
x_trgt_list = np.zeros(shape=(max_tick,env.n_ctrl))
v_trgt_list = np.zeros(shape=(max_tick,env.n_ctrl))
qpos_list   = np.zeros(shape=(max_tick,env.n_ctrl))
qvel_list   = np.zeros(shape=(max_tick,env.n_ctrl))
torque_list = np.zeros(shape=(max_tick,env.n_ctrl))
numbox = len(boxesReceived)
boxes = []
for i in range(numbox):
    boxes.append("box" + str(i))
boxz = np.zeros(shape=(max_tick,len(boxes)))

cnt = 0
bigCnt = 0
torqueMultiplier = np.arange(1.,0.3,-0.1)

while cnt < len(jointRoute)-1:
    # Loop
    pid = PID_ControllerClass(dim = 2, k_p = 1., k_d = 1.5*1./torqueMultiplier[bigCnt], out_min = -1.2*torqueMultiplier[bigCnt], out_max = 1.2*torqueMultiplier[bigCnt])

    env.reset(step=True)
    env.init_viewer(distance=3.0,lookat=[0,0,0])
    pid.reset()
    cnt = 0
    thrs = 0.1
    thrsBox = 0.1
    v_trgt = np.array([0,0])
    q_trgt = np.array([0,0])
    vel = np.zeros(shape=(len(coordinates),1))
    for i in vel.shape[0]:
        vel[i]=1.1

    while (env.tick < max_tick) and (cnt < len(jointRoute)-1):
        
        qpos = env.data.qpos[env.ctrl_qpos_idxs]
        qvel = env.data.qvel[env.ctrl_qvel_idxs]
        
        # Change PID target
        if abs(q_trgt[0]-qpos[0])<thrs and abs(q_trgt[1]-qpos[1])<thrs and abs(qvel[0])<thrs and abs(qvel[1])<thrs: 
            q_trgt,v_trgt = scheduler(jointRoute,cnt,1.1)
            cnt = cnt+1
        
        # PID controller
        pid.update(x_trgt=q_trgt,t_curr=env.get_sim_time(),x_curr=qpos,v_trgt=v_trgt,v_curr=qvel,VERBOSE=False)
        
        # Update
        torque = pid.out()
        env.step(ctrl=torque) # update

        # Append
        t_list[env.tick-1]        = env.get_sim_time()
        x_trgt_list[env.tick-1,:] = pid.x_trgt
        v_trgt_list[env.tick-1,:] = v_trgt
        qpos_list[env.tick-1,:]   = qpos
        qvel_list[env.tick-1,:]   = qvel
        torque_list[env.tick-1,:] = torque
        for i in range(len(boxes)):
            boxz[env.tick-1,i] = env.get_p_body(boxes[i])[2]
        
        # Render
        if env.loop_every(tick_every=20):
            env.render()

        for i in range(len(boxes)):
            if abs(boxz[0,i]-boxz[env.tick-1,i])>thrsBox:
                i = 0
                break

        if i < len(boxes)-1:
            break
    
    env.close_viewer() 
    bigCnt = bigCnt + 1

# Plot target and current joint position
fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
fig.subplots_adjust(hspace=0.4)
fig.suptitle("Joint Position", fontsize=10)
for a_idx,ax in enumerate(axs.ravel()):
    ax.plot(t_list[:env.tick],qpos_list[:env.tick,a_idx],
            '-',color='k',label='Current position')
    ax.plot(t_list[:env.tick],x_trgt_list[:env.tick,a_idx],
            '--',color='b',label='Target position')
    ax.set_title('Joint [%d]'%(a_idx),fontsize=8)
    if a_idx == 0: ax.legend(fontsize=8)
plt.show()

# Plot joint velocity
fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
fig.subplots_adjust(hspace=0.4)
fig.suptitle("Joint Velocity", fontsize=10)
for a_idx,ax in enumerate(axs.ravel()):
    ax.plot(t_list[:env.tick],qvel_list[:env.tick,a_idx],
            '-',color='k',label='Current velocity')
    ax.plot(t_list[:env.tick],v_trgt_list[:env.tick,a_idx],
            '--',color='r',label='Target position')
    ax.set_title('Joint [%d]'%(a_idx),fontsize=8)
    if a_idx == 0: ax.legend(fontsize=8)
plt.show()

# Plot control output
fig,axs = plt.subplots(nrows=1,ncols=2,sharex=False,sharey=False,figsize=(11,3))
fig.subplots_adjust(hspace=0.4)
fig.suptitle("Joint Control", fontsize=10)
for a_idx,ax in enumerate(axs.ravel()):
    ax.plot(t_list[:env.tick],torque_list[:env.tick,a_idx],color='r')
    ax.set_title('Joint [%d]'%(a_idx),fontsize=8)
plt.show()

fig,axs = plt.subplots(nrows=1,ncols=numbox,sharex=False,sharey=False,figsize=(11,3))
fig.subplots_adjust(hspace=0.4)
fig.suptitle("box position", fontsize=10)
for a_idx,ax in enumerate(axs.ravel()):
    ax.plot(t_list[:env.tick],boxz[:env.tick,a_idx],color='b')
    ax.set_title('Box %d'%(a_idx+1),fontsize=8)
plt.show()
