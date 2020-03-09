from datetime import timezone
import time
import os
import datetime
import numpy as np
import pickle
from skimage import io, color
import cv2
from collections import OrderedDict
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials


# def main():
#
#     dataFolder    = '../../../../data/'
#     subFolder     = dataFolder + "webCamSnaps/"
#
#     onboardCapture = True
#     currentImage,imagePath =  getSnapShot(subFolder)
#     # currentImage,imagePath =  getSnapShotFromPath(pathIn)
#
#     start = time.time()
#     modelName = 'naiveBayesModel.sav'
#
#     oneDImage, imageShape = generateFeatures(currentImage,imagePath)
#     print("Loading Classifier")
#
#     loadedModel = pickle.load(open(modelName, 'rb'))
#     print("Done Loading")
#     predictionBinary,prediction = getPredictionMatrix(loadedModel,oneDImage)
#
#     print("Writing Resulting Images ...")
#     binaryImage = writeBinaryImage(predictionBinary,imageShape,imagePath,onboardCapture)
#     resultsOut  = getResults(currentImage,binaryImage,predictionBinary,prediction,imagePath)
#     print(str(resultsOut))
#     # wks.append_row(resultsOut)
#
#
#     ## Now the Focus will


def getResultsXU4002(originalImage,binaryImage,predictionBinary,prediction,imagePath,dateTime):

    onlyCloud          = getCloudOnlyImage(originalImage,binaryImage)
    onlySky            = getSkyOnlyImage(originalImage,binaryImage)

    cloudPercentage    = (sum(predictionBinary)/len(predictionBinary))*100

    percentageAccuracy = sum(abs(prediction-.5)*200)/len(prediction)
    #
    colorSumBlueAll    = originalImage[:,:,0].sum()
    colorSumGreenAll   = originalImage[:,:,1].sum()
    colorSumRedAll     = originalImage[:,:,2].sum()

    dimSize = np.shape(originalImage)

    numOfPixels        = dimSize[0]*dimSize[1]

    averageBlueAll     = colorSumBlueAll/numOfPixels
    averageGreenAll    = colorSumGreenAll/numOfPixels
    averageRedAll      = colorSumRedAll/numOfPixels

    colorSumBlueSky    = onlySky[:,:,0].sum()
    colorSumGreenSky   = onlySky[:,:,1].sum()
    colorSumRedSky     = onlySky[:,:,2].sum()
    #
    colorSumBlueCloud  = onlyCloud[:,:,0].sum()
    colorSumGreenCloud = onlyCloud[:,:,1].sum()
    colorSumRedCloud   = onlyCloud[:,:,2].sum()
    #
    cloudPixelCount  = np.sum(binaryImage[:,:,0] == 255)
    skyPixelCount    = np.sum(binaryImage[:,:,0] == 0)


    if cloudPercentage !=100:
        averageBlueSky  = colorSumBlueSky/skyPixelCount
        averageGreenSky = colorSumGreenSky/skyPixelCount
        averageRedSky   = colorSumRedSky/skyPixelCount
    else:
        averageBlueSky  = -1  # Denoting 0% of Sky
        averageGreenSky = -1  # Denoting 0% of Sky
        averageRedSky   = -1  # Denoting 0% of Sky

# Printing the Average Pixel values for each Color

    if  cloudPercentage !=0:
        averageBlueCloud  = colorSumBlueCloud/cloudPixelCount
        averageGreenCloud = colorSumGreenCloud/cloudPixelCount
        averageRedCloud   = colorSumRedCloud/cloudPixelCount
    else:
        averageBlueCloud  = -1 # Denoting 0% of Sky
        averageGreenCloud = -1 # Denoting 0% of Sky
        averageRedCloud   = -1 # Denoting 0% of Sky

    cloudPercentage =str(float(cloudPercentage))
    print("------------------------------")
    # print("Predictionn Accuracy :  "+str(percentageAccuracy)+"%")
    print("------------------------------")
    print("Cloud Pecentage      :  "+cloudPercentage+"%")
    print('-----------------------------------')
    print('All Red              : ',averageRedAll)
    print('All Green            : ',averageGreenAll)
    print('All Blue             : ',averageBlueAll)
    print('-----------------------------------')
    print('Sky Red              : ',averageRedSky)
    print('Sky Green            : ',averageGreenSky)
    print('Sky Blue             : ',averageBlueSky)
    print('-----------------------------------')
    print('Cloud Red            : ',averageRedCloud)
    print('Cloud Green          : ',averageGreenCloud)
    print('Cloud Blue           : ',averageBlueCloud)
    print('-----------------------------------')
    print('Done.')


    sensorDictionary = OrderedDict([
            ("dateTime"             ,str(dateTime)),
            ("cloudPecentage"       ,cloudPercentage),
            ("allRed"               ,averageRedAll),
            ("allGreen"             ,averageGreenAll),
            ("allBlue"              ,averageBlueAll),
            ("skyRed"               ,averageRedSky),
            ("skyGreen"             ,averageGreenSky),
            ("skyBlue"              ,averageBlueSky),
            ("cloudRed"             ,averageRedCloud),
            ("cloudGreen"           ,averageGreenCloud),
            ("cloudBlue"            ,averageBlueCloud),
         ])

    return sensorDictionary

def writeBinaryImageXU4NoSave(Pixel_Row ,Image_Shape,PathIn,onboardCapture):
    # Designed to return a binary image and write the said image to a given path
    Image_Reshaped = []
    Pixel_Row_255 = Pixel_Row.astype(float)*255
    Pixel_Row_Transpose = np.transpose(Pixel_Row_255)
    Image_Reshaped_Pre = np.asarray(Pixel_Row_Transpose.reshape((Image_Shape[0], Image_Shape[1])))
    Image_Reshaped     = np.zeros((Image_Shape[0], Image_Shape[1], 3))

    Image_Reshaped[:, :, 0] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 1] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 2] = Image_Reshaped_Pre

    os.remove(PathIn)

    # binaryImagePath = PathIn.replace("SKYCAM", "SKYCAM_binary")
    # directoryCheck(binaryImagePath)
    # cv2.imwrite(binaryImagePath, Image_Reshaped)

    return Image_Reshaped


def getResults(originalImage,binaryImage,predictionBinary,prediction,imagePath):

    onlyCloud          = getCloudOnlyImage(originalImage,binaryImage)
    onlySky            = getSkyOnlyImage(originalImage,binaryImage)
    cloudPercentage    = (sum(predictionBinary)/len(predictionBinary))*100

    percentageAccuracy =sum(abs(prediction-.5)*200)/len(prediction)
    #
    colorSumBlueSky    = onlySky[:,:,0].sum()
    colorSumGreenSky   = onlySky[:,:,1].sum()
    colorSumRedSky     = onlySky[:,:,2].sum()
    #
    colorSumBlueCloud  = onlyCloud[:,:,0].sum()
    colorSumGreenCloud = onlyCloud[:,:,1].sum()
    colorSumRedCloud   = onlyCloud[:,:,2].sum()
    #
    cloudPixelCount  = np.sum(binaryImage[:,:,0] == 255)
    skyPixelCount    = np.sum(binaryImage[:,:,0] == 0)

    if cloudPercentage !=100:
        averageBlueSky  = colorSumBlueSky/skyPixelCount
        averageGreenSky = colorSumGreenSky/skyPixelCount
        averageRedSky   = colorSumRedSky/skyPixelCount
    else:
        averageBlueSky  = -1  # Denoting 0% of Sky
        averageGreenSky = -1  # Denoting 0% of Sky
        averageRedSky   = -1  # Denoting 0% of Sky

# Printing the Average Pixel values for each Color

    if  cloudPercentage !=0:
        averageBlueCloud  = colorSumBlueCloud/cloudPixelCount
        averageGreenCloud = colorSumGreenCloud/cloudPixelCount
        averageRedCloud   = colorSumRedCloud/cloudPixelCount
    else:
        averageBlueCloud  = -1 # Denoting 0% of Sky
        averageGreenCloud = -1 # Denoting 0% of Sky
        averageRedCloud   = -1 # Denoting 0% of Sky

    cloudPercentage =str(float(cloudPercentage))
    print("------------------------------")
    # print("Predictionn Accuracy :  "+str(percentageAccuracy)+"%")
    print("------------------------------")
    print("Cloud Pecentage      :  "+cloudPercentage+"%")
    print('-----------------------------------')
    print('Sky Red              : ',averageRedSky)
    print('Sky Green            : ',averageGreenSky)
    print('Sky Blue             : ',averageBlueSky)
    print('-----------------------------------')
    print('Cloud Red            : ',averageRedCloud)
    print('Cloud Green          : ',averageGreenCloud)
    print('Cloud Blue           : ',averageBlueCloud)
    print('-----------------------------------')
    print('Done.')
    dateTime  =  getDateTimeFromPath(imagePath)
    return [dateTime, cloudPercentage,averageRedSky,averageGreenSky,averageBlueSky,averageRedCloud,averageGreenCloud,averageBlueCloud]





def getResultsXU4(originalImage,binaryImage,predictionBinary,prediction,imagePath,dateTime):

    onlyCloud          = getCloudOnlyImage(originalImage,binaryImage)
    onlySky            = getSkyOnlyImage(originalImage,binaryImage)
    cloudPercentage    = (sum(predictionBinary)/len(predictionBinary))*100

    percentageAccuracy =sum(abs(prediction-.5)*200)/len(prediction)
    #
    colorSumBlueSky    = onlySky[:,:,0].sum()
    colorSumGreenSky   = onlySky[:,:,1].sum()
    colorSumRedSky     = onlySky[:,:,2].sum()
    #
    colorSumBlueCloud  = onlyCloud[:,:,0].sum()
    colorSumGreenCloud = onlyCloud[:,:,1].sum()
    colorSumRedCloud   = onlyCloud[:,:,2].sum()
    #
    cloudPixelCount  = np.sum(binaryImage[:,:,0] == 255)
    skyPixelCount    = np.sum(binaryImage[:,:,0] == 0)

    if cloudPercentage !=100:
        averageBlueSky  = colorSumBlueSky/skyPixelCount
        averageGreenSky = colorSumGreenSky/skyPixelCount
        averageRedSky   = colorSumRedSky/skyPixelCount
    else:
        averageBlueSky  = -1  # Denoting 0% of Sky
        averageGreenSky = -1  # Denoting 0% of Sky
        averageRedSky   = -1  # Denoting 0% of Sky

# Printing the Average Pixel values for each Color

    if  cloudPercentage !=0:
        averageBlueCloud  = colorSumBlueCloud/cloudPixelCount
        averageGreenCloud = colorSumGreenCloud/cloudPixelCount
        averageRedCloud   = colorSumRedCloud/cloudPixelCount
    else:
        averageBlueCloud  = -1 # Denoting 0% of Sky
        averageGreenCloud = -1 # Denoting 0% of Sky
        averageRedCloud   = -1 # Denoting 0% of Sky

    cloudPercentage =str(float(cloudPercentage))
    print("------------------------------")
    # print("Predictionn Accuracy :  "+str(percentageAccuracy)+"%")
    print("------------------------------")
    print("Cloud Pecentage      :  "+cloudPercentage+"%")
    print('-----------------------------------')
    print('Sky Red              : ',averageRedSky)
    print('Sky Green            : ',averageGreenSky)
    print('Sky Blue             : ',averageBlueSky)
    print('-----------------------------------')
    print('Cloud Red            : ',averageRedCloud)
    print('Cloud Green          : ',averageGreenCloud)
    print('Cloud Blue           : ',averageBlueCloud)
    print('-----------------------------------')
    print('Done.')


    sensorDictionary = OrderedDict([
            ("dateTime"             ,str(dateTime)),
            ("cloudPecentage"       ,cloudPercentage),
            ("skyRed"               ,averageRedSky),
            ("skyGreen"             ,averageGreenSky),
            ("skyBlue"              ,averageBlueSky),
            ("cloudRed"             ,averageRedCloud),
            ("cloudGreen"           ,averageGreenCloud),
            ("cloudBlue"            ,averageBlueCloud),
         ])


    return sensorDictionary










def getDateTimeFromPath(imagePath):

    nameIn ,extensionIn=getFileNameAndExtension(imagePath)
    return nameIn.split('MintsSky-')[-1]


def getPredictionMatrix(loadedModel,oneDImage):
    prediction       = loadedModel.predict(oneDImage)
    predictionBinary = np.transpose(np.matrix(np.array(prediction)))
    predictionBinary[predictionBinary < 0.5]  = 0
    predictionBinary[predictionBinary >= 0.5] = 1
    return predictionBinary,prediction

def getDateTimeString(now):
    yearOut   = str(now.year)
    monthOut  = str(now.month)
    dayOut    = str(now.day)
    hourOut   = str(now.hour)
    minuteOut = str(now.minute)
    secondOut = str(now.second)
    return yearOut+'-'+monthOut+'-'+dayOut+'-'+hourOut+'-'+minuteOut+'-'+secondOut


def getSnapShot(folderIn):

    camera = cv2.VideoCapture(0)
    now = datetime.datetime.now(timezone.utc)
    return_value, image = camera.read()
    imageName =  folderIn+ 'MintsSky-' +getDateTimeString(now)+'.png'
    # imageName = "lk.png"
    print(imageName)
    directoryCheck(imageName)
    cv2.imwrite(imageName, image)
    del(camera)
    return image,imageName;


def getSnapShotXU4(folderIn):

    # connected, index = getVideoPortIndex(folderIn)
    #
    # if(connected):
    camera = cv2.VideoCapture(0)
    # now = datetime.datetime.now(timezone.utc)
    return_value, image = camera.read()

        # imageName =  folderIn+ 'MintsSky-' +getDateTimeString(now)+'.png'
        # imageName = "lk.png"
    print(folderIn)
    directoryCheck(folderIn)
    cv2.imwrite(folderIn, image)
    del(camera)
    return image,folderIn;
    # else:
    #     print("No Camera Connected - Program Halted")



def getVideoPortIndex(folderIn):

    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            cap.release()
            return True, index ;
        else:
            index += 1
            if index ==20:
                cap.release()
                return False, index;






def getSnapShotFromPath(pathIn):
    inputImage = cv2.imread(pathIn)
    return inputImage,pathIn;



def getSnaps(numOfPics,folderIn):
    camera = cv2.VideoCapture(0)
    i = 0
    if numOfPics >=1:
        while i < numOfPics:
            return_value, image = camera.read()
            print(image)
            cv2.imwrite(folderIn+ 'testSnaps'+str(i)+'.png', image)
            i=i+1
    else:
        print(str(numOfPics) + "is not a valid number")
    del(camera)



def generateFeatures(inputImage,imagePath):
    # Take in an image path and append inputs and outputs
    # Image.open(input_path).convert('RGBA')

    # inputImage = cv2.imread(input_path)
    inputImage_RGB = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGBA)
    inputImage_HSV = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)

    RGB_for_LAB = io.imread(imagePath)
    inputImage_LAB = color.rgb2lab(RGB_for_LAB)

    Image_Array_RGB = np.array(inputImage_RGB)
    Image_Array_HSV = np.array(inputImage_HSV)
    Image_Array_LAB = np.array(inputImage_LAB)


    # Record the original shape
    Image_Shape = Image_Array_RGB.shape

    # Make a 1-dimensional view of arrays

    One_D_Image_Red   = np.transpose(np.matrix(Image_Array_RGB[:, :, 0].ravel()))
    One_D_Image_Green = np.transpose(np.matrix(Image_Array_RGB[:, :, 1].ravel()))
    One_D_Image_Blue  = np.transpose(np.matrix(Image_Array_RGB[:, :, 2].ravel()))

    # Recasting to support negative integers

    One_D_Image_Red   = One_D_Image_Red.astype(np.int16)
    One_D_Image_Green = One_D_Image_Green.astype(np.int16)
    One_D_Image_Blue  = One_D_Image_Blue.astype(np.int16)

    One_D_Image_H = np.transpose(np.matrix(Image_Array_HSV[:, :, 0].ravel()))
    One_D_Image_S = np.transpose(np.matrix(Image_Array_HSV[:, :, 1].ravel()))
    One_D_Image_V = np.transpose(np.matrix(Image_Array_HSV[:, :, 2].ravel()))

    One_D_Image_L = np.transpose(np.matrix(Image_Array_LAB[:, :, 0].ravel()))
    One_D_Image_A = np.transpose(np.matrix(Image_Array_LAB[:, :, 1].ravel()))
    One_D_Image_B = np.transpose(np.matrix(Image_Array_LAB[:, :, 2].ravel()))

    # Getting the Chroma Values for each pixel

    One_D_RGB_Only=np.hstack((One_D_Image_Red, One_D_Image_Green, One_D_Image_Blue))
    Max_RGB = One_D_RGB_Only.max(1)
    Min_RGB = One_D_RGB_Only.min(1)
    One_D_Chroma = Max_RGB-Min_RGB
    # One_D_Image_Red, One_D_Image_Green,One_D_Image_H, One_D_Image_S, One_D_Image_V, \One_D_Image_L, One_D_Image_A,
    One_D_Image = np.hstack((One_D_Image_Blue,\
                             One_D_Image_B, \
                             One_D_Image_Red/(One_D_Image_Blue+1), np.subtract(One_D_Image_Red, One_D_Image_Blue), \
                             (One_D_Image_Blue-One_D_Image_Red)/((One_D_Image_Blue+One_D_Image_Red)+1),\
                             One_D_Chroma
                             ))


    return One_D_Image, Image_Shape

def Generate_Targets(input_path):
    # Genarates a 1D vector for each target Image
    Input_Image_Binary = cv2.imread(input_path)
    Image_Array_Binary = np.array(Input_Image_Binary)
    Image_Shape = Image_Array_Binary.shape
    One_D_Binary = np.transpose(np.matrix(Image_Array_Binary[:, :, 1].ravel()))
    One_D_Binary = One_D_Binary.astype(float) / 255
    return One_D_Binary, Image_Shape



def writeBinaryImage(Pixel_Row ,Image_Shape,PathIn,onboardCapture):
    # Designed to return a binary image and write the said image to a given path
    Image_Reshaped = []
    Pixel_Row_255 = Pixel_Row.astype(float)*255
    Pixel_Row_Transpose = np.transpose(Pixel_Row_255)
    Image_Reshaped_Pre = np.asarray(Pixel_Row_Transpose.reshape((Image_Shape[0], Image_Shape[1])))
    Image_Reshaped     = np.zeros((Image_Shape[0], Image_Shape[1], 3))

    Image_Reshaped[:, :, 0] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 1] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 2] = Image_Reshaped_Pre

    nameIn ,extensionIn=getFileNameAndExtension(PathIn)
    if(onboardCapture):
        binaryImagePath = nameIn.split('Sky')[0] +'SkyPrediction'+ nameIn.split('Sky')[1] +extensionIn
    else:
        binaryImagePath = nameIn+'Binary'+extensionIn

    directoryCheck(binaryImagePath)
    cv2.imwrite(binaryImagePath, Image_Reshaped)

    return Image_Reshaped


def writeBinaryImageXU4(Pixel_Row ,Image_Shape,PathIn,onboardCapture):
    # Designed to return a binary image and write the said image to a given path
    Image_Reshaped = []
    Pixel_Row_255 = Pixel_Row.astype(float)*255
    Pixel_Row_Transpose = np.transpose(Pixel_Row_255)
    Image_Reshaped_Pre = np.asarray(Pixel_Row_Transpose.reshape((Image_Shape[0], Image_Shape[1])))
    Image_Reshaped     = np.zeros((Image_Shape[0], Image_Shape[1], 3))

    Image_Reshaped[:, :, 0] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 1] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 2] = Image_Reshaped_Pre

    # nameIn ,extensionIn=getFileNameAndExtension(PathIn)
    binaryImagePath = PathIn.replace("SKYCAM", "SKYCAM_binary")

    # if(onboardCapture):
    #     binaryImagePath = nameIn.split('Sky')[0] +'SkyPrediction'+ nameIn.split('Sky')[1] +extensionIn
    # else:
    #     binaryImagePath = nameIn+'Binary'+extensionIn

    directoryCheck(binaryImagePath)
    cv2.imwrite(binaryImagePath, Image_Reshaped)

    return Image_Reshaped


def Binary_Image_Writer(Pixel_Row ,Image_Shape , Des_Path):
    # Designed to return a binary image and write the said image to a given path
    Image_Reshaped = []
    Pixel_Row_255 = Pixel_Row.astype(float)*255
    Pixel_Row_Transpose = np.transpose(Pixel_Row_255)
    Image_Reshaped_Pre = np.asarray(Pixel_Row_Transpose.reshape((Image_Shape[0], Image_Shape[1])))
    Image_Reshaped     = np.zeros((Image_Shape[0], Image_Shape[1], 3))

    Image_Reshaped[:, :, 0] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 1] = Image_Reshaped_Pre
    Image_Reshaped[:, :, 2] = Image_Reshaped_Pre

    cv2.imwrite(Des_Path, Image_Reshaped)

    return Image_Reshaped

def  getFileNameAndExtension(pathIn):
    name, ext = os.path.splitext(pathIn)
    return name,ext;

def getCloudOnlyImage(Original_Image_Object, Binary_Image_Object):
    #  Designed to return a image with only the Clouds and rest Black
    Cloud_Pixels_Normalized = Binary_Image_Object.astype(float)/255
    Original_Image_float = Original_Image_Object.astype(float)
    # Multiplying Images
    Only_Clouds = cv2.multiply(Original_Image_float, Cloud_Pixels_Normalized)
    return Only_Clouds

def getSkyOnlyImage(Original_Image_Object, Binary_Image_Object):
    #  Designed to return a image with only the Sky and rest Black
    Sky_Pixels_Binary= np.asarray(Binary_Image_Object, dtype='float32')
    ret, Sky_Pixels_Binary = cv2.threshold(Sky_Pixels_Binary, 10, 255, cv2.THRESH_BINARY_INV)
    Sky_Pixels_Binary = np.asarray(Sky_Pixels_Binary, dtype='float')
    # Recognizing the Sky Pixes and normalizing the sky pixels binary (for multiplication)
    Sky_Pixels_Normalized = Sky_Pixels_Binary/ 255
    Original_Image_float = Original_Image_Object.astype(float)
    # Multiplying Images
    Only_Sky = cv2.multiply(Original_Image_float, Sky_Pixels_Normalized)

    return Only_Sky


# def Cloud_Only_Image_Writer(Original_Image_Object, Binary_Image_Object ,Des_Path):
#     #  Designed to return a image with only the Clouds and rest Black
#     Cloud_Pixels_Normalized = Binary_Image_Object.astype(float)/255
#     Original_Image_float = Original_Image_Object.astype(float)
#     # Multiplying Images
#     Only_Clouds = cv2.multiply(Original_Image_float, Cloud_Pixels_Normalized)
#     cv2.imwrite(Des_Path, Only_Clouds)
#     return Only_Clouds
#
#
# def Sky_Only_Image_Writer(Original_Image_Object, Binary_Image_Object ,Des_Path):
#     #  Designed to return a image with only the Sky and rest Black
#     #
#     Sky_Pixels_Binary= np.asarray(Binary_Image_Object, dtype='float32')
#
#     ret, Sky_Pixels_Binary = cv2.threshold(Sky_Pixels_Binary, 10, 255, cv2.THRESH_BINARY_INV)
#
#     Sky_Pixels_Binary = np.asarray(Sky_Pixels_Binary, dtype='float')
#
#     # Recognizing the Sky Pixes and normalizing the sky pixels binary (for multiplication)
#     Sky_Pixels_Normalized = Sky_Pixels_Binary/ 255
#     Original_Image_float = Original_Image_Object.astype(float)
#
#     # Multiplying Images
#     Only_Sky = cv2.multiply(Original_Image_float, Sky_Pixels_Normalized)
#     cv2.imwrite(Des_Path, Only_Sky)
#     return Only_Sky
#
# def dataFolderCleaner(dailyDownloadLocation):
#     if os.path.exists(dailyDownloadLocation):
#          shutil.rmtree(dailyDownloadLocation)
#     os.makedirs(dailyDownloadLocation)
#

# def downloadFile(url,localLocation):
#     directoryCheck(localLocation)
#     urllib.request.urlretrieve(url,localLocation)
#
def directoryCheck(outputPath):
    directoryIn = os.path.dirname(outputPath)
    if not os.path.exists(directoryIn):
        os.makedirs(directoryIn)
#
# def unzipFile(localLocation,dailyDownloadLocation):
#   destinationName = os.path.dirname(localLocation)+'/GASP.complete'
#   if os.path.exists(destinationName):
#       print("The folder does exist")
#       shutil.rmtree(destinationName)
#   else:
#       print("The folder does not exist")
#   unzipper(localLocation)
#   directoryPaths,directoryNames,directoryFiles=  gainDirectoryInfo(dailyDownloadLocation)
#   sourceName = dailyDownloadLocation + directoryNames[0]
#   os.rename(sourceName, destinationName)
#
#
# def unzipper(localLocation):
#   tar = tarfile.open(localLocation, "r:")
#   tar.extractall(os.path.dirname(localLocation))
#   tar.close()


# def gainDirectoryInfoFromPath(dailyDownloadLocation):
#     directoryPaths = []
#     directoryNames = []
#     directoryFiles = []
#     for (dirpath, dirnames, filenames) in walk(dailyDownloadLocation):
#         directoryPaths.extend(dirpath)
#         directoryNames.extend(dirnames)
#         directoryFiles.extend(filenames)
#
#     return directoryPaths,directoryNames,directoryFiles;

# def gainDirectoryInfo(dailyDownloadLocation):
#     directoryPaths = []
#     directoryNames = []
#     directoryFiles = []
#     for (dirpath, dirnames, filenames) in walk(dailyDownloadLocation):
#         directoryPaths.extend(dirpath)
#         directoryNames.extend(dirnames)
#         directoryFiles.extend(filenames)
#
#     return directoryPaths,directoryNames,directoryFiles;
#
#
# def fileDeleter(fileDirectory,fileExtension):
#     files = os.listdir(fileDirectory)
#     for item in files:
#         if item.endswith(fileExtension):
#             os.remove(os.path.join(fileDirectory, item))
#
#
# def fileDeleterFromPath(pathIn):
#     if os.path.exists(pathIn):
#         os.remove(pathIn)
#
# def getLocationList(directory, suffix=".csv"):
#     filenames = listdir(directory)
#     dateList = [ filename for filename in filenames if filename.endswith( suffix ) ]
#     return sorted(dateList)
#
# def sendCopy(seekPath,sendPath):
#
#     fileNameSend  = os.path.basename(seekPath)
#     directorySend = os.path.dirname(sendPath)
#     sendPathAddress = os.path.join(directorySend,fileNameSend)
#     directoryCheck(sendPathAddress)
#     # fileDeleterFromPath(sendPathAddress)
#
#     try:
#         copyfile(seekPath,    sendPathAddress)
#     except IOError as e:
#         print("Error: %s - Trying Again" % e)
#     try:
#         copyfile(seekPath,sendPathAddress)
#     except IOError as e:
#         print("Unable to copy file. %s" % e)
#
# def getUniqueList(mergedPre):
#     merged = []
#     seen = set()
#     for d in mergedPre:
#         t = tuple(d.items())
#         if t not in seen:
#             seen.add(t)
#             merged.append(d)
#     return merged
#
# def getListDictionaryFromPathAsIs(dirPath):
#
#     print('Reading from :' + dirPath)
#     reader = csv.DictReader(open(dirPath))
#     reader = list(reader)
#     return reader;
#
# def getListDictionary(inputPath,nodeID):
#     reader = csv.DictReader(open(inputPath))
#     reader = list(reader)
#     reader = [v for v in reader if v['node_id'] == nodeID]
#     keys = ['timestamp','node_id','subsystem','sensor','parameter','value_raw','value_hrf']
#     return reader,keys;
#
# def writeCSV(reader,keys,outputPath):
#     directoryCheck(outputPath)
#     csvWriter(outputPath,reader,keys)
#
#
# def csvWriter(writePath,organizedData,keys):
#     if len(organizedData)>0:
#         with open(writePath,'w') as output_file:
#             writer = csv.DictWriter(output_file, fieldnames=keys)
#             writer.writeheader()
#             writer.writerows(organizedData)
#
# def nanCorrection(organizedData,keys):
#     organizedDataFinal = []
#     for  organizedDataLine in organizedData:
#          organizedDataNaN = nanCorrectionSingleDictionary(organizedDataLine,keys)
#          organizedDataFinal.append(organizedDataNaN)
#     # print(organizedDataFinal)
#     return organizedDataFinal
#
# def nanCorrectionSingleDictionary(organizedDataLine,keysIn):
# #  Modyfying Each item for a single Dictionary
#     dictNaN = {}
#     for keyIn in keysIn:
#             dictNaN[keyIn] =  'NaN'
#
#     for key, value in organizedDataLine.items():
#         dictNaN[key] = value
#
#     return dictNaN

def timeTaken(message,start):
    print(message+str(time.time()-start)+' Seconds')


def gzExtractor(gzLocation):
    os.system('gzip -f ' +gzLocation)

if __name__ == "__main__":
   main()
