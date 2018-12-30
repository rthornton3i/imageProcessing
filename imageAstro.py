#import cv2 as cv
#import numpy as np
#import math
import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf
import astroProcessing_Functions as apf

fileName = 'stars.jpg'
[img,imgSize] = ipf.imgRead(fileName)
imgBW = ipf.imgBandW(img)
imgBW = ipf.imgCrop(imgBW,[420,500],[450,560])

[imgStars,imgThresh,starList,stars,numStars] = apf.starsID(imgBW,nearNeighbors=4,backThresh=125,starThresh=125,kernel=(5,5))
ipf.imgWrite(imgStars,'stars_stars.bmp',numCh=1)
ipf.imgWrite(imgThresh,'stars_thresh.bmp',numCh=1)

plt.close()
plt.imshow(imgThresh)
y,x = zip(*starList)
plt.scatter(x, y)

print(numStars)