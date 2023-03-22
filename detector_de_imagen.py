import cv2
import pygame

# Inicializar la cámara y obtener la resolución de la imagen
camera = cv2.VideoCapture(0)
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))

# Definir el rango de color azul a detectar en formato HSV
blue_lower = (90, 50, 50)
blue_upper = (130, 255, 255)

# Inicializar la posición del objeto en el centro de la pantalla
object_position = width // 2, height // 2

# Bucle principal del juego
while True:
    # Capturar el fotograma actual de la cámara
    _, frame = camera.read()

    # Convertir el fotograma a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Aplicar una máscara de color azul al fotograma
    mask = cv2.inRange(hsv, blue_lower, blue_upper)

    # Aplicar una operación de erosión y dilatación para eliminar el ruido
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encontrar el contorno más grande en la máscara
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        object_position = int(x), int(y)

    # Dibujar un círculo en la posición del objeto
    pygame.draw.circle(screen, (0, 255, 0), object_position, 20)

    # Actualizar la pantalla de Pygame
    pygame.display.update()

    # Escuchar eventos de teclado y mover el objeto en consecuencia
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                object_position = object_position[0] - 10, object_position[1]
            elif event.key == pygame.K_d:
                object_position = object_position[0] + 10, object_position[1]

    # Salir del juego si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos de OpenCV y Pygame
camera.release()
cv2.destroyAllWindows()
pygame.quit()

