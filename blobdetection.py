import cv2
import numpy as np

# Buka input stream dari webcam
webcam = cv2.VideoCapture(0)

while True:
    # Baca frame dari webcam
    _, img = webcam.read()
    
    # Konversi gambar dari BGR ke HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Buat binary image dengan threshold untuk warna tertentu
    lower = np.array([9, 114, 170])
    upper = np.array([61, 206, 255])
    mask = cv2.inRange(imgHSV, lower, upper)
    
    # Gunakan mask langsung sebagai gambar threshold
    thresh = mask

    # Mencari kontur
    contour_img = img.copy()
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    isolated_count = 0
    cluster_count = 0

    for cntr in contours:
        area = cv2.contourArea(cntr)
        convex_hull = cv2.convexHull(cntr)
        convex_hull_area = cv2.contourArea(convex_hull)
        
        if convex_hull_area > 0:  # Periksa apakah convex_hull_area tidak nol
            ratio = area / convex_hull_area
            if ratio < 0.91:
                # Jika rasio kurang dari 0.91, kontur dianggap sebagai cluster
                cv2.drawContours(contour_img, [cntr], 0, (0, 0, 255), 2)
                cluster_count += 1
            else:
                # Jika rasio lebih dari atau sama dengan 0.91, kontur dianggap terisolasi
                cv2.drawContours(contour_img, [cntr], 0, (0, 255, 0), 2)
                isolated_count += 1

    print('number_clusters:', cluster_count)
    print('number_isolated:', isolated_count)

    cv2.imshow("thresh", thresh)
    cv2.imshow("contour_img", contour_img)
    
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

webcam.release()
cv2.destroyAllWindows()
