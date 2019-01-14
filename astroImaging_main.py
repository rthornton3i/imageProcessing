#from PIL import Image as im
import math
import numpy as np
import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf
import astroProcessing_Functions as apf

fileName = 'stars.jpg'
#fileName = 'carina.bmp'

[img,imgSize,origin] = ipf.imgRead(fileName)

#[transImg,transOrigin] = ipf.imgTranslate(img,[100,200],origin)
#ipf.imgWrite(transImg,'test1.bmp')

rotImg = ipf.imgRotate(img,math.pi/8,origin)
#ipf.imgWrite(rotImg,'test.bmp')

interpImg = ipf.imgInterpolate(rotImg)
ipf.imgWrite(interpImg,'test.bmp')

#imgBW = ipf.imgBandW(img)
#
#imgBW1 = ipf.imgCrop(imgBW,[400,550],[950,1100])
#imgBW2 = ipf.imgCrop(imgBW,[375,525],[950,1100])
#ipf.imgWrite(imgBW1,'stars_crop.bmp',"L")

#[imgThresh1,starIDs1,numStars1] = apf.starID_ShpInt(imgBW1,neighbor=8,backThresh=125,kernel=(11,11),exclude=False)
#[imgThresh2,starIDs2,numStars2] = apf.starID_ShpInt(imgBW2,neighbor=4,backThresh=125,kernel=(11,11),exclude=False)
#ipf.imgWrite(imgThresh1,'stars_thresh1.bmp',"L")
#ipf.imgWrite(imgThresh2,'stars_thresh2.bmp',"L")

#plt.close()
#plt.subplot(121),plt.imshow(imgThresh1,interpolation="none")
#plt.subplot(122),plt.imshow(imgThresh2,interpolation="none")

#[imgStars1,starAdjs1,starCenters1,numStars1] = apf.starID_Neighbors(imgBW1,neighbor=8,starThresh=250,compStars=5,refStars=10,kernel=(11,11),exclude=True)
#[imgStars2,starAdjs2,starCenters2,numStars2] = apf.starID_Neighbors(imgBW2,neighbor=8,starThresh=250,compStars=5,refStars=10,kernel=(11,11),exclude=True)
#
#avgDists = apf.starMatch(starAdjs1,starAdjs2)

#plt.close()
#plt.subplot(121),plt.imshow(imgStars1,interpolation="none")
#plt.subplot(122),plt.imshow(imgStars2,interpolation="none")