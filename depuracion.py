import cv2
import numpy as np
import pygame

# Definimos las dimensiones de la pantalla del juego
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 600

# Inicializamos Pygame
pygame.init()

# Creamos la ventana del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Creamos un objeto de color amarillo
YELLOW = (255, 255, 0)
yellow_rect = pygame.Rect(0, 0, 50, 50)
yellow_surface = pygame.Surface((50, 50))
yellow_surface.fill(YELLOW)

# Inicializamos la cámara
cap = cv2.VideoCapture(0)

# Definimos los kernels para los procesos de erosión y dilatación
kernel_erode = np.ones((5, 5), np.uint8)
kernel_dilate = np.ones((10, 10), np.uint8)

# Bucle principal del juego
while True:
    # Capturamos un frame de la cámara
    ret, frame = cap.read()

    # Si la captura ha sido exitosa
    if ret:
        # Convertimos la imagen a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definimos el rango de colores que queremos detectar (en este caso, amarillo)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])

        # Aplicamos una máscara para obtener solo los píxeles de color amarillo
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Aplicamos erosión y dilatación para eliminar el ruido y mejorar la detección
        mask = cv2.erode(mask, kernel_erode, iterations=1)
        mask = cv2.dilate(mask, kernel_dilate, iterations=1)

        # Buscamos el contorno del objeto de color amarillo
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Si hemos encontrado algún contorno
        if contours:
            # Obtenemos el contorno más grande (el objeto de color amarillo)
            largest_contour = max(contours, key=cv2.contourArea)

            # Obtenemos el rectángulo que engloba al contorno
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Ajustamos la posición y tamaño del objeto de color amarillo para que se ajuste a la pantalla del juego
            yellow_rect.x = int(x * 3500 / 640)
            yellow_rect.y = int(y * SCREEN_HEIGHT / cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            yellow_rect.w = int(w * SCREEN_WIDTH / cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            yellow_rect.h = int(h * SCREEN_HEIGHT / cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
           

        # Dibujamos el objeto de color amarillo en la pantalla del juego
        screen.fill((255, 255, 255))
        screen.blit(yellow_surface, yellow_rect)
        

    # Actualizamos la pantalla del juego
    pygame.display.flip()

    # Comprobamos si se ha cerrado la ventana del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Si se ha cerrado la ventana, liberamos los recursos y salimos del programa
            cap.release()
            pygame.quit()
            exit()

