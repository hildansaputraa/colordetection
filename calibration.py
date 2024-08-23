import cv2
import numpy as np
import json

try:
    with open('yellow.json', 'r') as openfile:
        data_kalibrasi = json.load(openfile)
except Exception as e:
    data_kalibrasi = {
        "min" : [0,0,0],
        "max" : [0,0,0] 
    }
    
def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)

cv2.createTrackbar("Hue Min","TrackBars",data_kalibrasi['min'][0],179,empty)
cv2.createTrackbar("Hue Max","TrackBars",data_kalibrasi['max'][0],179,empty)
cv2.createTrackbar("Sat Min","TrackBars",data_kalibrasi['min'][1],255,empty)
cv2.createTrackbar("Sat Max","TrackBars",data_kalibrasi['max'][1],255,empty)
cv2.createTrackbar("Val Min","TrackBars",data_kalibrasi['min'][2],255,empty)
cv2.createTrackbar("Val Max","TrackBars",data_kalibrasi['max'][2],255,empty)

webcam = cv2.VideoCapture(0)

while True:    
    _, img = webcam.read()  
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    data_kalibrasi['min'][0] = cv2.getTrackbarPos("Hue Min","TrackBars")
    data_kalibrasi['max'][0] = cv2.getTrackbarPos("Hue Max", "TrackBars")
    data_kalibrasi['min'][1] = cv2.getTrackbarPos("Sat Min", "TrackBars")
    data_kalibrasi['max'][1] = cv2.getTrackbarPos("Sat Max", "TrackBars")
    data_kalibrasi['min'][2] = cv2.getTrackbarPos("Val Min", "TrackBars")
    data_kalibrasi['max'][2] = cv2.getTrackbarPos("Val Max", "TrackBars")

    lower = np.array(data_kalibrasi['min'])
    upper = np.array(data_kalibrasi['max'])

    print(data_kalibrasi['min'],data_kalibrasi['max'])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)


    imgStack = stackImages(0.6,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("Image Stack", imgStack)

    key = cv2.waitKey(1)
    if key == ord('y'): # y for yellow
        print(lower)
        print(upper)
        with open("yellow.json", "w") as outfile:
            json.dump(data_kalibrasi, outfile) 
    elif key == ord('g'): # g for green
        print(lower)
        print(upper)
        with open("green.json", "w") as outfile:
            json.dump(data_kalibrasi, outfile)
    elif key == 27: #esc
        break