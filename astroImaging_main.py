#from PIL import Image as im
#import numpy as np
#import math
#import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf
import astroProcessing_Functions as apf

fileName = 'stars.jpg'
#fileName = 'lakeandballoon.bmp'

[img,imgSize] = ipf.imgRead(fileName)

imgBW = ipf.imgBandW(img)
#imgBW = ipf.imgCrop(imgBW,[315,365],[350,400])
imgBW = ipf.imgCrop(imgBW,[400,500],[450,550])

[imgThresh,numStars] = apf.starID(imgBW,neighbor=4,backThresh=100,kernel=(5,5))
ipf.imgWrite(imgThresh,'stars_thresh.bmp',"L")

print(numStars)