# ***************************************************************************
#  mintsXU4
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#   ---------------------------------
#   Date: February 4th, 2019
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#  ***************************************************************************

import serial
import datetime
import os
import csv
#import deepdish as dd
from mintsXU4 import mintsLatest as mL
from mintsXU4 import mintsDefinitions as mD
from getmac import get_mac_address
import time
import serial
import pynmea2
from collections import OrderedDict
import netifaces as ni
import math

macAddress    = mD.macAddress
dataFolder    = mD.dataFolder
latestDisplayOn    = mD.latestDisplayOn




def sensorFinisher(dateTime,sensorName,sensorDictionary):
    # Getting Write Path
    print("-----------------------------------")
    writePath = getWritePath(sensorName,dateTime)
    exists    = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    print(writePath)
    if(latestDisplayOn):
       mL.writeJSONLatest(sensorDictionary,sensorName)
    print(sensorName)
    print(sensorDictionary)
    print("-----------------------------------")



def sensorFinisherIP(dateTime,sensorName,sensorDictionary):
    #Getting Write Path
    writePath = getWritePathIP(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    print(writePath)
    if(latestDisplayOn):
       mL.writeJSONLatest(sensorDictionary,sensorName)

    print("-----------------------------------")
    print(sensorName)
    print(sensorDictionary)

def dataSplit(dataString,dateTime):
    dataOut   = dataString.split('!')
    if(len(dataOut) == 2):
        tag       = dataOut[0]
        dataQuota = dataOut[1]
        if(tag.find("#mintsO")==0):
            sensorSplit(dataQuota,dateTime)

def sensorSplit(dataQuota,dateTime):
    dataOut    = dataQuota.split('>')
    if(len(dataOut) == 2):
        sensorID   = dataOut[0]
        sensorData = dataOut[1]
        sensorSend(sensorID,sensorData,dateTime)

def sensorSend(sensorID,sensorData,dateTime):
    if(sensorID=="BME280"):
        BME280Write(sensorData,dateTime)
    if(sensorID=="MGS001"):
        MGS001Write(sensorData,dateTime)
    if(sensorID=="SCD30"):
        SCD30Write(sensorData,dateTime)
    if(sensorID=="VEML6075"):
        VEML6075Write(sensorData,dateTime)
    if(sensorID=="AS7262"):
        AS7262Write(sensorData,dateTime)
    if(sensorID=="PPD42NSDuo"):
        PPD42NSDuoWrite(sensorData,dateTime)
    if(sensorID=="OPCN2"):
        OPCN2Write(sensorData,dateTime)
    if(sensorID=="OPCN3"):
        OPCN3Write(sensorData,dateTime)
    if(sensorID=="VEML6070"):
        VEML6070Write(sensorData,dateTime)
    if(sensorID=="TSL2591"):
        TSL2591Write(sensorData,dateTime)
    if(sensorID=="LIBRAD"):
        LIBRADWrite(sensorData,dateTime)
    if(sensorID=="HTU21D"):
        HTU21DWrite(sensorData,dateTime)
    if(sensorID=="BMP280"):
        BMP280Write(sensorData,dateTime)
    if(sensorID=="INA219"):
        INA219Write(sensorData,dateTime)
    if(sensorID=="PPD42NS"):
        PPD42NSWrite(sensorData,dateTime)
    if(sensorID=="TMG3993"):
        TMG3993Write(sensorData, dateTime)
    if(sensorID=="GL001"):
        GL001Write(sensorData, dateTime)
    if(sensorID=="GUV001"):
        GUV001Write(sensorData, dateTime)
    if(sensorID=="APDS9002"):
        APDS9002Write(sensorData, dateTime)
    if(sensorID=="HM3301"):
        HM3301Write(sensorData, dateTime)




def BME280Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "BME280"
    dataLength = 4
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)), # always the same
        		("temperature"  ,dataOut[0]), # check with arduino code
            	("pressure"     ,dataOut[1]),
                ("humidity"     ,dataOut[2]),
            	("altitude"     ,dataOut[3])
                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def MGS001Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "MGS001"
    dataLength = 8
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"   , str(dateTime)),
        		("nh3"        ,dataOut[0]),
            	("co"         ,dataOut[1]),
                ("no2"        ,dataOut[2]),
            	("c3h8"       ,dataOut[3]),
        		("c4h10"      ,dataOut[4]),
            	("ch4"        ,dataOut[5]),
                ("h2"         ,dataOut[6]),
            	("c2h5oh  "   ,dataOut[7]),
                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def SCD30Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "SCD30"
    dataLength = 3
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("c02"          ,dataOut[0]),
            	("temperature"  ,dataOut[1]),
                ("humidity"     ,dataOut[2]),

                ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def LIBRADWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "LIBRAD"
    dataLength = 4
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
        	    ("countPerMinute"     ,dataOut[0]),
            	("radiationValue"     ,dataOut[1]),
                ("timeSpent"          ,dataOut[2]),
                ("LIBRADCount"        ,dataOut[3])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def VEML6070Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "VEML6070"
    dataLength = 1
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    , str(dateTime)),
        	    ("UVLightLevel" ,dataOut[0]),
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def TSL2591Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "TSL2591"
    dataLength = 5
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"   ,str(dateTime)),
        	    ("luminosity" ,dataOut[0]),
            	("ir"         ,dataOut[1]),
                ("full"       ,dataOut[2]),
                ("visible"    ,dataOut[3]),
                ("lux"        ,dataOut[4])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)

def VEML6075Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "VEML6075"
    dataLength = 7
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    , str(dateTime)),
        	    ("rawUVA" ,dataOut[0]),
                ("rawUVB" ,dataOut[1]),
        	    ("visibleCompensation" ,dataOut[2]),
                ("irCompensation" ,dataOut[3]),
                ("uva" ,dataOut[4]),
                ("uvb" ,dataOut[5]),
                ("index" ,dataOut[6]),
        	     ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def AS7262Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "AS7262"
    dataLength = 13
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("temperature"        ,dataOut[0]),
                ("violetPre"          ,dataOut[1]),
            	("bluePre"            ,dataOut[2]),
                ("greenPre"           ,dataOut[3]),
                ("yellowPre"          ,dataOut[4]),
                ("orangePre"          ,dataOut[5]),
        	    ("redPre"             ,dataOut[6]),
                ("violetCalibrated"   ,dataOut[7]),
            	("blueCalibrated"     ,dataOut[8]),
                ("greenCalibrated"    ,dataOut[9]),
                ("yellowCalibrated"   ,dataOut[10]),
                ("orangeCalibrated"   ,dataOut[11]),
                ("redCalibrated"      ,dataOut[12])
        	    ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)







def HTU21DWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "HTU21D"
    dataLength = 2
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    , str(dateTime)),
        	    ("temperature" ,dataOut[0]),
            	("humidity"    ,dataOut[1])
        	     ])


        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def BMP280Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "BMP280"
    dataLength = 2
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary =  OrderedDict([
                ("dateTime"     , str(dateTime)),
        		("temperature"  ,dataOut[0]),
            	("pressure"     ,dataOut[1])
                ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def INA219Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "INA219"
    dataLength = 5

    if(len(dataOut) == (dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"      ,str(dateTime)),
        	    ("shuntVoltage"  ,dataOut[0]),
            	("busVoltage"    ,dataOut[1]),
                ("currentMA"     ,dataOut[2]),
                ("powerMW"       ,dataOut[3]),
                ("loadVoltage"   ,dataOut[4])
        	     ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def OPCN2Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "OPCN2"
    dataLength= 28
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    ,str(dateTime)),
        		("valid"       ,dataOut[0]),
            	("binCount0"   ,dataOut[1]),
            	("binCount1"   ,dataOut[2]),
            	("binCount2"   ,dataOut[3]),
            	("binCount3"   ,dataOut[4]),
            	("binCount4"   ,dataOut[5]),
            	("binCount5"   ,dataOut[6]),
            	("binCount6"   ,dataOut[7]),
            	("binCount7"   ,dataOut[8]),
            	("binCount8"   ,dataOut[9]),
            	("binCount9"   ,dataOut[10]),
            	("binCount10"  ,dataOut[11]),
            	("binCount11"  ,dataOut[12]),
            	("binCount12"  ,dataOut[13]),
            	("binCount13"  ,dataOut[14]),
            	("binCount14"  ,dataOut[15]),
                ("binCount15"  ,dataOut[16]),
                ("bin1TimeToCross"      ,dataOut[17]),
                ("bin3TimeToCross"      ,dataOut[18]),
                ("bin5TimeToCross"      ,dataOut[19]),
                ("bin7TimeToCross"      ,dataOut[20]),
                ("sampleFlowRate"       ,dataOut[21]),
                ("temperatureOrPressure",dataOut[22]),
                ("samplingPeriod"       ,dataOut[23]),
                ("checkSum"             ,dataOut[24]),
                ("pm1"                  ,dataOut[25]),
                ("pm2_5"                ,dataOut[26]),
                ("pm10"                 ,dataOut[27])
                ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)



def OPCN3Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "OPCN3"
    dataLength=43
    if(len(dataOut) == (dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"    ,str(dateTime)),
        		("valid"       ,dataOut[0]),
            	("binCount0"   ,dataOut[1]),
            	("binCount1"   ,dataOut[2]),
            	("binCount2"   ,dataOut[3]),
            	("binCount3"   ,dataOut[4]),
            	("binCount4"   ,dataOut[5]),
            	("binCount5"   ,dataOut[6]),
            	("binCount6"   ,dataOut[7]),
            	("binCount7"   ,dataOut[8]),
            	("binCount8"   ,dataOut[9]),
            	("binCount9"   ,dataOut[10]),
            	("binCount10"  ,dataOut[11]),
            	("binCount11"  ,dataOut[12]),
            	("binCount12"  ,dataOut[13]),
            	("binCount13"  ,dataOut[14]),
            	("binCount14"  ,dataOut[15]),
            	("binCount15"  ,dataOut[16]),
            	("binCount16"  ,dataOut[17]),
            	("binCount17"  ,dataOut[18]),
            	("binCount18"  ,dataOut[19]),
            	("binCount19"  ,dataOut[20]),
            	("binCount20"  ,dataOut[21]),
            	("binCount21"  ,dataOut[22]),
            	("binCount22"  ,dataOut[23]),
            	("binCount23"  ,dataOut[24]),
                ("bin1TimeToCross"      ,dataOut[25]),
                ("bin3TimeToCross"      ,dataOut[26]),
                ("bin5TimeToCross"      ,dataOut[27]),
                ("bin7TimeToCross"      ,dataOut[28]),
                ("samplingPeriod"       ,dataOut[29]),
                ("sampleFlowRate"       ,dataOut[30]),
                ("temperature"          ,str(float(dataOut[31])/1000)),
                ("humidity"             ,str(float(dataOut[32])/500)),
                ("pm1"                ,dataOut[33]),
                ("pm2_5"              ,dataOut[34]),
                ("pm10"               ,dataOut[35]),
                ("rejectCountGlitch"    ,dataOut[36]),
                ("rejectCountLongTOF"   ,dataOut[37]),
                ("rejectCountRatio"     ,dataOut[38]),
                ("rejectCountOutOfRange",dataOut[39]),
                ("fanRevCount"          ,dataOut[40]),
                ("laserStatus"          ,dataOut[41]),
                ("checkSum"             ,dataOut[42])
                ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def PPD42NSDuoWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "PPD42NSDuo"
    dataLength = 8
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
                ("sampleTimeSeconds"  ,dataOut[0]),
                ("LPOPmMid"           ,dataOut[1]),
            	("LPOPm10"            ,dataOut[2]),
                ("ratioPmMid"         ,dataOut[3]),
                ("ratioPm10"          ,dataOut[4]),
        	("concentrationPmMid" ,dataOut[5]),
                ("concentrationPm2_5" ,dataOut[6]),
                ("concentrationPm10"  ,dataOut[7])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)


def PPD42NSWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "PPD42NS"
    dataLength = 4
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
        	    ("lowPulseOccupancy"  ,dataOut[0]),
            	("concentration"      ,dataOut[1]),
                ("ratio"              ,dataOut[2]),
                ("timeSpent"          ,dataOut[3])
        	     ])

        sensorFinisher(dateTime,sensorName,sensorDictionary)





def TMG3993Write(sensorData, dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "TMG3993"
    dataLength = 5
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
                ("infraRed"           ,dataOut[0]),
            	("red"                ,dataOut[1]),
                ("green"              ,dataOut[2]),
                ("blue"               ,dataOut[3]),
                ("proximity"          ,dataOut[4])
        	     ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def GL001Write(sensorData, dateTime):
    print("GL001Write: {0}".format(dateTime))
    dataOut    = sensorData.split(':')
    sensorName = "GL001"
    dataLength = 1
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
                ("lightLevel"          ,dataOut[0])
        	     ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)




def GUV001Write(sensorData, dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "GUV001"
    dataLength = 1
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
                ("uvLevel"          ,dataOut[0])
        	     ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)




def APDS9002Write(sensorData, dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "APDS9002"
    dataLength = 3
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
                ("luminance"          ,dataOut[0]),
                ("voltage"          ,dataOut[1]),
                ("raw"          ,dataOut[2])
        	     ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def HM3301Write(sensorData, dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "HM3301"
    dataLength = 3
    if(len(dataOut) ==(dataLength +1)):
        sensorDictionary = OrderedDict([
                ("dateTime"           ,str(dateTime)),
                ("pm1"          ,dataOut[0]),
                ("pm2_5"          ,dataOut[1]),
                ("pm10"          ,dataOut[2])
        	     ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def TB108LWrite(sensorData, dateTime):
    dataOut    = sensorData.split(',')
    sensorName = "TB108L"
    dataLength = 4
    if(len(dataOut) ==(dataLength)):
        sensorDictionary = OrderedDict([
                ("dateTime"       ,str(dateTime)),
                ("ozone"          ,dataOut[0]),
                ("temperature"    ,dataOut[1]),
                ("pressure"       ,dataOut[2]),
                ("voltage"        ,dataOut[3])
        	     ])
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def getDeltaTime(beginTime,deltaWanted):
    return (time.time() - beginTime)> deltaWanted



def getLatitudeCords(latitudeStr,latitudeDirection):
    latitude = float(latitudeStr)
    latitudeCord      =  math.floor(latitude/100) +(latitude - 100*(math.floor(latitude/100)))/60
    if(latitudeDirection=="S"):
        latitudeCord = -1*latitudeCord
    return latitudeCord

def getLongitudeCords(longitudeStr,longitudeDirection):
    longitude = float(longitudeStr)
    longitudeCord      =  math.floor(longitude/100) +(longitude - 100*(math.floor(longitude/100)))/60
    if(longitudeDirection=="W"):
        longitudeCord = -1*longitudeCord
    return longitudeCord

def GPSGPGGAWrite(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.gps_qual>0):
        sensorName = "GPSGPGGA"
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("timestamp"         ,sensorData.timestamp),
                ("latitude"          ,sensorData.lat),
                ("latitudeDirection" ,sensorData.lat_dir),
                ("longitude"         ,sensorData.lon),
                ("longitudeDirection",sensorData.lon_dir),
                ("gpsQuality"        ,sensorData.gps_qual),
                ("numberOfSatellites",sensorData.num_sats),
                ("HorizontalDilution",sensorData.horizontal_dil),
                ("altitude"          ,sensorData.altitude),
                ("altitudeUnits"     ,sensorData.altitude_units),
                ("undulation"        ,sensorData.geo_sep),
                ("undulationUnits"   ,sensorData.geo_sep_units),
                ("age"               ,sensorData.age_gps_data),
                ("stationID"         ,sensorData.ref_station_id)
        	     ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)


def GPSGPGGA2Write(dataString,dateTime):
    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    latitudeCordinate = getLatitudeCords(sensorData.lat,sensorData.lat_dir)

    if(sensorData.gps_qual>0):
        sensorName = "GPSGPGGA2"
        sensorDictionary = OrderedDict([
                ("dateTime"          ,str(dateTime)),
                ("timestamp"         ,sensorData.timestamp),
                ("latitudeCoordinate" ,getLatitudeCords(sensorData.lat,sensorData.lat_dir)),
                ("longitudeCoordinate",getLongitudeCords(sensorData.lon,sensorData.lon_dir)),
                ("latitude"          ,sensorData.lat),
                ("latitudeDirection" ,sensorData.lat_dir),
                ("longitude"         ,sensorData.lon),
                ("longitudeDirection",sensorData.lon_dir),
                ("gpsQuality"        ,sensorData.gps_qual),
                ("numberOfSatellites",sensorData.num_sats),
                ("HorizontalDilution",sensorData.horizontal_dil),
                ("altitude"          ,sensorData.altitude),
                ("altitudeUnits"     ,sensorData.altitude_units),
                ("undulation"        ,sensorData.geo_sep),
                ("undulationUnits"   ,sensorData.geo_sep_units),
                ("age"               ,sensorData.age_gps_data),
                ("stationID"         ,sensorData.ref_station_id)
        	 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def GPSGPRMCWrite(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.status=='A'):
        sensorName = "GPSGPRMC"
        sensorDictionary = OrderedDict([
                ("dateTime"             ,str(dateTime)),
                ("timestamp"            ,sensorData.timestamp),
                ("status"               ,sensorData.status),
                ("latitude"             ,sensorData.lat),
                ("latitudeDirection"    ,sensorData.lat_dir),
                ("longitude"            ,sensorData.lon),
                ("longitudeDirection"   ,sensorData.lon_dir),
                ("speedOverGround"      ,sensorData.spd_over_grnd),
                ("trueCourse"           ,sensorData.true_course),
                ("dateStamp"            ,sensorData.datestamp),
                ("magVariation"         ,sensorData.mag_variation),
                ("magVariationDirection",sensorData.mag_var_dir)
                 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)

def GPSGPRMC2Write(dataString,dateTime):

    dataStringPost = dataString.replace('\n', '')
    sensorData = pynmea2.parse(dataStringPost)
    if(sensorData.status=='A'):
        sensorName = "GPSGPRMC2"
        sensorDictionary = OrderedDict([
                ("dateTime"             ,str(dateTime)),
                ("timestamp"            ,sensorData.timestamp),
                ("status"               ,sensorData.status),
                ("latitudeCoordinate"    ,getLatitudeCords(sensorData.lat,sensorData.lat_dir)),
                ("longitudeCoordinate"   ,getLongitudeCords(sensorData.lon,sensorData.lon_dir)),
                ("latitude"             ,sensorData.lat),
                ("latitudeDirection"    ,sensorData.lat_dir),
                ("longitude"            ,sensorData.lon),
                ("longitudeDirection"   ,sensorData.lon_dir),
                ("speedOverGround"      ,sensorData.spd_over_grnd),
                ("trueCourse"           ,sensorData.true_course),
                ("dateStamp"            ,sensorData.datestamp)
                 ])

        #Getting Write Path
        sensorFinisher(dateTime,sensorName,sensorDictionary)






def writeCSV2(writePath,sensorDictionary,exists):
    keys =  list(sensorDictionary.keys())
    with open(writePath, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        # print(exists)
        if(not(exists)):
            writer.writeheader()
        writer.writerow(sensorDictionary)


# def writeHDF5Latest(writePath,sensorDictionary,sensorName):
#     try:
#         dd.io.save(dataFolder+sensorName+".h5", sensorDictionary)
#     except:
#         print("Data Conflict!")


def getWritePathIP(labelIn,dateTime):
    #Example  : MINTS_0061.csv
    writePath = dataFolder+"/"+macAddress+"/"+"MINTS_"+ macAddress+ "_IP.csv"
    return writePath;


def getWritePathSnaps(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/snaps/MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) + "_" +str(dateTime.hour).zfill(2) + "_" +str(dateTime.minute).zfill(2)+ "_" +str(dateTime.second).zfill(2) +".png"
    return writePath;



def getWritePath(labelIn,dateTime):
    #Example  : MINTS_0061_OOPCN3_2019_01_04.csv
    writePath = dataFolder+"/"+macAddress+"/"+str(dateTime.year).zfill(4)  + "/" + str(dateTime.month).zfill(2)+ "/"+str(dateTime.day).zfill(2)+"/"+ "MINTS_"+ macAddress+ "_" +labelIn + "_" + str(dateTime.year).zfill(4) + "_" +str(dateTime.month).zfill(2) + "_" +str(dateTime.day).zfill(2) +".csv"
    return writePath;

def getListDictionaryFromPath(dirPath):
    print("Reading : "+ dirPath)
    reader = csv.DictReader(open(dirPath))
    reader = list(reader)

def fixCSV(keyIn,valueIn,currentDictionary):
    editedList       = editDictionaryList(currentDictionary,keyIn,valueIn)
    return editedList

def editDictionaryList(dictionaryListIn,keyIn,valueIn):
    for dictionaryIn in dictionaryListIn:
        dictionaryIn[keyIn] = valueIn

    return dictionaryListIn

def getDateDataOrganized(currentCSV,nodeID):
    currentCSVName = os.path.basename(currentCSV)
    nameOnly = currentCSVName.split('-Organized.')
    dateOnly = nameOnly[0].split(nodeID+'-')
    print(dateOnly)
    dateInfo = dateOnly[1].split('-')
    print(dateInfo)
    return dateInfo


def getFilePathsforOrganizedNodes(nodeID,subFolder):
    nodeFolder = subFolder+ nodeID+'/';
    pattern = "*Organized.csv"
    fileList = [];
    for path, subdirs, files in os.walk(nodeFolder):
        for name in files:
            if fnmatch(name, pattern):
                fileList.append(os.path.join(path, name))
    return sorted(fileList)


def getLocationList(directory, suffix=".csv"):
    filenames = listdir(directory)
    dateList = [ filename for filename in filenames if filename.endswith( suffix ) ]
    return sorted(dateList)


def getListDictionaryCSV(inputPath):
    # the path will depend on the node ID
    reader = csv.DictReader(open(inputPath))
    reader = list(reader)
    return reader

def writeCSV(reader,keys,outputPath):
    directoryCheck(outputPath)
    csvWriter(outputPath,reader,keys)

def directoryCheck(outputPath):
    exists = os.path.isfile(outputPath)
    directoryIn = os.path.dirname(outputPath)
    if not os.path.exists(directoryIn):
        os.makedirs(directoryIn)
    return exists

def csvWriter(writePath,organizedData,keys):
    with open(writePath,'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(organizedData)


def gainDirectoryInfo(dailyDownloadLocation):
    directoryPaths = []
    directoryNames = []
    directoryFiles = []
    for (dirpath, dirnames, filenames) in walk(dailyDownloadLocation):
        directoryPaths.extend(dirpath)
        directoryNames.extend(dirnames)
        directoryFiles.extend(filenames)

    return directoryPaths,directoryNames,directoryFiles;
