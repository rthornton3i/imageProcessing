import numpy as np
import math
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

def vec2vec(vector,angle):
    pass

def vec2ang(vector1,vector2):
    np.dot()
    
    return angRad