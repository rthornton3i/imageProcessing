#from PIL import Image as im
import numpy as np
import math
#import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf
import miscellaneous_Functions as mf

def starID_Neighbors(imgBW,neighbor=8,starThresh=250,compStars=5,kernel=(11,11),exclude=True):
    imgSize = np.shape(imgBW)
    
    near4 = [[0,1],[-1,0],[0,-1],[1,0]]
    near8 = [[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[1,-1],[-1,-1]]
    
    if neighbor == 4:
        near = near4
    elif neighbor == 8:
        near = near8
    else:
        near = near8
    
    kVert = int((kernel[0]-1)/2)
    kHorz = int((kernel[1]-1)/2)
    
    imgBW[0:kVert,:] = 0
    imgBW[-kVert:,:] = 0
    imgBW[:,0:kHorz] = 0
    imgBW[:,-kHorz:] = 0
    
    imgStars = ipf.imgThreshold(imgBW,lowVal=starThresh,highVal=starThresh)
    
    starList = starPixels(imgStars,imgSize,near)
    numStars = len(starList)
    
    starCenters = []
    for star in starList:
        starCenters.append(starCoM(star))
        
    starInts = []
    for star in starCenters:
        [starShape,starInt] = starGeometry(star,imgStars,kernel,near,exclude)
        starInts.append(starInt)
    
    starIDs = list(zip(starInts,starCenters))
    starIDs = sorted(starIDs,key=lambda x:x[0])
    
    starCenters = []
    starCenters = [star[1] for star in starIDs]
    
    starAdjs = []
    for star in starCenters[-compStars:]:
        nearStars = starNeighbors(star,starCenters)
        starAdjs.append(nearStars)
        
    starAdjs = np.flip(starAdjs,axis=0)
    starCenters = np.asarray(starCenters)
    
    return [imgStars,starAdjs,starCenters,numStars]
    
def starID_ShpInt(imgBW,neighbor=8,backThresh=125,kernel=(11,11),exclude=False):
    imgSize = np.shape(imgBW)
    
    near4 = [[0,1],[-1,0],[0,-1],[1,0]]
    near8 = [[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[1,-1],[-1,-1]]
    
    if neighbor == 4:
        near = near4
    elif neighbor == 8:
        near = near8
    else:
        near = near8
    
    kVert = int((kernel[0]-1)/2)
    kHorz = int((kernel[1]-1)/2)
    
    imgBW[0:kVert,:] = 0
    imgBW[-kVert:,:] = 0
    imgBW[:,0:kHorz] = 0
    imgBW[:,-kHorz:] = 0
    
    imgThresh = ipf.imgThreshold(imgBW,lowVal=backThresh)
    
    starList = starPixels(imgThresh,imgSize,near)
    numStars = len(starList)
    
    starCenters = []
    for star in starList:
        starCenters.append(starCoM(star))
        
    starShapes = []
    starInts = []
    for star in starCenters:
        [starShape,starInt] = starGeometry(star,imgThresh,kernel,near,exclude)
        
        starShapes.append(starShape)
        starInts.append(starInt)
    
    starIDs = list(zip(starShapes,starInts,starCenters))
    starIDs = sorted(starIDs,key=lambda x:x[1])
    
    return [imgThresh,starIDs,numStars]

def starPixels(img,imgSize,near):    
    starList = []
    pixels = []
    for row in range(1,imgSize[0]-1):
        for colm in range(1,imgSize[1]-1):
            curVal = img[row,colm]
            if curVal > 0 and (row,colm) not in pixels:
                star = (row,colm)
                pixels.append(star)
                
                nearVals = [(row+index[0],colm+index[1],img[row+index[0],colm+index[1]]) for index in near]
                tempStars = [(nearVal[0],nearVal[1]) for nearVal in nearVals if nearVal[2] > 0]
                
                for tempStar in tempStars:
                    pixels.append(tempStar)
                    nearVals = [(tempStar[0]+index[0],tempStar[1]+index[1],img[tempStar[0]+index[0],tempStar[1]+index[1]]) for index in near]
                    
                    for nearVal in nearVals:
                        if nearVal[2] > 0 and (nearVal[0],nearVal[1]) not in tempStars and (nearVal[0],nearVal[1]) not in pixels:
                            tempStars.append((nearVal[0],nearVal[1]))
                
                tempStars.append(star)
                starList.append(tempStars)    
    
    return starList
    
def starCoM(star):
    rows = [pixel[0] for pixel in star]
    colms = [pixel[1] for pixel in star]
    
    rowCenter = int(np.round(np.mean(rows)))
    colmCenter = int(np.round(np.mean(colms)))
    
    starCenter = (rowCenter,colmCenter)
    
    return starCenter
    
def starGeometry(star,img,kernel,near,exclude):
    kVert = int((kernel[0]-1)/2)
    kHorz = int((kernel[1]-1)/2)
    
    starShape = [img[star[0]+n,star[1]+m] for n in range(-kVert,kVert+1) for m in range(-kHorz,kHorz+1)]
    starShape = np.reshape(starShape,kernel)
    starInt = sum(sum(starShape)) 
    
    if exclude == True:
        tempArray = np.zeros((kernel[0]+2,kernel[1]+2))
        tempArray[1:-1,1:-1] = starShape
        starSize = np.shape(tempArray)
    
        row = kVert + 1
        colm = kHorz + 1
        starCenter = (row,colm,tempArray[row,colm])
        
        nearVals = [(row+index[0],colm+index[1],tempArray[row+index[0],colm+index[1]]) for index in near]
        tempStars = [nearVal for nearVal in nearVals if nearVal[2] > 0]
        
        for tempStar in tempStars:
            nearVals = [(tempStar[0]+index[0],tempStar[1]+index[1],tempArray[tempStar[0]+index[0],tempStar[1]+index[1]]) for index in near]
            
            for nearVal in nearVals:
                if nearVal[2] > 0 and nearVal not in tempStars and nearVal != starCenter:
                    tempStars.append(nearVal)
        
        tempStars.append(starCenter)
        
        for row in range(starSize[0]):
            for colm in range(starSize[1]):
                curStar = (row,colm,tempArray[row,colm])
                if curStar not in tempStars:
                    tempArray[row,colm] = 0
        
        starShape = tempArray
        starInt = sum(sum(starShape)) 
                
    return [starShape,starInt]

def starNeighbors(star,starCenters):
    nearStars = []
    
    row = star[0]
    colm = star[1]
    
    loopCount = 1    
    starCount = 0
    while True:
        rcArray = mf.spiralStep(loopCount)
        
        for rc in rcArray:
            tempRow = row + rc[0]
            tempColm = colm + rc[1]
            
            if (tempRow,tempColm) in starCenters:
                starCount += 1
                nearStars.append((rc[0],rc[1]))
            
            if starCount == 10:
                return nearStars
        
        loopCount += 1
    
def starMatch(mainAdjs,secAdjs):
    avgDists = []
    
    secIndex = 0
    for secStar in secAdjs:
        mainIndex = 0
        for mainStar in mainAdjs:
            minDists = [starNearest(secAdjStar,mainStar) for secAdjStar in secStar]
            
            medDist = np.median(minDists)
            stdDist = np.std(minDists)
            
            avgDist = np.mean([dist for dist in minDists if abs(medDist - dist) < (stdDist * 2)])
            avgDist = 0.0 if np.isnan(avgDist) else avgDist
            
            avgDists.append((mainIndex,secIndex,avgDist))
            
            mainIndex += 1
        secIndex += 1
    
    return avgDists

def starNearest(testStar,nearStars):
    dists = []
    for nearStar in nearStars:
        dist = math.sqrt((nearStar[0]-testStar[0])**2 + (nearStar[1]-testStar[1])**2)
        dists.append(dist)
        
    index,value = min([(index,value) for index,value in enumerate(dists)],key=lambda x:x[1]) 
    
    return value    