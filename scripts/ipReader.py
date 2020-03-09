from datetime import timezone
import time
import os
import datetime
import netifaces as ni
from collections import OrderedDict
import netifaces as ni
from requests import get

from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions  as mD

dataFolder = mD.dataFolder


def main():

    sensorName = "IP"
    dateTimeNow = datetime.datetime.now()
    print("Gaining the Public and Private IPs")

    publicIp = get('https://api.ipify.org').text
    #localIp  = ni.ifaddresses('docker0')[ni.AF_INET][0]['addr'] # Lab Machine
    localIp = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'] # Odroid XU4

    sensorDictionary =  OrderedDict([
            ("dateTime"     , str(dateTimeNow)),
            ("publicIp"  ,str(publicIp)),
            ("localIp"  ,str(localIp))
            ])

    mSR.sensorFinisherIP(dateTimeNow,sensorName,sensorDictionary)

if __name__ == "__main__":
    print("=============")
    print("    MINTS    ")
    print("=============")
    main()
