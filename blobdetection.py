import cv2
import numpy as np

# Buka input stream dari webcam
webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Baca frame dari webcam
    ret, img = webcam.read()
    
    if not ret:
        print("Tidak dapat membaca frame dari webcam.")
        break
    
    # Konversi gambar dari BGR ke HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Buat binary image dengan threshold untuk warna tertentu
    lower = np.array([15, 98, 126])
    upper = np.array([105, 203, 225])
    mask = cv2.inRange(imgHSV, lower, upper)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Hitung momen dari gambar biner
    M = cv2.moments(mask)
    
    if M["m00"] != 0:
        # Hitung koordinat x, y dari pusat
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        X = cX - 320
        Y = cY - 240
        # Tandai titik pusat dan beri teks
        cv2.circle(mask_bgr, (cX, cY), 5, (0, 0, 255), -1)
        cv2.putText(mask_bgr, f"({X}, {Y})", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    else:
        # Jika tidak ada area terdeteksi, tampilkan pesan
        print("Tidak ada area yang terdeteksi.")
    
    # Tampilkan gambar hasil
    cv2.imshow("thresh", mask_bgr)
    print(X,Y)
    # Tunggu input untuk keluar (ESC)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

# Lepaskan resources dan tutup jendela
webcam.release()
cv2.destroyAllWindows()
