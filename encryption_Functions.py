import numpy as np

#Character to Binary
def char2bin(msg,digits=8):
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

#Encrypt Message to Image
def msg2img(imgBin,binMsg,imgSize,numDigits=1):
    numEl = np.prod(imgSize)
    
    img = imgBin
    
    imgIndex = 0
    for letter in binMsg:   
        if imgIndex >= numEl:
            break

        for n in range(0,len(letter),numDigits):
            if imgIndex >= numEl:
                break
            
            pixel = img[imgIndex][:-numDigits] + letter[n:n+numDigits]
            img[imgIndex] = pixel
        
            imgIndex += 1
    
    return img

#Decrypt Message in Image
def img2msg(imgBin,digits=8,char=100,numDigits=1):
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