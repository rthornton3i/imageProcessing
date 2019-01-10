#from PIL import Image as im
#import numpy as np
import matplotlib.pyplot as plt

import imageProcessing_Functions as ipf
import astroProcessing_Functions as apf

fileName = 'stars.jpg'

[img,imgSize] = ipf.imgRead(fileName)

imgBW = ipf.imgBandW(img)

imgBW1 = ipf.imgCrop(imgBW,[400,550],[950,1100])
imgBW2 = ipf.imgCrop(imgBW,[375,525],[950,1100])
#ipf.imgWrite(imgBW1,'stars_crop.bmp',"L")

#[imgThresh1,starIDs1,numStars1] = apf.starID_ShpInt(imgBW1,neighbor=8,backThresh=125,kernel=(11,11),exclude=False)
#[imgThresh2,starIDs2,numStars2] = apf.starID_ShpInt(imgBW2,neighbor=4,backThresh=125,kernel=(11,11),exclude=False)
#ipf.imgWrite(imgThresh1,'stars_thresh1.bmp',"L")
#ipf.imgWrite(imgThresh2,'stars_thresh2.bmp',"L")

#plt.close()
#plt.subplot(121),plt.imshow(imgThresh1,interpolation="none")
#plt.subplot(122),plt.imshow(imgThresh2,interpolation="none")

[imgStars1,starAdjs1,numStars1] = apf.starID_Neighbors(imgBW1,neighbor=8,starThresh=250)
[imgStars2,starAdjs2,numStars2] = apf.starID_Neighbors(imgBW2,neighbor=8,starThresh=250)
ipf.imgWrite(imgStars1,'stars_stars1.bmp',"L")
ipf.imgWrite(imgStars2,'stars_stars2.bmp',"L")

plt.close()
plt.subplot(121),plt.imshow(imgStars1,interpolation="none")
plt.subplot(122),plt.imshow(imgStars2,interpolation="none")