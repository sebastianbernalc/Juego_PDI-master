import cv2
import numpy as np
import pygame

# Inicializa la biblioteca Pygame
pygame.init()

# Define el tamaño de la ventana del juego
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Define el rango de color azul que deseas detectar
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# Define el rango de color amarillo que deseas detectar
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Define la velocidad de movimiento de los objetos
MOVEMENT_SPEED = 5

# Crea la ventana del juego
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Juego de detección de colores")

# Crea los objetos del juego
blue_object = pygame.Rect(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2, 50, 50)
yellow_object = pygame.Rect(WINDOW_WIDTH // 4 * 3, WINDOW_HEIGHT // 2, 50, 50)

# Inicia la captura de video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    # Lee un fotograma de la cámara
    ret, frame = cap.read()

    # Aplica un filtro gaussiano para suavizar la imagen y reducir el ruido
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # Convierte la imagen a espacio de color HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Crea máscaras para los píxeles dentro del rango de color azul y amarillo
    blue_mask = cv2.inRange(hsv[:, WINDOW_WIDTH // 2:], lower_blue, upper_blue)
    yellow_mask = cv2.inRange(hsv[:, :WINDOW_WIDTH // 2], lower_yellow, upper_yellow)

    # Aplica una serie de operaciones morfológicas para eliminar pequeñas imperfecciones en las máscaras
    blue_mask = cv2.erode(blue_mask, None, iterations=2)
    blue_mask = cv2.dilate(blue_mask, None, iterations=2)
    yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
    yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)

    # Encuentra los contornos de las máscaras y dibuja los contornos en la imagen original
    blue_contours, hierarchy = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_contours, hierarchy = cv2.findContours(yellow_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(blue_contours) > 0:
        c = max(blue_contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        blue_object.centerx = x + w // 2 + WINDOW_WIDTH // 2
    if len(yellow_contours) > 0:
        c = max(yellow_contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        yellow_object.centerx = x + w // 2

    # Mueve los objetos del juego según la detección de los colores
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and yellow_object.left > 0:
        yellow_object.left -= MOVEMENT_SPEED
    if keys[pygame.K_RIGHT] and yellow_object.right < WINDOW_WIDTH // 2:
        yellow_object.right += MOVEMENT_SPEED
    if blue_object.right < WINDOW_WIDTH and blue_object.right < blue_object.centerx:
        blue_object.right += MOVEMENT_SPEED

    # Dibuja los objetos del juego en la ventana
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 255), blue_object)
    pygame.draw.rect(window, (255, 255, 0), yellow_object)

    # Actualiza la pantalla
    pygame.display.update()

    # Verifica si el usuario ha cerrado la ventana del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            exit()
