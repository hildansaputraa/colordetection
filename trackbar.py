import cv2
import numpy as np

def nothing(x):
    pass  # nothing happens when the pass is executed

imgBGR = np.zeros((300,512,3), np.uint8)
imgHSV = imgBGR
cv2.namedWindow('image')

# In OpenCV, Hue has values from 0 to 180, Saturation and Value from 0 to 255.

# inputs of cv2.createTrackbar()
# first argument is the trackbar name,
# second one is the window name to which it is attached,
# third argument is the default value,
# fourth one is the maximum value,
# fifth one is the callback function which is executed every time trackbar value changes.
cv2.createTrackbar('H','image',0,180,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

while(1):
    cv2.imshow('image',imgBGR)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # wait for ESC key to exit
        break

    H = cv2.getTrackbarPos('H','image')
    S = cv2.getTrackbarPos('S','image')
    V = cv2.getTrackbarPos('V','image')
    SW = cv2.getTrackbarPos(switch,'image')
    
    if SW == 0:
        imgBGR[:] = 0
    else:
        imgHSV[:] = [H,S,V]
        imgBGR=cv2.cvtColor(imgHSV,cv2.COLOR_HSV2BGR)

cv2.destroyAllWindows()
