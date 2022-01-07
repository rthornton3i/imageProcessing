import numpy as np

import imageProcessing_Functions as ipf

def imgEncrypt(encImg,fileName,numDigits=1,imgDigits=8,encDigits=8):    
    [img,imgSize,origin] = ipf.imgRead(fileName)    
    [imgBin_Enc,digits_Enc] = img2bin(img,imgDigits)
    
    [imgBin,digits] = img2bin(encImg,encDigits)
    
    imgMsg = msg2img(imgBin,binMsg,imgSize,numDigits)
    
    imgDec = bin2img(imgMsg,imgSize)
    
    ipf.imgWrite(fileName[:fileName.find('.')] + '_encrypt.bmp',imgDec)
    
    return msgDigits

def imgDecrypt(fileName,numDigits=1,imgDigits=8,encDigits=8,char=30):
    [img,imgSize,origin] = ipf.imgRead(fileName[:fileName.find('.')] + '_encrypt.bmp')    

    imgBin = ipf.imgBinary(img,imgDigits)
    
    binMsg = img2msg(imgBin,encDigits,char,numDigits)
    msg = bin2char(binMsg)
    
    return msg

def msgEncrypt(msg,fileName,numDigits=1,imgDigits=8,msgDigits=8):
    [binMsg,msgDigits] = char2bin(msg,msgDigits)
    
    [img,imgSize,origin] = ipf.imgRead(fileName)    
    
    imgBin = ipf.imgBinary(img,imgDigits)
    
    imgMsg = msg2img(imgBin,binMsg,imgSize,numDigits)
    
    imgDec = bin2img(imgMsg,imgSize)
    
    ipf.imgWrite(fileName[:fileName.find('.')] + '_encrypt.bmp',imgDec)
    
    return msgDigits

def msgDecrypt(fileName,numDigits=1,imgDigits=8,msgDigits=8,char=30):
    [img,imgSize,origin] = ipf.imgRead(fileName[:fileName.find('.')] + '_encrypt.bmp')    

    imgBin = ipf.imgBinary(img,imgDigits)
    
    binMsg = img2msg(imgBin,msgDigits,char,numDigits)
    msg = bin2char(binMsg)
    
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

#Image to Binary
def img2bin(img,digits):
    imgSize = np.shape(img)
    
    maxDig = len(bin(max(ipf.imgFlatten(img,len(imgSize))))[2:])
    if maxDig > digits:
        digits = maxDig
        
    binImg = []
    for row in range(imgSize[0]):
        for colm in range(imgSize[1]):
            pixVal = img[row,colm]
            
            dec2bin = [bin(pix)[2:].zfill(digits) for pix in pixVal] if len(imgSize) == 3 else bin(pixVal)[2:].zfill(digits)
            
            binImg.append(dec2bin)
            
    binImg = np.reshape(binImg,imgSize)
    
    return [binImg,digits]

#Convert to Decimal
def bin2img(img,imgSize):
    imgDec = []
    for index,value in enumerate(img):
        bin2dec = int(value,2)
        imgDec.append(bin2dec)
    
    imgDec = np.reshape(imgDec,[imgSize[0],imgSize[1],imgSize[2]])
    
    return imgDec
    
#Character to Binary
def char2bin(msg,digits):
    binMsg = []
    for index,value in enumerate(msg):
        dec2bin = bin(ord(value))[2:]
        binMsg.append(dec2bin)
    
    maxDig = len(max(binMsg,key=len)) 
    if maxDig > digits:
        digits = maxDig
    
    for index,value in enumerate(binMsg):
        binMsg[index] = str(value).zfill(digits)
    
    return [binMsg,digits]

#Binary to Character
def bin2char(binMsg):
    msg = []
    for index in binMsg:
        char = chr(int(index,2))
        msg.extend(char)
        
    msg = ''.join(msg)
    
    return msg

#Encrypt Image to Image
def img2img(imgBin,imgBin_Enc,imgSize,numDigits):
    numEl = np.prod(imgSize)
    encImg = imgBin
    
    imgIndex = 0
    for letter in binMsg:   
        if imgIndex >= numEl:
            break

        for n in range(0,len(letter),numDigits):
            if imgIndex >= numEl:
                break
            
            pixel = img[imgIndex][:-numDigits] + letter[n:n+numDigits]
            encImg[imgIndex] = pixel
        
            imgIndex += 1
    
    return encImg
    
#Encrypt Message to Image
def msg2img(imgBin,binMsg,imgSize,numDigits):
    numEl = np.prod(imgSize)
    encImg = imgBin
    
    imgIndex = 0
    for letter in binMsg:   
        if imgIndex >= numEl:
            break

        for n in range(0,len(letter),numDigits):
            if imgIndex >= numEl:
                break
            
            pixel = img[imgIndex][:-numDigits] + letter[n:n+numDigits]
            encImg[imgIndex] = pixel
        
            imgIndex += 1
    
    return encImg

#Decrypt Message in Image
def img2msg(imgBin,digits,char,numDigits):
    length = int(digits*char/numDigits)
    
    bits = []
    for pixel in imgBin[:length]:
        bit = pixel[-numDigits:]
        bits.extend(bit)
    
    bitList = [bit for subBits in bits for bit in subBits]
    
    byte = []
    for index,value in enumerate(bitList):
        if index % digits == 0:
            byte.append(''.join(bits[index:index+digits]))
    
    return byte