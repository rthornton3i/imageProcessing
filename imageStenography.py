#import cv2 as cv
#import numpy as np
#import matplotlib.pyplot as plt

import imageProcessing_Functions as imf
import encryption_Functions as ef

def imgEncrypt(msg,fileName,numDigits=1,imgDigits=8,msgDigits=8):
    [binMsg,msgDigits] = ef.char2bin(msg,msgDigits)
    
    [img,imgSize] = imf.imgRead(fileName)    
    
    imgBin = imf.imgBinary(img,imgDigits)
    
    imgMsg = ef.msg2img(imgBin,binMsg,imgSize,numDigits)
    
    imgDec = imf.imgDecimal(imgMsg,imgSize)
    
    imf.imgWrite(fileName[:fileName.find('.')] + '_encrypt.bmp',imgDec)
    
    return msgDigits

def imgDecrypt(fileName,numDigits=1,imgDigits=8,msgDigits=8,char=30):
    [img,imgSize] = imf.imgRead(fileName[:fileName.find('.')] + '_encrypt.bmp')    

    imgBin = imf.imgBinary(img,imgDigits)
    
    binMsg = ef.img2msg(imgBin,msgDigits,char,numDigits)
    msg = ef.bin2char(binMsg)
    
    return msg

def msgRead(msgName):
    file = open(msgName,'r',encoding='utf-8',errors='ignore')
    msg = file.readlines()
    file.close()
    
    msg = ' '.join(msg)
    length = len(msg)
    
    return [msg,length]

def msgWrite(msgName,msg):
    file = open(msgName[:msgName.find('.')] + '_decrypt.txt','w')
    file.write(msg)
    file.close()

fileName = 'lakeandballoon.bmp'
msgName = 'obama.txt'

[msg,length] = msgRead(msgName)

digits = imgEncrypt(msg,fileName,numDigits=1)
newMsg = imgDecrypt(fileName,numDigits=1,msgDigits=digits,char=length)

msgWrite(msgName,newMsg)