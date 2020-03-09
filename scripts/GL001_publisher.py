#!/usr/bin/env python2

from std_msgs.msg import Float32
import datetime
from os import listdir
import os
import rospy 
import json
from mintsXU4 import mintsDefinitions as mD

if __name__ == '__main__':
     rospy.init_node('GL001_pub', anonymous=True)
     pub_lightLevel = rospy.Publisher('walkingrobot/GL001/lightLevel', Float32, queue_size=10)

     rate = rospy.Rate(0.2) 

     data_path = mD.dataFolder
     
     keyword =  '/' + mD.findMacAddress() + '/GL001.json'


     while not rospy.is_shutdown():
	with open(data_path+keyword) as file:
		data = json.load(file)

		lightLevel =float(data['lightLevel'])

		pub_lightLevel.publish(lightLevel)

		rate.sleep()
