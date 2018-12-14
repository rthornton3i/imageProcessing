import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#ORIGINAL IMAGE
img = cv.imread('cameraman.png')
#origImg = cv.imshow('img',img)

ht, wt, ch = img.shape

#Scale
scale = cv.resize(img,(2*wt,2*ht),interpolation=cv.INTER_CUBIC)

#Translate
transMatrix = np.float32([[1,0,100],[0,1,50]])
trans = cv.warpAffine(img,transMatrix,(wt,ht))

#Rotate
rotMatrix = cv.getRotationMatrix2D((wt/2,ht/2),90,1)
rot = cv.warpAffine(img,rotMatrix,(wt,ht))

#Affine
pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])

affMatrix = cv.getAffineTransform(pts1,pts2)
aff = cv.warpAffine(img,affMatrix,(wt,ht))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(aff),plt.title('Output')
plt.show()

#NEW IMAGE
#newImg = cv.imshow('rot',rot)

#cv.destroyAllWindows()
#plt.close()