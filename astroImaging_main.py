#from PIL import Image as im
#import numpy as np
import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf
import astroProcessing_Functions as apf

fileName = 'stars.jpg'

[img,imgSize] = ipf.imgRead(fileName)

imgBW = ipf.imgBandW(img)

imgBW1 = ipf.imgCrop(imgBW,[380,480],[450,550])
imgBW2 = ipf.imgCrop(imgBW,[400,500],[450,550])

[imgThresh1,starIDs1,numStars1] = apf.starID_ShpInt(imgBW1,neighbor=8,backThresh=125,kernel=(11,11),exclude=False)
[imgThresh2,starIDs2,numStars2] = apf.starID_ShpInt(imgBW2,neighbor=8,backThresh=125,kernel=(11,11),exclude=False)

[imgStars,starAdjs,numStars] = apf.starID_Neighbors(imgBW,neighbor=8,starThresh=250)

ipf.imgWrite(imgThresh1,'stars_thresh1.bmp',"L")
ipf.imgWrite(imgThresh2,'stars_thresh2.bmp',"L")

ipf.imgWrite(imgStars,'stars_stars.bmp',"L")

plt.close()
plt.subplot(121),plt.imshow(imgThresh1,interpolation="none")
plt.subplot(122),plt.imshow(imgThresh2,interpolation="none")