import cv2

# Membuka kamera dengan DirectShow
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    imgHSV= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.imshow('Camera', imgHSV)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
