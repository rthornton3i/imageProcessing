#from PIL import Image as im
import numpy as np
#import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf

def starID_Neighbors(imgBW,neighbor=8,starThresh=250):
    imgSize = np.shape(imgBW)
    
    near4 = [[0,1],[-1,0],[0,-1],[1,0]]
    near8 = [[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[1,-1],[-1,-1]]
    
    if neighbor == 4:
        near = near4
    elif neighbor == 8:
        near = near8
    else:
        near = near8
    
    imgBW[0,:] = 0
    imgBW[-1,:] = 0
    imgBW[:,0] = 0
    imgBW[:,-1] = 0
    
    imgStars = ipf.imgThreshold(imgBW,lowVal=starThresh,highVal=starThresh)
    
    starList = starPixels(imgStars,imgSize,near)
    numStars = len(starList)
    
    starCenters = []
    for star in starList:
        starCenters.append(starCoM(star))
        
    starAdjs = []
    for star in starCenters:
        nearStars = starNeighbors(star,imgStars)
        starAdjs.append(nearStars)
    
#    starIDs = list(zip(starShapes,starInts,starCenters))
#    starIDs = sorted(starIDs,key=lambda x:x[1])
    
    return [imgStars,starAdjs,numStars]
    
def starID_ShpInt(imgBW,neighbor=8,backThresh=125,kernel=(9,9),exclude=False):
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

def starNeighbors(star,img):
    nearStars = []
    
    row = star[0]
    colm = star[1]
    dRow = 0
    dColm = -1
    
    for i in range(max(X, Y)**2):
        if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
            print (x, y)
            # DO STUFF...
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy
    
    return nearStars    
    
def starAlign(mainStars,secStars):
    pass