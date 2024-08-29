import cv2
import numpy as np

# Membuka kamera
cap = cv2.VideoCapture(0,cv2.CAP_D)

#
# Membuat detektor blob dengan parameter yang telah ditentukan
detector = cv2.SimpleBlobDetector_create(params)


while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definisi warna hijau
    low_green = np.array([9, 114, 170])
    high_green = np.array([61, 206, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

    
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Tampilkan gambar dengan deteksi hijau dan blob
    cv2.imshow("Green with Blobs", frame_with_keypoints)

    key = cv2.waitKey(1)
    if key == 27: # Tekan ESC untuk keluar
        break

# Melepaskan resources
cap.release()
cv2.destroyAllWindows()
