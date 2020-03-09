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

     rospy.init_node('A'+ mac_add +'_' + 'VEML_pub', anonymous=True)
     pub_rawUVA = rospy.Publisher('A'+mac_add+'/rawUVA', Float32, queue_size=10)
     pub_rawUVB = rospy.Publisher('A'+mac_add+'/rawUVB', Float32, queue_size=10)

     rate = rospy.Rate(0.2) 

     data_path = mD.dataFolder

     keyword =  '/' + mac_add+ '/VEML6075.json'


     while not rospy.is_shutdown():
          with open(data_path+keyword) as file:
               data = json.load(file)
               rawUVA =float(data['rawUVA'])
               rawUVB =float(data['rawUVB'])

               pub_rawUVA.publish(rawUVA)
               pub_rawUVB.publish(rawUVB)

               rate.sleep()


