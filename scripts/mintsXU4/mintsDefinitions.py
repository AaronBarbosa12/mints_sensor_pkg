
from getmac import get_mac_address
import serial.tools.list_ports

def findPort(find):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        currentPort = str(p)
        if(currentPort.endswith(find)):
            return(currentPort.split(" ")[0])


def findDuePort():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        currentPort = str(p[2])
        if(currentPort.find("PID=2341")>=0):
            return(p[0])

def findNanoPorts():
    ports = list(serial.tools.list_ports.comports())
    outPorts = []
    for p in ports:
        currentPort = str(p)
        if(currentPort.endswith("FT232R USB UART")):
            outPorts.append(currentPort.split(" ")[0])

    return outPorts

def findSabrentPorts():
    ports = list(serial.tools.list_ports.comports())
    outPorts = []
    for p in ports:
        currentPort = str(p[2])
        if(currentPort.find("PID=067B")>=0):
            outPorts.append(str(p[0]).split(" ")[0])
    return outPorts

def findOzonePort():
    ports = list(serial.tools.list_ports.comports())
    ozonePort = []
    for p in ports:
        currentPort = str(p[2])
        if(currentPort.find("PID=067B")>=0):
            ozonePort.append(str(p[0]).split(" ")[0])
    return ozonePort


def findMacAddress():
    macAddress= get_mac_address(interface="eth0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="docker0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="enp1s0")
    if (macAddress!= None):
        return macAddress.replace(":","")

    macAddress= get_mac_address(interface="enp2s0")
    if (macAddress!= None):
        return macAddress.replace(":","")
    return "xxxxxxxx"



dataFolder            = "/home/aaron/catkin_ws/src/mints_sensor_pkg/mintsData/raw"
duePort               = findDuePort()
nanoPorts             = findNanoPorts()
ozonePort             = findOzonePort()
show2Port             = findPort("CP2104 USB to UART Bridge Controller")
macAddress            = findMacAddress()
# macAddress          = get_mac_address(interface="docker0").replace(":","")  #LAB Machine
# macAddress          = get_mac_address(interface="enp1s0").replace(":","")
# macAddress            = get_mac_address(interface="eth0").replace(":","") # XU4
latestDisplayOn       = True
gpsPort               = findPort("GPS/GNSS Receiver")


# print(length(findNansPorts))
