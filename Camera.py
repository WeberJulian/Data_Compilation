import time as ti
import numpy
import math as m
import matplotlib.pyplot as plt
from scipy.misc import imread

scale = 0.7       # m/pix
v = 15            # m/s
t = 45             # t for teta, 0 pointed to the north, anti-clockwise, degrease
ts = 30            # ts for teta per sec, rotation speed
#maxts = 20        # max rotation speed
#tss = 10        # angular acceleration caused command system
timeFlow = 10     # speed of the simulation
frameRate = 0.5   # ips
every = 0.1       # time of one simulation loop

def cP2M(posP):
    posM = [scale*posP[0], scale*posP[1]]
    return posM


def cM2P(posM):
    posP = [posM[0] / scale, posM[1] / scale]
    return posP

posP = [3000, 3000]
posM = cP2M(posP)

directions = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,1,0,0]

tempT = ti.time()
tempt = 0
tempts = 0

traj = [posP]

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

while directions != [] :
    direction = directions.pop()
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

    deltaT = (ti.time() - tempT) * timeFlow
    tempT = ti.time()
    distance = v * deltaT

    posM = [posM[0] + distance * m.sin(t), posM[1] - distance * m.cos(t)]
    countcor = abs(tempt - t) + countcor
    tempt = t
    traj.append(cM2P(posM))
    # print(t)
    ti.sleep(every / timeFlow - tempT + ti.time())

    print(t)


# [posM[0] + distance * m.sin(t), posM[1] - distance * m.cos(t)]
'''
while directions != [] :
    deltaT = (ti.time() - tempT) * timeFlow
    tempT = ti.time()

    direction = directions.pop()
    distance = v * deltaT

    t = cor(tempt, ts * deltaT)
    ts = (tempt - (tempt + ts * deltaT)) / deltaT

    if direction == 0 :
        if ts != 0 :
            ts = ts + tss * deltaT * (ts/abs(ts)) * (-1)
    else :
        ts = ts + tss * deltaT * direction

    if abs(ts) > maxts:  # we have reach the max ts
        ts = 45


    posM = [posM[0] + v * deltaT * m.sin((tempt+t)/2), posM[1] - v * deltaT * m.cos((tempt+t)/2)]
    tempt = t
    traj.append(cM2P(posM))
    print(t)
    print(ts)
    print(deltaT)
    print("\n")
    ti.sleep(every / timeFlow - tempT + ti.time())
'''


print(traj)

X = []
Y = []
for XY in traj :
    X.append(XY[0])
    Y.append(XY[1])

plt.scatter(X,Y,zorder=1)
img = imread("Base.bmp")
plt.imshow(img,zorder=0)
plt.show()