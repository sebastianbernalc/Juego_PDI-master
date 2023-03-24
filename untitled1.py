import cv2
import numpy as np

# Define el rango de color amarillo que deseas detectar
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

  

    # Convierte la imagen a espacio de coqlor HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask2=cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('yellow detector', hsv)
    

    # Salir del ciclo si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

