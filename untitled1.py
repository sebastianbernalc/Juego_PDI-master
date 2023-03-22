import cv2

# Accede a la cámara
cap = cv2.VideoCapture(0)

while True:
    # Captura un cuadro de la cámara
    ret, frame = cap.read()

    # Invierte la imagen
    frame = cv2.flip(frame, 1)

    # Muestra la imagen invertida
    cv2.imshow('Inverted Camera', frame)

    # Si se presiona la tecla 'q', sal del bucle
    if cv2.waitKey(1) == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()

