import math
import numpy as np
#import matplotlib.pyplot as plt

def spiralStep(loopCount):
    dR_Array = []
    dC_Array = []
    
    stepSizeA = (loopCount*2)+1
    stepSizeB = (loopCount*2)-1
    
    for n in range(loopCount-1,-loopCount,-1):       
        dR_Array.append(n)
    for n in range(stepSizeA):
        dR_Array.append(-loopCount)
    for n in range(-loopCount+1,loopCount):       
        dR_Array.append(n)
    for n in range(stepSizeA):
        dR_Array.append(loopCount)
        
    for m in range(stepSizeB):
        dC_Array.append(loopCount)
    for m in range(loopCount,-loopCount-1,-1):       
        dC_Array.append(m)
    for m in range(stepSizeB):
        dC_Array.append(-loopCount)
    for m in range(-loopCount,loopCount+1):       
        dC_Array.append(m)
    
    rcArray = list(zip(dR_Array,dC_Array))
    
    return rcArray

def vec2vec(vector1,angRad):
    vector1 = [[vector1[0]],[vector1[1]]][::-1]
    rotDir = angRad / abs(angRad)
    
    rotMat = [[math.cos(angRad),-math.sin(angRad)*rotDir],
              [math.sin(angRad)*rotDir,math.cos(angRad)]]
    
    vector2 = np.matmul(rotMat,vector1)[::-1]
    
    return vector2

def vec2ang(vector1,vector2):
    vector1 = vector1[::-1]
    vector2 = vector2[::-1]
    
    vecMag1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    vecMag2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    
    rotDir = np.cross(vector1,vector2) / abs(np.cross(vector1,vector2))
    
    angRad = np.arccos(np.dot(vector1,vector2) / np.dot(vecMag1,vecMag2)) * rotDir
    
    return angRad