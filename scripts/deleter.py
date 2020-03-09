import os
import sys
import shutil
import datetime
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD

dataFolder    = mD.dataFolder
macAddress    = mD.macAddress


def main():
    deleteDaysBack = 14
    try:
        shutil.rmtree(getDeletePath(deleteDaysBack))
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


def getDeletePath(daysBefore):
    deleteDate =  datetime.datetime.now() -  datetime.timedelta(daysBefore)
    deletePath = dataFolder+"/"+macAddress+"/"+str(deleteDate.year).zfill(4)  + \
    "/" + str(deleteDate.month).zfill(2)+ "/"+str(deleteDate.day).zfill(2)
    print(deletePath)
    return deletePath;


if __name__ == '__main__':
  main()
