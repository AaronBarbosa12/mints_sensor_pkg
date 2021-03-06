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
	rospy.init_node('A'+ mac_add +'_' + 'SCD30_pub', anonymous=True)
	pub_c02= rospy.Publisher('A'+mac_add + '/SCD30/c02', Float32, queue_size=10)
	pub_temperature= rospy.Publisher('A'+mac_add + '/SCD30/temperature', Float32, queue_size=10)
	pub_humidity= rospy.Publisher('A'+mac_add + '/SCD30/humidity', Float32, queue_size=10)

	rate = rospy.Rate(0.2) 

	data_path = mD.dataFolder

	keyword =  '/' + mac_add + '/SCD30.json'


	while not rospy.is_shutdown():
		with open(data_path+keyword) as file:
			data = json.load(file)

			c02 =float(data['c02'])
			temperature =float(data['temperature'])
			humidity =float(data['humidity'])

			pub_c02.publish(c02)
			pub_temperature.publish(temperature)
			pub_humidity.publish(humidity)


			rate.sleep()
