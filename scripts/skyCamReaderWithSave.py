from datetime import timezone
import time
import os
import datetime
import numpy as np
import pickle
from skimage import io, color
import cv2

from mintsXU4 import mintsSkyCamReader as mSCR
from mintsXU4 import mintsSensorReader as mSR
from mintsXU4 import mintsDefinitions as mD


dataFolder = mD.dataFolder


def main():

    sensorName = "SKYCAM_002"
    dateTimeNow = datetime.datetime.now()
    subFolder     = mSR.getWritePathSnaps(sensorName,dateTimeNow)


    onboardCapture = True
    try:
        start = time.time()
        currentImage,imagePath =  mSCR.getSnapShotXU4(subFolder)
        modelName = 'naiveBayesModel.sav'
        oneDImage, imageShape = mSCR.generateFeatures(currentImage,imagePath)
        print("Loading Classifier")
        loadedModel = pickle.load(open(modelName, 'rb'))
        print("Done Loading")
        predictionBinary,prediction = mSCR.getPredictionMatrix(loadedModel,oneDImage)
        print("Writing Resulting Images ...")
        binaryImage = mSCR.writeBinaryImageXU4(predictionBinary,imageShape,imagePath,onboardCapture)

        sensorDictionary  = mSCR.getResultsXU4002(currentImage,binaryImage,predictionBinary,prediction,imagePath,dateTimeNow)
        mSR.sensorFinisher(dateTimeNow,sensorName,sensorDictionary)
        mSCR.timeTaken("Preiction time is ",start)
    except:
        print("TRY AGAIN")


if __name__ == "__main__":
   main()
