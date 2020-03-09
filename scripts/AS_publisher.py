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

	rospy.init_node('A'+ mac_add +'_' + 'AS7262_pub', anonymous=True)
	pub_temperature= rospy.Publisher('A'+mac_add + '/AS7262/temperature', Float32, queue_size=10)
	pub_violetPre= rospy.Publisher('A'+mac_add + '/AS7262/violetPre', Float32, queue_size=10)
	pub_bluePre= rospy.Publisher('A'+mac_add + '/AS7262/bluePre', Float32, queue_size=10)
	pub_greenPre= rospy.Publisher('A'+mac_add + '/AS7262/greenPre', Float32, queue_size=10)
	pub_yellowPre= rospy.Publisher('A'+mac_add + '/AS7262/yellowPre', Float32, queue_size=10)
	pub_orangePre= rospy.Publisher('A'+mac_add + '/AS7262/orangePre', Float32, queue_size=10)
	pub_redPre= rospy.Publisher('A'+mac_add + '/AS7262/redPre', Float32, queue_size=10)
	pub_violetCalibrated= rospy.Publisher('A'+mac_add + '/AS7262/violetCalibrated', Float32, queue_size=10)
	pub_blueCalibrated= rospy.Publisher('A'+mac_add + '/AS7262/blueCalibrated', Float32, queue_size=10)
	pub_greenCalibrated= rospy.Publisher('A'+mac_add + '/AS7262/greenCalibrated', Float32, queue_size=10)
	pub_yellowCalibrated= rospy.Publisher('A'+mac_add + '/AS7262/yellowCalibrated', Float32, queue_size=10)
	pub_orangeCalibrated= rospy.Publisher('A'+mac_add + '/AS7262/orangeCalibrated', Float32, queue_size=10)
	pub_redCalibrated= rospy.Publisher('A'+mac_add + '/AS7262/redCalibrated', Float32, queue_size=10)
	rate = rospy.Rate(0.2) 

	data_path = mD.dataFolder

	keyword =  '/' + mac_add + '/AS7262.json'


	while not rospy.is_shutdown():
		with open(data_path+keyword) as file:
			data = json.load(file)

			temperature =float(data['temperature'])
			violetPre =float(data['violetPre'])
			bluePre =float(data['bluePre'])
			greenPre =float(data['greenPre'])
			yellowPre=float(data['yellowPre'])
			orangePre =float(data['orangePre'])
			redPre =float(data['redPre'])
			violetCalibrated =float(data['violetCalibrated'])
			blueCalibrated =float(data['blueCalibrated'])
			greenCalibrated =float(data['greenCalibrated'])
			yellowCalibrated =float(data['yellowCalibrated'])
			orangeCalibrated =float(data['orangeCalibrated'])
			redCalibrated =float(data['redCalibrated'])

			pub_temperature.publish(temperature)
			pub_violetPre.publish(violetPre)
			pub_bluePre.publish(bluePre)
			pub_greenPre.publish(greenPre)
			pub_yellowPre.publish(yellowPre)
			pub_orangePre.publish(orangePre)
			pub_redPre.publish(redPre)
			pub_violetCalibrated.publish(violetCalibrated)
			pub_blueCalibrated.publish(blueCalibrated)
			pub_greenCalibrated.publish(greenCalibrated)
			pub_yellowCalibrated.publish(yellowCalibrated)
			pub_orangeCalibrated.publish(orangeCalibrated)
			pub_redCalibrated.publish(redCalibrated)

			rate.sleep()
     

