import cv2
import numpy as np
import json
#import serial
import time

#kirim koordinat
#PORT = '/dev/ttyUSB0'
#BAUD_RATE = 9600
#ser = serial.Serial(PORT, BAUD_RATE)

# Buka input stream dari webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Dapatkan dimensi frame cap
ret, img = cap.read()
height, width, _ = img.shape

# Koordinat pusat frame
center_x = width // 2
center_y = height // 2

Xgreen, Xyellow, Ygreen, Yyellow = 0, 0, 0, 0

nilaiPrev = ""

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
    
    
    #green
    blurGreen = cv2.medianBlur(maskGreen, 17)
    contoursGreen = cv2.findContours(blurGreen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoursGreen = contoursGreen[0] if len(contoursGreen) == 2 else contoursGreen[1]


    for cntr in contoursGreen:
        area = cv2.contourArea(cntr)
        Mgreen = cv2.moments(cntr)
        if area > 10000:
            if Mgreen["m00"] != 0:
                cXy = int(Mgreen["m10"] / Mgreen["m00"])
                cYy = int(Mgreen["m01"] / Mgreen["m00"])
                    
                Xgreen = cXy - center_x
                Ygreen = cYy - center_y
        
                cv2.circle(img, (cXy, cYy), 5, (0, 0, 255), -1)
                cv2.putText(img, f"({Xgreen}, {Ygreen})", (cXy, cYy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.drawContours(img, [cntr], 0, (0, 0, 255), 2)
               
  
    
    #yellow
    blurYellow = cv2.medianBlur(maskYellow, 17)
    contoursYellow = cv2.findContours(blurYellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoursYellow = contoursYellow[0] if len(contoursYellow) == 2 else contoursYellow[1]


    for cntr in contoursYellow:
        area = cv2.contourArea(cntr)
        Myellow = cv2.moments(cntr)
        if area > 5000:
            if Myellow["m00"] != 0:
                cXy = int(Myellow["m10"] / Myellow["m00"])
                cYy = int(Myellow["m01"] / Myellow["m00"])
                    
                Xyellow = cXy - center_x
                Yyellow = cYy - center_y
        
                cv2.circle(img, (cXy, cYy), 5, (0, 0, 255), -1)
                cv2.putText(img, f"({Xyellow}, {Yyellow})", (cXy, cYy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.drawContours(img, [cntr], 0, (0, 0, 255), 2)

    
    cv2.imshow("Image", img)
    cv2.imshow("Result Green", blurGreen)
    cv2.imshow("Result Yellow", blurYellow)
    
    
    
    nilaiNew = f"{Xgreen}+{Ygreen}+{Xyellow}+{Yyellow}"
    
    # Bandingkan nilaiNew dengan nilaiPrev
    if nilaiNew != nilaiPrev:
        print(f"{Xgreen}+{Ygreen}+{Xyellow}+{Yyellow}")
        nilaiPrev = nilaiNew  # Update nilaiPrev setelah perbandingan
        #ser.write(f"{Xgreen},{Xyellow},{Ygreen},{Yyellow}\n".encode('utf-8'))

    
    
    key = cv2.waitKey(1)
    if key == 27:  # Tekan ESC untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
