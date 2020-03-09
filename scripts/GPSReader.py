
import serial
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD
import time
import serial
import pynmea2
from collections import OrderedDict
import os

dataFolder = mD.dataFolder
# duePort    = mD.duePort
gpsPort    =  mD.gpsPort

baudRate  = 9600




def main():

    reader = pynmea2.NMEAStreamReader()
    ser = serial.Serial(
    port= gpsPort,\
    baudrate=baudRate,\
    parity  =serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

    lastGPRMC = time.time()
    lastGPGGA = time.time()
    delta  = 2
    print("connected to: " + ser.portstr)

    #this will store the line
    line = []
    while True:
       try:
           for c in ser.read():
               line.append(chr(c))
               if chr(c) == '\n':
                   dataString     = (''.join(line))
                   dateTime  = datetime.datetime.now()
                   if (dataString.startswith("$GPGGA") and mSR.getDeltaTime(lastGPGGA,delta)):
                       mSR.GPSGPGGA2Write(dataString,dateTime)
                       lastGPGGA = time.time()
                   if (dataString.startswith("$GPRMC") and mSR.getDeltaTime(lastGPGGA,delta)):
                       mSR.GPSGPRMC2Write(dataString,dateTime)
                       lastGPRMC = time.time()
                   line = []
                   break
       except:
           print("Incomplete String Read")
           line = []

    ser.close()



if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    os.system("sudo chmod a+rw " + gpsPort)
    print("Monitoring Ozone Sensor on port: {0}".format(gpsPort[0])+ " with baudrate " + str(baudRate))
    main()
