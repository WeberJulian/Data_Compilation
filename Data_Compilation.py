# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 19:05:26 2017

Data Compilation

@author: julian weber
"""

from PIL import Image as pl
import numpy as np
import glob, os, sys
import random as rd
import time as ti

t1 = ti.clock()

print("Initialisation...")

###################  Variables  #######################

W = 200
L = 200
size = W, L                 #Size of output

nbTotal = 8000

try:
    if '' != sys.argv[1]:
        nbTotal = int(sys.argv[1])
except:
    pass
 
  
collection = "Collection_"
fileName = "id_"

rotation = True             #Enable 90° rotation
compression = 0       #From 0 to 1, 0 means no compression 

outformat = "L"

imb = pl.open("Base.bmp")  
imo = pl.open("Out.bmp")
imo = imo.convert(outformat)
sizeInf = imb.getbbox()
baseW = abs(sizeInf[0] - sizeInf[2])
baseH = abs(sizeInf[1] - sizeInf[3])

xDomain = 0, baseW - size[0]
yDomain = 0, baseH - size[1]


###################  Program  #######################

print("Creating path...")

i = 1
while os.path.exists(collection + str(i)):
    i = i + 1
collection = collection + str(i)
    
if not os.path.exists(collection):
        os.makedirs(collection)

os.makedirs(collection + "/Base")
os.makedirs(collection + "/Out")

print("Generating data...")



for k in range(nbTotal):
    x = rd.randint(xDomain[0], xDomain[1])
    y = rd.randint(yDomain[0], yDomain[1])
    r = rd.randint(0,3)
    box = x, y, x + size[0], y + size[1]
    temp1 = imb.crop(box)
    temp2 = imo.crop(box)
    
    for i in range(r):
        temp1 = temp1.transpose(pl.ROTATE_90)
        temp2 = temp2.transpose(pl.ROTATE_90)
        
    if compression != 0 :
        c = 1 - compression
        temp1 = temp1.resize((int(size[0]*c), int(size[1]*c)))
        temp2 = temp2.resize((int(size[0]*c), int(size[1]*c)))
        
    path = collection + "/Base/" + fileName + str(k) + ".jpg"
    temp1.save(path)
    path = collection + "/Out/" + fileName + str(k) + ".jpg"
    temp2.save(path)
    
    if k * 10 // nbTotal == k * 10 / nbTotal:
        print(str(k * 100 / nbTotal) + "%")
    
print("Writing log...")

separator = "\n"

log = open(collection + "/log.txt", 'w')
log.write("========== Settings =========" + separator + separator)
log.write("Crop size : "+str(W)+"x"+str(L) + separator)
log.write("Number of outputs : "+ str(nbTotal) + separator)
log.write("Rotations : "+ str(rotation) + separator)
log.write("Resize : "+ str(compression) + separator)
log.write("Output format : "+ str(outformat) + separator)
log.close()


t2 = ti.clock()
print("Done in " + str(int(t2-t1)) + " secs")
