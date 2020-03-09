#!/usr/bin/env python2

from std_msgs.msg import Float32
import datetime
import os 
from os import listdir
import rospy 
import json
from mintsXU4 import mintsDefinitions as mD

if __name__ == '__main__':
     rospy.init_node('APDS_pub', anonymous=True)
     pub_luminance= rospy.Publisher('walkingrobot/APDS9002/luminance', Float32, queue_size=10)

     rate = rospy.Rate(0.2) 

     data_path = mD.dataFolder
     
     keyword =  '/' + mD.findMacAddress() + '/APDS9002.json'


     while not rospy.is_shutdown():
	with open(data_path+keyword) as file:
		data = json.load(file)
		luminance =float(data['luminance'])

		pub_luminance.publish(luminance)

		rate.sleep()
     

