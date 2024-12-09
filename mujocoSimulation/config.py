import matplotlib.pyplot as plt
import mujoco
import mediapy as media
import numpy as np
import sys
import os
import time
import itertools

sys.path.append('helper/')
sys.path.append('mujoco_usage/')
from mujoco_parser import *
from slider import *
from utility import *

r = 0.0625 #Drivewheel radius
L = 0.446708 #Seperation between drivewheels + 0.0015
RpS = 16 # 1m/s = 16 Radians/s
maxRv = 0.6 # the maximum experienced rotational velocity [m/s]
rr = 1/1000 # refresh rate currently 50Hz
maxTick = 1000000