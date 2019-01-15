#from PIL import Image as im
import math
import numpy as np
import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf
import astroProcessing_Functions as apf

fileName = 'stars.jpg'
#fileName = 'carina.bmp'

[img,imgSize,origin] = ipf.imgRead(fileName)
img1 = ipf.imgCrop(img,[400,550],[950,1100])
img2 = ipf.imgCrop(img,[375,525],[950,1100])



imgBW1 = ipf.imgBandW(img1)

[imgStars,starAdjs,starCenters,numStars] = apf.starID(imgBW1,neighbor=8,starThresh=250,compStars=3,refStars=15,kernel=(11,11),exclude=True)



imgBW_sec = ipf.imgBandW(img2)
imgBW_sec = ipf.imgThreshold(imgBW_sec,lowVal=75)

[imgStars_sec,starAdjs_sec,starCenters_sec,numStars_sec] = apf.starID(imgBW_sec,neighbor=8,starThresh=250,compStars=3,refStars=15,kernel=(11,11),exclude=True)
transVector = apf.starCompare(starAdjs,starAdjs_sec,starCenters,starCenters_sec,refStars=3)
imgTrans = ipf.imgTranslate(img2,transVector,origin=None)



imgs = []
imgs.append(imgBW1)
imgs.append(imgTrans)
stackImg = ipf.imgStack(imgs,channels=1)



plt.close()
plt.subplot(131),plt.imshow(imgBW1,interpolation="none")
plt.subplot(132),plt.imshow(imgTrans,interpolation="none")
plt.subplot(133),plt.imshow(stackImg,interpolation="none")