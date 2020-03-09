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
	rospy.init_node('A'+ mac_add +'_' + 'MGS001_pub', anonymous=True)
	pub_nh3= rospy.Publisher('A'+mac_add + '/MGS001/nh3', Float32, queue_size=10)
	pub_co= rospy.Publisher('A'+mac_add + '/MGS001/co', Float32, queue_size=10)
	pub_no2= rospy.Publisher('A'+mac_add + '/MGS001/no2', Float32, queue_size=10)
	pub_c3h8= rospy.Publisher('A'+mac_add + '/MGS001/c3h8', Float32, queue_size=10)
	pub_c4h10= rospy.Publisher('A'+mac_add + '/MGS001/c4h10', Float32, queue_size=10)
	pub_ch4= rospy.Publisher('A'+mac_add + '/MGS001/ch4', Float32, queue_size=10)
	pub_h2= rospy.Publisher('A'+mac_add + '/MGS001/h2', Float32, queue_size=10)
	pub_c2h5oh= rospy.Publisher('A'+mac_add + '/MGS001/c2h5oh', Float32, queue_size=10)
	rate = rospy.Rate(0.2) 

	data_path = mD.dataFolder

	keyword =  '/' + mac_add + '/MGS001.json'


	while not rospy.is_shutdown():
		with open(data_path+keyword) as file:
			data = json.load(file)

			nh3 =float(data['nh3'])
			co =float(data['co'])
			no2 =float(data['no2'])
			c3h8 =float(data['c3h8'])
			c4h10=float(data['c4h10'])
			ch4 =float(data['ch4'])
			h2 =float(data['h2'])
			c2h5oh =float(data['c2h5oh  '])

			pub_nh3.publish(nh3)
			pub_co.publish(co)
			pub_no2.publish(no2)
			pub_c3h8.publish(c3h8)
			pub_c4h10.publish(c4h10)
			pub_ch4.publish(ch4)
			pub_h2.publish(h2)
			pub_c2h5oh.publish(c2h5oh)

			rate.sleep()
