#!/usr/bin/env python2

from std_msgs.msg import Float32
import datetime
from os import listdir
import os
import rospy 
import json
from mintsXU4 import mintsDefinitions as mD

if __name__ == '__main__':
     rospy.init_node('TSL2591_pub', anonymous=True)
     pub_luminosity= rospy.Publisher('walkingrobot/TSL2591/luminosity', Float32, queue_size=10)
     pub_ir= rospy.Publisher('walkingrobot/TSL2591/ir', Float32, queue_size=10)
     pub_full= rospy.Publisher('walkingrobot/TSL2591/full', Float32, queue_size=10)
     pub_visible= rospy.Publisher('walkingrobot/TSL2591/visible', Float32, queue_size=10)
     pub_lux= rospy.Publisher('walkingrobot/TSL2591/lux', Float32, queue_size=10)
     rate = rospy.Rate(0.2) 

     data_path = mD.dataFolder
     
     keyword =  '/' + mD.findMacAddress() + '/TSL2591.json'


     while not rospy.is_shutdown():
	with open(data_path+keyword) as file:
		data = json.load(file)

		luminosity =float(data['luminosity'])
		ir =float(data['ir'])
		full =float(data['full'])
		visible =float(data['visible'])
		lux=float(data['lux'])

		pub_luminosity.publish(luminosity)
		pub_ir.publish(ir)
		pub_full.publish(full)
		pub_visible.publish(visible)
		pub_lux.publish(lux)

		rate.sleep()
