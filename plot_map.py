#!/usr/bin/env python2
import serial 
import rospy
from nav_msgs.msg import Path
import numpy as np
import matplotlib.pyplot as plt
import time

lidar_map = np.load("/home/aaron/map.npy", allow_pickle=True).item()
grid = np.asarray(lidar_map.data)
grid = np.reshape(grid,(1024,1024))
print(lidar_map.info)

plt.imshow(grid)
plt.show()
