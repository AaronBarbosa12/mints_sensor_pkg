#!/usr/bin/env python2

from std_msgs.msg import Float32
import datetime
from os import listdir
import os
import rospy 
import json
from mintsXU4 import mintsDefinitions as mD

if __name__ == '__main__':
     mac_add = mD.findMacAddress()
     rospy.init_node('A'+ mac_add +'_' + 'GUV001_pub', anonymous=True)
     pub_uvLevel = rospy.Publisher('A'+mac_add + '/GUV001/uvLevel', Float32, queue_size=10)

     rate = rospy.Rate(0.2) 

     data_path = mD.dataFolder

     keyword =  '/' + mac_add + '/GUV001.json'


     while not rospy.is_shutdown():
          with open(data_path+keyword) as file:
               data = json.load(file)

               uvLevel =float(data['uvLevel'])

               pub_uvLevel.publish(uvLevel)

               rate.sleep()
