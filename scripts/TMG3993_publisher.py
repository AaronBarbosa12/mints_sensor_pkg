#!/usr/bin/env python2

from std_msgs.msg import Float32
import datetime
from os import listdir
import os
import rospy 
import json
from mintsXU4 import mintsDefinitions as mD

if __name__ == '__main__':
     rospy.init_node('TMG3993_pub', anonymous=True)
     pub_infraRed= rospy.Publisher('walkingrobot/TMG3993/infraRed', Float32, queue_size=10)
     pub_red= rospy.Publisher('walkingrobot/TMG3993/red', Float32, queue_size=10)
     pub_green= rospy.Publisher('walkingrobot/TMG3993/green', Float32, queue_size=10)
     pub_blue= rospy.Publisher('walkingrobot/TMG3993/blue', Float32, queue_size=10)
     pub_proximity= rospy.Publisher('walkingrobot/TMG3993/proximity', Float32, queue_size=10)
     rate = rospy.Rate(0.2) 

     data_path = mD.dataFolder
     
     keyword =  '/' + mD.findMacAddress() + '/TMG3993.json'


     while not rospy.is_shutdown():
	with open(data_path+keyword) as file:
		data = json.load(file)

		infraRed =float(data['infraRed'])
		red =float(data['red'])
		green =float(data['green'])
		blue =float(data['blue'])
		proximity=float(data['proximity'])

		pub_infraRed.publish(infraRed)
		pub_red.publish(red)
		pub_green.publish(green)
		pub_blue.publish(blue)
		pub_proximity.publish(proximity)

		rate.sleep()
