import math
import matplotlib.pyplot as plt
import numpy as np

gravity = 9.8
cardBoardToPlastic = 0.54

def maxAccBox(size,weight,pos,maxVel=0.1,material=1,shape=1):
    acc = 0
    if material and shape:
        acc = ((weight*gravity*cardBoardToPlastic)-((size[1]*size[2]*maxVel*maxVel)/2))/weight

    return acc

def accCal(segmentVel,dist):
    time = 0
    totalDist = 0
    for vel in segmentVel:
        time = time + dist/vel
        totalDist = totalDist + dist
    return 2*totalDist/(time*time)


if __name__ == '__main__':
    path = [[6,2.5,0],[6.9,2.5,0],[7.8,2.5,math.pi/2],[7.8,14.7,math.pi],[6.1,14.7,-math.pi/2],[6.1,9.6,0],[6.9,9.6,-math.pi/2],[6.9,2.5,0],[6,2.5,0]]
    plt.plot([path[i][0] for i in range(len(path))],[path[i][1] for i in range(len(path))])
    plt.ylabel('some numbers')
    plt.gca().set_xlim([0, 15])
    plt.gca().set_ylim([0, 15])
    plt.autoscale(False)
    plt.show()
    print(maxAccBox([0.1,0.5,0.5],0.01,1))
    print(accCal(np.arange(0.1,1.1,0.1),0.1))

