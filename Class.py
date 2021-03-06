# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 16:28:58 2017
@author: julian weber
"""

from PIL import Image as pl
import numpy as np
import glob, os
import shutil 
import random as rd
import time as ti

t1 = ti.clock()

a,b,c = 0 , 95, 255 


try:
    if '' != sys.argv[1]:
       b = int(sys.argv[1])
except:
    pass


def moy(file):
    im = pl.open(file)

    mat = np.asarray(im)

    S=0
    for i in range(int(mat.shape[1])):
        for j in range(mat.shape[0]):
            S = S + mat[i,j]
    S = S /  mat.shape[0] / mat.shape[1]
    return S    


if not os.path.exists("Dataset"):
    os.makedirs("Dataset")    
     
if not os.path.exists("Dataset/danger"):
    os.makedirs("Dataset/danger")
    
if not os.path.exists("Dataset/safe"):
    os.makedirs("Dataset/safe")
    

n=0
for filename in glob.glob('Out/*.jpg'):
   n = n + 1

print("Images à traiter : " + str(n))      
    
it = 0
for filename in glob.glob('Out/*.jpg'):
    it = it + 1
    if it * 10 // n == it * 10 / n:
        print(str(it * 100 / n) + "%")		
    temp = moy(filename) 
    bg = a
    bd = b
    if ( temp >= bg and temp <= bd):
        shutil.copy2("Base"+filename[3:],"Dataset/safe"+"/"+filename[4:])
    bg = bd
    bd = c
    if ( temp >= bg and temp <= bd):
        shutil.copy2("Base"+filename[3:],"Dataset/danger"+"/"+filename[4:])
        
t2 = ti.clock()
print("Done in " + str(int(t2-t1)) + " secs")
