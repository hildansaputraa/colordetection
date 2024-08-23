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

Xgreen, Xyellow, Ygreen, Yyellow = 0, 0, 0, 0

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
    bgrGreen = cv2.cvtColor(maskGreen, cv2.COLOR_GRAY2BGR)
    bgrYellow = cv2.cvtColor(maskYellow, cv2.COLOR_GRAY2BGR)
    
    mask = cv2.bitwise_or(maskYellow, maskGreen)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # Tambahkan garis koordinat tengah
    cv2.line(mask_bgr, (center_x, 0), (center_x, height), (255, 0, 0), 2)  # Garis vertikal biru
    cv2.line(mask_bgr, (0, center_y), (width, center_y), (255, 0, 0), 2)   # Garis horizontal biru
    
    # Hitung momen dari gambar biner
    Mgreen = cv2.moments(maskGreen)
    
    if Mgreen["m00"] != 0:
        # Hitung koordinat x, y dari pusat objek yang terdeteksi
        cXg = int(Mgreen["m10"] / Mgreen["m00"])
        cYg = int(Mgreen["m01"] / Mgreen["m00"])
        
        Xgreen = cXg - center_x
        Ygreen = cYg - center_y
        
        cv2.circle(bgrGreen, (cXg, cYg), 5, (0, 0, 255), -1)
        cv2.putText(bgrGreen, f"({Xgreen}, {Ygreen})", (cXg, cYg), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    else:
        print("Tidak ada hijau yang terdeteksi.")
    
    Myellow = cv2.moments(maskYellow)
    
    if Myellow["m00"] != 0:
        # Hitung koordinat x, y dari pusat objek yang terdeteksi
        cXy = int(Myellow["m10"] / Myellow["m00"])
        cYy = int(Myellow["m01"] / Myellow["m00"])

        Xyellow = cXy - center_x
        Yyellow = cYy - center_y
    
        cv2.circle(bgrYellow, (cXy, cYy), 5, (0, 0, 255), -1)
        cv2.putText(bgrYellow, f"({Xyellow}, {Yyellow})", (cXy, cYy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        print("Tidak ada kuning yang terdeteksi.")
    
    # Gabungkan gambar asli dengan mask_bgr untuk menampilkan hasil akhir
    output = cv2.addWeighted(img, 0.7, mask_bgr, 0.3, 0)
    
    # Tampilkan gambar hasil
    cv2.imshow("KOORDINAT GAMBAR1", bgrYellow)
    cv2.imshow("KOORDINAT GAMBAR", bgrGreen)
   # cv2.imshow("GAMBAR ASLI", output)

    print(Xgreen,"+",Xyellow,"+",Ygreen,"+",Yyellow)
    ser.write(f"{Xgreen},{Xyellow},{Ygreen},{Yyellow}\n".encode('utf-8'))
    
    key = cv2.waitKey(1)
    if key == 27:  # Tekan ESC untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
