import cv2 as cv
import numpy as np
#import matplotlib.pyplot as plt

#Number and Identify Stars
def starsID(imgBW,nearNeighbors=4,backThresh=125,starThresh=125,kernel=(5,5)):
    imgSize = np.shape(imgBW)
    
    kVert = int((kernel[0]-1)/2)
    kHorz = int((kernel[1]-1)/2)
    
    imgBW[0:kVert-1,:] = 0
    imgBW[-kVert:-1,:] = 0
    imgBW[:,0:kHorz-1] = 0
    imgBW[:,-kHorz:-1] = 0
    
    ret1,imgThresh = cv.threshold(imgBW,backThresh,255,cv.THRESH_TOZERO)
    ret2,imgStars = cv.threshold(imgBW,starThresh,255,cv.THRESH_BINARY)
    
    near4 = [[0,1],[-1,0],[0,-1],[1,0]]
    near8 = [[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[1,-1],[-1,-1]]
    
    if nearNeighbors == 4:
        near = near4
    elif nearNeighbors == 8:
        near = near8
    else:
        near = near4
       
    starList = []
    for row in range(1,imgSize[0]-1):
        for colm in range(1,imgSize[1]-1):
            curVal = imgThresh[row,colm]
            if curVal > 0:
                nearVals = [(row+index[0],colm+index[1],imgThresh[row+index[0],colm+index[1]]) for index in near8]
                
                maxIndex = max(nearVals,key=lambda x:x[2])
                
                if maxIndex[2] > curVal:
                    while maxIndex[2] > curVal:
                        tempRow = maxIndex[0]
                        tempColm = maxIndex[1]
                        curVal = imgThresh[tempRow,tempColm]
                        
                        nearVals = [(tempRow+index[0],tempColm+index[1],imgThresh[tempRow+index[0],tempColm+index[1]]) for index in near8]
                
                        maxIndex = max(nearVals,key=lambda x:x[2])
                        
                    if (tempRow,tempColm) not in starList:
                        starList.append((tempRow,tempColm))
                else:
                    if (row,colm) not in starList:
                        starList.append((row,colm))
    
    dupStars = []
    for star in starList:
        nearVals = [(star[0]+index[0],star[1]+index[1]) for index in near8]
        
        dupStars = [nearVal for nearVal in nearVals if nearVal in starList]
                
        for dupStar in dupStars:
            nearVals = [(dupStar[0]+index[0],dupStar[1]+index[1]) for index in near]
            
            for nearVal in nearVals:
                if nearVal in starList and nearVal not in dupStars and (nearVal[0],nearVal[1]) != star:
                    dupStars.append(nearVal)
        
        for dupStar in dupStars:
            starList.remove(dupStar)
    
    numStars = len(starList)
    
    starShapes = []
    for star in starList:
        starShape = [imgBW[star[0]+n,star[1]+m] for n in range(-kVert,kVert+1) for m in range(-kHorz,kHorz+1)]
        starShapes.append(starShape)
    
    return [imgStars,imgThresh,starList,starShapes,numStars]