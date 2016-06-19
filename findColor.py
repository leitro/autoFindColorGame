import cv2
import numpy as np
import os
import pyscreenshot as ss
import time

def onMouse(event, x, y, flags, param):
    global flag, pLeftTop, pRightBottom
    if event == cv2.EVENT_LBUTTONDOWN:
        if flag:
            pLeftTop = (x,y)
        else:
            pRightBottom = (x,y)
        flag = False

flag = True
pLeftTop = None
pRightBottom = None

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', onMouse)

img = ss.grab(bbox=(0,0,1300,768))
img = np.array(img)
cv2.imshow('frame', img)
if cv2.waitKey(0) & 0xff == ord(' '):
    cv2.destroyWindow('frame')
#print(pLeftTop, pRightBottom)
while True:
    img = ss.grab(bbox=(0,0,1300,768))
    img = np.array(img)
    target = img[pLeftTop[1]:pRightBottom[1],pLeftTop[0]:pRightBottom[0]]
    gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
    im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    centersGray = []
    for c in contours:
        (x,y), radius = cv2.minEnclosingCircle(c)
        x, y = int(x), int(y)
        centers.append((x,y))
        centersGray.append(gray[y,x])
    sets = set(centersGray)
    index = None
    for s in sets:
        if centersGray.count(s) == 1:
            index = centersGray.index(s)
            break
    realX = centers[index][0] + pLeftTop[0]
    realY = centers[index][1] + pLeftTop[1]
    os.system('xdotool mousemove '+str(realX)+' '+str(realY))
    os.system('xdotool click 1')
    print(realX,realY)
