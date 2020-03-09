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
	rospy.init_node('A'+ mac_add +'_' + 'BME280_pub', anonymous=True)
	pub_temperature= rospy.Publisher('A'+mac_add + '/BME280/temperature', Float32, queue_size=10)
	pub_pressure= rospy.Publisher('A'+mac_add + '/BME280/pressure', Float32, queue_size=10)
	pub_humidity= rospy.Publisher('A'+mac_add + '/BME280/humidity', Float32, queue_size=10)
	pub_altitude= rospy.Publisher('A'+mac_add + '/BME280/altitude', Float32, queue_size=10)

	rate = rospy.Rate(0.2) 

	data_path = mD.dataFolder

	keyword =  '/' + mac_add + '/BME280.json'


	while not rospy.is_shutdown():
		with open(data_path+keyword) as file:
			data = json.load(file)

			temperature =float(data['temperature'])
			pressure =float(data['pressure'])
			humidity =float(data['humidity'])
			altitude =float(data['altitude'])

			pub_temperature.publish(temperature)
			pub_pressure.publish(pressure)
			pub_humidity.publish(humidity)
			pub_altitude.publish(altitude)

			rate.sleep()
     

