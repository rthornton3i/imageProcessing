from PIL import Image as im
import math
import numpy as np
#import matplotlib.pyplot as plt

import miscellaneous_Functions as mf

#Read Image
def imgRead(fileName,mode="RGB"):
    img = np.asarray(im.open(fileName).convert(mode))
    imgSize = np.shape(img)
    origin = [int((imgSize[0]-1)/2),int((imgSize[1]-1)/2)]
                
    return [img,imgSize,origin]

#Write Image
def imgWrite(img,fileName,mode="RGB"):
    img = np.uint8(img)
    tempImg = im.fromarray(img).convert(mode)
    tempImg.save(fileName,quality=100)

###############################################################################

#Convert to B&W:
def imgBandW(img):
    imgBW = np.mean(img,axis=2)
    
    return imgBW

#Threshold
def imgThreshold(img,lowVal=0,highVal=255):
    imgSize = np.shape(img)
    imgThresh = np.zeros([imgSize[0],imgSize[1]])
    
    for row in range(imgSize[0]):
        for colm in range(imgSize[1]):
            if img[row,colm] >= highVal:
                pixVal = 255
            elif img[row,colm] <= lowVal:
                pixVal = 0
            else:
                pixVal = img[row,colm]
                
            imgThresh[row,colm] = pixVal
    	
    return imgThresh
    
def imgInterpolate(img,neighbor=8):
    imgSize = np.shape(img)
    interpImg = np.zeros((imgSize[0],imgSize[1])).astype(int) if len(imgSize) == 2 else np.zeros((imgSize[0],imgSize[1],imgSize[2])).astype(int)
    
    near4 = [[0,1],[-1,0],[0,-1],[1,0]]
    near8 = [[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[1,-1],[-1,-1]]
    
    if neighbor == 4:
        near = near4
    elif neighbor == 8:
        near = near8
    else:
        near = near8
        
    for row in range(imgSize[0]):
        for colm in range(imgSize[1]):
            pixVal = img[row,colm]
            nearVals = [(index[0],index[1],img[row+index[0],colm+index[1]]) for index in near]
            
            if pixVal == 0 and np.any(nearVals > 0):
                avgVal = []
                for nearVal in nearVals:
                    tempRow = nearVal[0]
                    tempColm = nearVal[1]
                    
                    val1 = nearVal[2]
                    val2 = [compVal[2] for compVal in nearVals if (compVal[0],compVal[1]) == (-tempRow,-tempColm)]
                
                    interpVal = np.mean((val1,val2))
                    
                    avgVal.append(interpVal)

                pixVal = np.mean(avgVal)                
                
            interpImg[row,colm] = pixVal
            
    return interpImg

###############################################################################

#Flatten
def imgFlatten(img,dims):
    dim = 1
    flatImg = img
    while dims > dim:
        tempImg = [item for subImg in flatImg for item in subImg]
        flatImg = tempImg
        dim += 1
    
    return flatImg

#Unflatten
def imgUnflat(flatImg,imgSize):
    if np.size(imgSize) == 2:
        img = np.reshape(flatImg,[imgSize[0],imgSize[1]])
    elif np.size(imgSize) == 3:
        img = np.reshape(flatImg,[imgSize[0],imgSize[1],imgSize[2]])
        
    return img

###############################################################################

#Crop
def imgCrop(img,rows,colms):
    rows.sort
    colms.sort
    
    cropImg = img[rows[0]:rows[1],colms[0]:colms[1]]
    
    return cropImg

#Transform (Translate/Rotate)
def imgTransform(img,pts1,pts2):
    imgSize = np.shape(img)
    origin = [int((imgSize[0]-1)/2),int((imgSize[1]-1)/2)]
    
    pt1a = pts1[0]
    pt1b = pts1[1]
    pt2a = pts2[0]
    pt2b = pts2[1]
    
    vecPt1a = [origin[0]-pt1a[0],pt1a[1]-origin[1]]
    vecPt1b = [origin[0]-pt1b[0],pt1b[1]-origin[1]]
    
    vecPt2a = [origin[0]-pt2a[0],pt2a[1]-origin[1]]
    vecPt2b = [origin[0]-pt2b[0],pt2b[1]-origin[1]]
    
    return transfImg   
 
#Rotate
def imgRotate(img,rotAng,origin):
    imgSize = np.shape(img)
    rotImg = np.zeros((imgSize[0],imgSize[1])).astype(int) if len(imgSize) == 2 else np.zeros((imgSize[0],imgSize[1],imgSize[2])).astype(int)
    
    for row in range(imgSize[0]):
        for colm in range(imgSize[1]):
            pixVal = img[row,colm]            
            
            row2or = origin[0]-row
            colm2or = colm-origin[1]
            
            rotLoc = mf.vec2vec([row2or,colm2or],rotAng)
            
            rotRow = int(origin[0]-rotLoc[0])
            rotColm = int(origin[1]+rotLoc[1])
            
            if rotRow >= 0 and rotRow < imgSize[0] and rotColm >= 0 and rotColm < imgSize[1]:
                rotImg[rotRow,rotColm] = pixVal
    
    return rotImg

#Translate
def imgTranslate(img,transVector,origin): 
    imgSize = np.shape(img)    
    transImg = np.zeros((imgSize[0],imgSize[1])).astype(int) if len(imgSize) == 2 else np.zeros((imgSize[0],imgSize[1],imgSize[2])).astype(int)
    transOrigin = [origin[0]+transVector[0],origin[1]+transVector[1]]
    
    for row in range(imgSize[0]):
        for colm in range(imgSize[1]):
            transRow = row+transVector[0]
            transColm = colm+transVector[1]
            
            if transRow >= 0 and transRow < imgSize[0] and transColm >= 0 and transColm < imgSize[1]:
                transImg[transRow,transColm] = img[row,colm]

    return [transImg,transOrigin]

###############################################################################

#Convert to Binary (0/1)
def imgBinary(img,digits=8):
    imgSize = np.shape(img)
    numEl = np.prod(imgSize)
    
    img = np.reshape(img,[1,numEl])

    imgBin = []
    for index,value in enumerate(img[0]):
        dec2bin = bin(value)[2:]
        imgBin.append(dec2bin)
    
    maxDig = len(max(imgBin,key=len)) 
    if maxDig > digits:
        digits = maxDig
    
    for index,value in enumerate(imgBin):
        imgBin[index] = str(value).zfill(digits)
        
    return imgBin

#Convert to Decimal
def imgDecimal(img,imgSize):
    imgDec = []
    for index,value in enumerate(img):
        bin2dec = int(value,2)
        imgDec.append(bin2dec)
    
    imgDec = np.reshape(imgDec,[imgSize[0],imgSize[1],imgSize[2]])
    
    return imgDec