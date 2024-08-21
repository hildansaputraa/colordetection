import cv2
import numpy as np
import serial
import time

#kirim koordinat
PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
ser = serial.Serial(PORT, BAUD_RATE)

# Buka input stream dari webcam
webcam = cv2.VideoCapture(0)

# Dapatkan dimensi frame webcam
ret, img = webcam.read()
height, width, _ = img.shape


# Koordinat pusat frame
center_x = width // 2
center_y = height // 2

X, Y = 0, 0

while True:
    # Baca frame dari webcam
    ret, img  = webcam.read()
    
    
    if ret is False:
        print("Tidak dapat membaca frame dari webcam.")
        break
    
    # Konversi gambar dari BGR ke HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower = np.array([15, 98, 126])
    upper = np.array([105, 203, 225])
    mask = cv2.inRange(imgHSV, lower, upper)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Tambahkan garis koordinat tengah
    cv2.line(mask_bgr, (center_x, 0), (center_x, height), (255, 0, 0), 2)  # Garis vertikal hijau
    cv2.line(mask_bgr, (0, center_y), (width, center_y), (255, 0, 0), 2)   # Garis horizontal hijau
    
    # Hitung momen dari gambar biner
    M = cv2.moments(mask)
    
    if M["m00"] != 0:
        # Hitung koordinat x, y dari pusat objek yang terdeteksi
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        X = cX - center_x
        Y = cY - center_y
        cv2.circle(mask_bgr, (cX, cY), 5, (0, 0, 255), -1)
        cv2.putText(mask_bgr, f"({X}, {Y})", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        print("Tidak ada area yang terdeteksi.")
    
    # Gabungkan gambar asli dengan mask_bgr untuk menampilkan hasil akhir
    output = cv2.addWeighted(img, 0.7, mask_bgr, 0.3, 0)
    
    # Tampilkan gambar hasil
    cv2.imshow("KOORDINAT GAMBAR", mask_bgr)
    cv2.imshow("GAMBAR ASLI", output)
    #print(X, Y)
    ser.write(f"{X},{Y}\n".encode('utf-8'))
    print(f"Data {X}{Y} berhasil dikirim.")
          
    key = cv2.waitKey(1)
    if key == 27: 
        break

webcam.release()
cv2.destroyAllWindows()
