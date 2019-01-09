from PIL import Image as im
import numpy as np
#import matplotlib.pyplot as plt

#Read Image
def imgRead(fileName,mode="RGB"):
    img = np.asarray(im.open(fileName).convert(mode))
    imgSize = np.shape(img)
                
    return [img,imgSize]

#Write Image
def imgWrite(img,fileName,mode="RGB"):
    tempImg = im.fromarray(img).convert(mode)
    tempImg.save(fileName,quality=100)

###############################################################################

#Convert to B&W:
def imgBandW(img):
    imgBW = np.mean(img,axis=2)
    
    return imgBW

#Threshold
def imgThreshold(img,lowVal=0,highVal=255):
    tempImg = img
    imgSize = np.shape(img)
    
    for row in range(imgSize[0]):
        for colm in range(imgSize[1]):
            if img[row,colm] >= highVal:
                pixVal = 255
            elif img[row,colm] <= lowVal:
                pixVal = 0
            else:
                pixVal = img[row,colm]
                
            tempImg[row,colm] = pixVal
    	
    return tempImg

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
    
    return transImg    
#Rotate
def imgRotate(img):
    ht, wt = img.shape
    
    rotMatrix = cv.getRotationMatrix2D((wt/2,ht/2),90,1)
    rot = cv.warpAffine(img,rotMatrix,(wt,ht))
    
    return rot
    
#Scale
def imgScale(img):
    ht, wt, ch = img.shape
    
    scale = cv.resize(img,(2*wt,2*ht),interpolation=cv.INTER_CUBIC)
    
    return scale

#Translate
def imgTranslate(img):
    ht, wt, ch = img.shape
    
    transMatrix = np.float32([[1,0,100],[0,1,50]])
    trans = cv.warpAffine(img,transMatrix,(wt,ht))
    
    return trans

#Affine
def imgAffine(img,startPts,endPts):
    ht, wt, ch = img.shape
    
    pts1 = np.float32(startPts)
    pts2 = np.float32(endPts)
    
    affMatrix = cv.getAffineTransform(pts1,pts2)
    aff = cv.warpAffine(img,affMatrix,(wt,ht))
    
    return aff

#Perspective
def imgPerspective(img,pts):
    ht, wt, ch = img.shape
    
    pts.sort(key=lambda x: x[0])

    ptsTop = pts[0:2]
    ptsTop.sort(key=lambda x: x[1])
    ptsBot = pts[2:4]
    ptsBot.sort(key=lambda x: x[1])
    
    pts = []
    pts.extend(ptsTop)
    pts.extend(ptsBot)
    print(pts)
    
    pts1 = np.float32(pts)
    pts2 = np.float32([[0,0],[0,wt],[ht,0],[ht,wt]])
    
    persMatrix = cv.getPerspectiveTransform(pts1,pts2)
    pers = cv.warpPerspective(img,persMatrix,(wt,ht))
    
    return pers

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