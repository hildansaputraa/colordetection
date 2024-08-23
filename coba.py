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
    green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # Deteksi blob di area hijau
    keypoints = detector.detect(green_mask)
    
    # Gambar keypoints (blob) di gambar asli
    frame_with_keypoints = cv2.drawKeypoints(green, keypoints, np.array([]), (0, 0, 255), 
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Tampilkan gambar dengan deteksi hijau dan blob
    cv2.imshow("Green with Blobs", frame_with_keypoints)

    key = cv2.waitKey(1)
    if key == 27: # Tekan ESC untuk keluar
        break

# Melepaskan resources
cap.release()
cv2.destroyAllWindows()
