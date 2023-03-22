import cv2
import numpy as np
import pygame
import sys

# Inicializar pygame
pygame.init()

# Configurar la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de movimiento")

# Cargar la imagen del objeto
object_image = pygame.image.load('jugador2.png')
object_rect = object_image.get_rect()
object_speed = 5

# Configurar la cámara
camera = cv2.VideoCapture(0)

while True:
    # Capturar la imagen de la cámara
    _, frame = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de colores que se quiere detectar (en este ejemplo, se detectará el color azul)
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Crear una máscara binaria que muestre los píxeles dentro del rango de colores
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Encontrar los contornos de los objetos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se encuentra un objeto azul en la imagen, mover el objeto en el juego hacia ese objeto
    if len(contours) > 0:
        # Encontrar el contorno más grande (que debería ser el objeto azul más grande en la imagen)
        largest_contour = max(contours, key=cv2.contourArea)

        # Encontrar el centro del contorno más grande
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Mover el objeto en el juego hacia el centro del objeto azul
            if object_rect.centerx < cx:
                object_rect.centerx += object_speed
            elif object_rect.centerx > cx:
                object_rect.centerx -= object_speed

    # Manejar eventos del teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                object_rect.centerx -= object_speed
            elif event.key == pygame.K_d:
                object_rect.centerx += object_speed

    # Dibujar el objeto en la pantalla
    screen.fill((255, 255, 255))
    screen.blit(object_image, object_rect)
    pygame.display.flip()

