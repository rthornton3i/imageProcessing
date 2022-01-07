import numpy as np
#import matplotlib.pyplot as plt

import encryption_Functions as ef
import imageProcessing_Functions as ipf

fileName = 'carina.bmp'

##############################################################################

encName = 'cameraman.png'
[img,imgSize,origin] = ipf.imgRead(encName,mode="L")

binImg = ef.img2bin(img,digits=8)


##############################################################################

#msgName = 'obama.txt'

#[msg,length] = ef.msgRead(msgName)

#digits = ef.msgEncrypt(msg,fileName,numDigits=1)
#newMsg = ef.msgDecrypt(fileName,numDigits=1,msgDigits=digits,char=length)

#ef.msgWrite(msgName,newMsg)