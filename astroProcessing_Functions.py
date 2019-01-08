#from PIL import Image as im
import numpy as np
import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf

#Number and Identify Stars
def starID(imgBW,neighbor=4,backThresh=125,kernel=(5,5)):
    imgSize = np.shape(imgBW)
    
    kVert = int((kernel[0]-1)/2)
    kHorz = int((kernel[1]-1)/2)
    
    imgBW[0:kVert,:] = 0
    imgBW[-kVert:,:] = 0
    imgBW[:,0:kHorz] = 0
    imgBW[:,-kHorz:] = 0
    
    imgThresh = ipf.imgThreshold(imgBW,lowVal=backThresh)
    
    starList = starPixels(imgThresh,imgSize,neighbor)
    numStars = len(starList)
    
    starCenters = []
    for star in starList:
        starCenters.append(starCoM(star))
        
    starShapes = []
    for star in starCenters:
        starShape = [imgThresh[star[0]+n,star[1]+m] for n in range(-kVert,kVert+1) for m in range(-kHorz,kHorz+1)]
        starShapes.append(starShape)
    
    plt.close()
    plt.imshow(imgThresh,interpolation="none")
    y,x = zip(*starCenters)
    plt.scatter(x,y)

    return [imgThresh,numStars]

def starPixels(imgThresh,imgSize,neighbor):
    near4 = [[0,1],[-1,0],[0,-1],[1,0]]
    near8 = [[0,1],[-1,0],[0,-1],[1,0],[1,1],[-1,1],[1,-1],[-1,-1]]
    
    if neighbor == 4:
        near = near4
    elif neighbor == 8:
        near = near8
    else:
        near = near8
    
    starList = []
    pixels = []
    for row in range(1,imgSize[0]-1):
        for colm in range(1,imgSize[1]-1):
            curVal = imgThresh[row,colm]
            if curVal > 0 and (row,colm) not in pixels:
                star = (row,colm)
                pixels.append(star)
                
                nearVals = [(row+index[0],colm+index[1],imgThresh[row+index[0],colm+index[1]]) for index in near]
                tempStars = [(nearVal[0],nearVal[1]) for nearVal in nearVals if nearVal[2] > 0]
                
                for tempStar in tempStars:
                    pixels.append(tempStar)
                    nearVals = [(tempStar[0]+index[0],tempStar[1]+index[1],imgThresh[tempStar[0]+index[0],tempStar[1]+index[1]]) for index in near]
                    
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