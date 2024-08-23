import cv2
import numpy as np
import json
import serial
import time

#kirim koordinat
PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
ser = serial.Serial(PORT, BAUD_RATE)

# Buka input stream dari webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Dapatkan dimensi frame cap
ret, img = cap.read()
height, width, _ = img.shape

# Koordinat pusat frame
center_x = width // 2
center_y = height // 2

X, Y = 0, 0

# Load kalibrasi warna
try:
    with open('yellow.json', 'r') as openfile:
        yellow = json.load(openfile)
except Exception as e:
    print('data kalibrasi yellow tidak ada')
    exit()

try:
    with open('green.json', 'r') as openfile:
        green = json.load(openfile)
except Exception as e:
    print('data kalibrasi green tidak ada')
    exit()

while True:
    # Baca frame dari cap
    ret, img  = cap.read()
    
    if ret is False:
        print("Tidak dapat membaca frame dari cap.")
        break
    
    # Konversi gambar dari BGR ke HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Membuat mask untuk warna kuning
    lowerYellow = np.array(yellow['min'])
    upperYellow = np.array(yellow['max'])
    maskYellow = cv2.inRange(imgHSV, lowerYellow, upperYellow)
    
    # Membuat mask untuk warna hijau
    lowerGreen = np.array(green['min'])
    upperGreen = np.array(green['max'])
    maskGreen = cv2.inRange(imgHSV, lowerGreen, upperGreen)
    
    # Gabungkan kedua mask
    mask = cv2.bitwise_or(maskYellow, maskGreen)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Tambahkan garis koordinat tengah
    cv2.line(mask_bgr, (center_x, 0), (center_x, height), (255, 0, 0), 2)  # Garis vertikal biru
    cv2.line(mask_bgr, (0, center_y), (width, center_y), (255, 0, 0), 2)   # Garis horizontal biru
    
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

    ser.write(f"{X},{Y}\n".encode('utf-8'))
    print(f"Data {X}{Y} berhasil dikirim.")
    
    key = cv2.waitKey(1)
    if key == 27:  # Tekan ESC untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
