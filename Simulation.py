import time as ti
import numpy as np
import math as m
import matplotlib.pyplot as plt
import glob, os, sys
import random as rd
import _thread as th
from scipy.misc import imread
from PIL import Image as pl
import tensorflow as tf

a = 10
delay = 0.5
traj = []
scale = 0.7       # m/pix
posP = [3000, 3000]
dir = 0
t = 0  # t for teta, 0 pointed to the north, anti-clockwise, degrease



# FONCTIONS INTERMEDIARES

def cor(t, cor):
    if t + cor >= 360:
        t = t + cor -360
    elif t + cor < 0:
        t = 360 + cor + t
    else :
        t = t + cor
    return t

def signe(nb):
    if nb == 0:
        return 0
    nb = nb / abs(nb)
    return nb

def cP2M(posP):
    posM = [scale*posP[0], scale*posP[1]]
    return posM

def cM2P(posM):
    posP = [posM[0] / scale, posM[1] / scale]
    return posP

def rmax(list):
    max = list[0]
    rmax = 0
    for k in range(len(list)) :
        if list[k] > max :
            max = list[k]
            rmax = k
    return rmax, max




# FONCTION CAMERA

W = 200
L = 200
preW = int(m.sqrt(2)*W/2)+1
preL = int(m.sqrt(2)*L/2)+1

def camera(posP, teta):
    W = 200
    L = 200
    x, y = posP[0], posP[1]
    imb = pl.open("Base.bmp")
    box = x - preW, y - preL, x + preW, y + preL

    temp = imb.crop(box)
    temp = temp.rotate(teta, expand=True)

    sizeInf = temp.getbbox()
    tempW = abs(sizeInf[0] - sizeInf[2])
    tempL = abs(sizeInf[1] - sizeInf[3])

    mid = int(tempW/2), int(tempL/2)
    box = int(mid[0] - W/2), int(mid[1] - L/2), int(mid[0] + W/2), int(mid[1] + L/2)
    crop = temp.crop(box)
    pl.close()
    return crop


# TREADS

def funA():
    global t
    global posP
    global dir
    global traj

    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        while True :
            im = camera(posP, t)

            sizeInf = temp.getbbox()
            W = abs(sizeInf[0] - sizeInf[2])
            L = abs(sizeInf[1] - sizeInf[3])

            box1 = 0,0,int(W/3),int(L/3)
            box2 = int(W/3), 0, int(W * 2/ 3), int(L / 3)
            box3 = int(W * 2/ 3), 0, W, int(L / 3)

            im1 = im.crop(box1)
            im2 = im.crop(box2)
            im3 = im.crop(box3)

            im.save("im.jpg")
            im1.save("im1.jpg")
            im2.save("im2.jpg")
            im3.save("im3.jpg")


            # IMAGE PRINCIPALE im

            image_data = tf.gfile.FastGFile(im, 'rb').read()
            time1 = ti.time()
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
            if predictions[0][0] > predictions[0][0] and predictions[0][0] > 0.9 :
                print("PARACHUTE !")
                print(traj)
                quit()


            # IMAGES SECONDAIRES im1 im2 im3

            #im1
            image_data = tf.gfile.FastGFile(im1, 'rb').read()
            time1 = ti.time()
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            p1 = predictions[0][0]

            # im2
            image_data = tf.gfile.FastGFile(im2, 'rb').read()
            time1 = ti.time()
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            p2 = predictions[0][0]

            # im3
            image_data = tf.gfile.FastGFile(im3, 'rb').read()
            time1 = ti.time()
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, \
                                   {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            p3 = predictions[0][0]

            rmax = rmax([p1,p2,p3])[0]
            if rmax[1] > 0.7 :
                if rmax[0] == 0:
                    dir = -15
                if rmax[0] == 1:
                    dir = 0
                if rmax[0] == 2:
                    dir = 15
            else :
                dir = 0



def funB():
    global t
    global posP
    global dir
    global traj
    posM = cP2M(posP)
    scale = 0.7  # m/pix
    v = 15  # m/s
    ts = 30  # ts for teta per sec, rotation speed
    timeFlow = 10  # speed of the simulation
    frameRate = 0.5  # ips
    every = 0.1  # time of one simulation loop
    tempT = ti.time()
    tempt = 0
    tempts = 0
    traj = [posP]
    while True :
        direction = dir
        dir = 0
        countcor = 0
        while countcor < abs(direction):
            deltaT = (ti.time() - tempT) * timeFlow
            tempT = ti.time()
            distance = v * deltaT
            t = cor(tempt, ts * deltaT * signe(direction))
            posM = [posM[0] + distance * m.cos(t - 90), posM[1] + distance * m.sin(t - 90)]
            countcor = ts * deltaT + countcor
            tempt = t
            traj.append(cM2P(posM))
            print(t)
            ti.sleep(every / timeFlow - tempT + ti.time())
            posP = cM2P(posM)

        deltaT = (ti.time() - tempT) * timeFlow
        tempT = ti.time()
        distance = v * deltaT

        posM = [posM[0] + distance * m.sin(t), posM[1] - distance * m.cos(t)]
        countcor = abs(tempt - t) + countcor
        tempt = t
        traj.append(cM2P(posM))
        # print(t)
        ti.sleep(every / timeFlow - tempT + ti.time())
        posP = cM2P(posM)

th.start_new_thread(funA, ())
th.start_new_thread(funB, ())

try:
   th.start_new_thread( print_time, ("Thread-1", 2))
   th.start_new_thread( print_time, ("Thread-2", 4))
except:
   print ("Error: unable to start thread")

while 1:
   pass