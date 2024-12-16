import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib

plt.rcParams.update({'font.size': 25})
plt.rcParams["figure.figsize"] = (13,8)
lw = 3

filenameReal = ['pos1','pos2','pos3','pos4','pos5','desired']
filenameSim = ['pathOSCmax','pathOSCmin','pathPIDmax','pathPIDmin','desired']

lineStyles = ['-','--',':']
colors = ['r','b','g','y']

for i,name in enumerate(filenameReal):
    var = pd.read_csv(name + '.csv')

    x=np.array(list(var['x']))
    y=np.array(list(var['y']))
    
    if i < 5:
        t=np.array(list(var['rosbagTimestamp']))
        theta=np.array(list(var['z.1']))
        if i == 0:
            plt.plot(x,y, color=colors[3], linestyle=lineStyles[1], linewidth=lw)
        else: 
            plt.plot(x,y, color=colors[3], linestyle=lineStyles[1], linewidth=lw, label='_nolegend_')
    else:
        t=np.array(list(var['i']))
        theta=np.array(list(var['theta']))
        plt.scatter(x, y, c=colors[1], marker='o', linewidth=lw*10, zorder=10)

plt.ylabel(r'y-direction $[m]$')
plt.xlabel(r'x-direction $[m]$')
plt.xlim(5.5,8.5)
plt.legend(['MiR200 actual trajectories','Waypoints for test'])
plt.grid(True)
ax = plt.gca()

plt.savefig('figures/realPathMiR.png')
plt.show()

colors = ['r','m','g','c','b']

for i,name in enumerate(filenameSim):
    var = pd.read_csv(name + '.csv')
    
    t=np.array(list(var['i']))
    x=np.array(list(var['x']))
    y=np.array(list(var['y']))
    theta=np.array(list(var['theta']))

    if i < 4:
        plt.plot(x,y, color=colors[i], linestyle=lineStyles[1], linewidth=lw)
    else:
        plt.scatter(x, y, c=colors[i], marker='o', linewidth=lw*10, zorder=10)

plt.ylabel(r'y-direction $[m]$')
plt.xlabel(r'x-direction $[m]$')
plt.xlim(5.5,8.5)
plt.legend(['Trajectory OSC max config','Trajectory OSC min config','Trajectory PID max config','Trajectory PID min config','Waypoints for test'])
plt.grid(True)
ax = plt.gca()

plt.savefig('figures/simPathMiR.png')
plt.show()

filenameGrid = ['gridSetup1','gridSetup2','gridSetup3']

for i,name in enumerate(filenameGrid):
    var = pd.read_csv(name + '.csv')
    
    t=np.array(list(var['t']))
    acc=np.array(list(var['acc']))
    vel=np.array(list(var['vel']))
    bruteData=np.array(list(var['brute']))

    rows = np.arange(0.4,1.1,0.1)
    cols = np.arange(0.1,1.2,0.1)

    scatterTable = np.zeros((len(rows),len(cols)))
    colorsTable = np.array(scatterTable,dtype='<U11')
    colorsTable[:,:] = 'w'

    for j in range(len(acc)):
        idacc = np.argwhere(abs(rows-acc[j])<1e-6).flatten()
        idvel = np.argwhere(abs(cols-vel[j])<1e-6).flatten()
        scatterTable[len(rows)-1-idacc,idvel] = format(t[j]*0.0005, '.2f')
        colorsTable[len(rows)-1-idacc,idvel] = 'y'

    idacc = np.argwhere(abs(rows-bruteData[2])<1e-6).flatten()
    idvel = np.argwhere(abs(cols-bruteData[3])<1e-6).flatten()
    if scatterTable[len(rows)-1-idacc,idvel] > 0:
        colorsTable[len(rows)-1-idacc,idvel] = 'c'
    else:
        scatterTable[len(rows)-1-idacc,idvel] = format(bruteData[0]*0.0005, '.2f')
        colorsTable[len(rows)-1-idacc,idvel] = 'g'

    tab = plt.table(cellText=scatterTable,cellColours=colorsTable,loc=(0,0),cellLoc='center')

    for key, cell in tab.get_celld().items():
        cell.set_linewidth(4)
        cell.set_height(1./len(rows))
        cell.set_width(1./len(cols))

    custom_lines = [Patch(facecolor='w', edgecolor='k', lw=4,label='Unexplored'),Patch(facecolor='y', edgecolor='k', lw=4,label='Grid sim time[s]'),Patch(facecolor='g', edgecolor='k', lw=4,label='Brute sim time[s]'),Patch(facecolor='c', edgecolor='k', lw=4,label='Brute and Grid sim time[s]')]
   
    plt.ylabel(r'Acceleration $[m/s^2]$')
    plt.xlabel(r'Velocity $[m/s]$')
    plt.ylim(0.35,1.05)
    plt.xlim(0.05,1.15)
    plt.xticks(cols)
    plt.yticks(rows)
    plt.grid(False)
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,box.width, box.height * 0.8])
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),ncol=2,handles=custom_lines)

    plt.savefig('figures/'+ name + '.png')
    plt.show()