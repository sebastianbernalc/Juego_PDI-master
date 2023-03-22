import pygame
import numpy as np
import cv2
import queue
import threading


# Inicializar el Pygame(GAME)
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

# Configurar la pantalla a 1280x600.
tam_screen = (1280, 600)
screen = pygame.display.set_mode(tam_screen)
pygame.display.set_caption('Football Head')

# Función que lee continuamente la cámara y escribe los fotogramas en la cola
def capture_frames(queue):
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if ret:
            queue.put(frame)
        else:
            
            break
    camera.release()

# Cargar imagenes
fondo_img = pygame.image.load('images/fondo.png')
jugador1_img = pygame.image.load('images/jugador1.png')
jugador2_img = pygame.image.load('images/jugador2.png')
balon_img = pygame.image.load('images/balon.png')
porteria1_img = pygame.image.load('images/porteria1.png')
porteria2_img = pygame.image.load('images/porteria2.png')
gol_image = pygame.image.load("images/gol.png")
audio=True


# Redimensionar imagenes
fondo_img = pygame.transform.scale(fondo_img, tam_screen)
jugador1_img = pygame.transform.scale(jugador1_img, (100, 100))
jugador2_img = pygame.transform.scale(jugador2_img, (100, 100))
balon_img = pygame.transform.scale(balon_img, (50, 50))
porteria1_img = pygame.transform.scale(porteria1_img, (200, 250))
porteria2_img = pygame.transform.scale(porteria2_img, (200, 250))

# Establecer posiciones iniciales de los objetos
porteria1_rect = porteria1_img.get_rect()
porteria1_rect.x = 0
porteria1_rect.y = 270

porteria2_rect = porteria2_img.get_rect()
porteria2_rect.x = 1080
porteria2_rect.y = 270

jugador1_rect = jugador1_img.get_rect()
jugador1_rect.x = 200
jugador1_rect.y = 400

jugador2_rect = jugador2_img.get_rect()
jugador2_rect.x = 970
jugador2_rect.y = 400

balon_rect = balon_img.get_rect()
balon_rect.x = 600
balon_rect.y = 450

gol_rect = gol_image.get_rect()
gol_rect.x = 360
gol_rect.y = 70

# Banderas del juego
jugador1_salto = False
jugador2_salto = False
palo1_colision = False
palo2_colision = False
jugador1_colision = False
jugador2_colision = False

# Establecer las variables del juego
cont_jugador1 = 0
cont_jugador2 = 0
text1 = font.render("Frionel: " + str(cont_jugador1), True, (255, 255, 255))
text2 = font.render("Penaldo: " + str(cont_jugador2), True, (255, 255, 255))
limite_der = 1100
limite_izq = 90
jugador1_y0 = 400
jugador2_y0 = 400
balon_x0 = 600
balon_y0 = 450

max_salto = 35.0
g = 9.8
theta = 90.0
v0 = 80.0
t1_salto = 0.0
t2_salto = 0.0
t_balon = 0.0

jugador1_vel = 2.0
jugador2_vel = 2.0

v0x = v0 * np.cos(np.deg2rad(theta))
v0y = v0 * np.sin(np.deg2rad(theta))

# Travesaños de las porterias
palo1 = pygame.Rect(porteria1_rect.x, porteria1_rect.y, porteria1_rect.width, 20)
pygame.draw.rect(screen, (255, 0, 0), palo1, 2)
palo2 = pygame.Rect(porteria2_rect.x, porteria2_rect.y, porteria2_rect.width, 20)
pygame.draw.rect(screen, (255, 0, 0), palo2, 2)
red1 = pygame.Rect(porteria1_rect.x+80, porteria1_rect.y+50, 20, porteria1_rect.height-50)
pygame.draw.rect(screen, (255, 0, 0), red1, 2)
red2 = pygame.Rect(porteria2_rect.x+100, porteria2_rect.y+50, 20, porteria2_rect.height-50)
pygame.draw.rect(screen, (255, 0, 0), red2, 2)
pygame.display.update()

frame_queue = queue.Queue()
capture_thread = threading.Thread(target=capture_frames, args=(frame_queue,))
capture_thread.start()
pygame.mixer.music.load("fut.wav")

# Reproduce la canción en bucle
pygame.mixer.music.play(-1)
# Establecer el ciclo de juego
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            cv2.destroyAllWindows()
            pygame.quit()
            quit()
    
        # Inicializar la cola y el hilo de la cámara
        
    if not frame_queue.empty():
            kernel_erode = np.ones((5, 5), np.uint8)
            kernel_dilate = np.ones((10, 10), np.uint8)
            frame = frame_queue.get()
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            
            # Convertimos la imagen a HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


            # Definimos el rango de colores que queremos detectar (en este caso, amarillo)
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([40, 255, 255])
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            # Aplicamos una máscara para obtener solo los píxeles de color amarillo
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            mask2=cv2.inRange(hsv, lower_blue, upper_blue)
            # Aplicamos erosión y dilatación para eliminar el ruido y mejorar la detección
            mask = cv2.erode(mask, kernel_erode, iterations=2)
            mask = cv2.dilate(mask, kernel_dilate, iterations=2)
            mask2 = cv2.erode(mask2, kernel_erode, iterations=2)
            mask2 = cv2.dilate(mask2, kernel_dilate, iterations=2)

            # Buscamos el contorno del objeto de color amarillo
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Si hemos encontrado algún contorno
            if contours:
                # Obtenemos el contorno más grande (el objeto de color amarillo)
                largest_contour = max(contours, key=cv2.contourArea)

                # Obtenemos el rectángulo que engloba al contorno
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Ajustamos la posición y tamaño del objeto de color amarillo para que se ajuste a la pantalla del juego
                jugador1_rect.x = int(x * 3500 / 640)
             
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if(x>218):
                        jugador1_rect.x=1192
                    print(jugador1_rect.x)# Comprobar si el objeto azul está por encima o por debajo de la mitad del eje y
                    
                    
                    if y>170:
                        if ~jugador1_salto:
                            jugador1_vel = 1.0
                            jugador1_salto = ~jugador1_salto
                   
            
            if contours2:
                # Obtenemos el contorno más grande (el objeto de color amarillo)
                largest_contour = max(contours2, key=cv2.contourArea)

                # Obtenemos el rectángulo que engloba al contorno
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Ajustamos la posición y tamaño del objeto de color amarillo para que se ajuste a la pantalla del juego
                
                jugador2_rect.x = int(x*(3500/640)-1500)
                
                for contour in contours2:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if(jugador2_rect.x<9):
                        jugador2_rect.x=9

                    
                    print(y)# Comprobar si el objeto azul está por encima o por debajo de la mitad del eje y
                    if y > 350:
                        if ~jugador2_salto:
                            jugador2_vel = 1.0
                            jugador2_salto = ~jugador2_salto
                        
                  


    # Mover jugadores
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if jugador1_rect.x > limite_izq:
            jugador1_rect.x -= jugador1_vel
    elif keys[pygame.K_d]:
        if jugador1_rect.x < limite_der:
            jugador1_rect.x += jugador1_vel
    if keys[pygame.K_w]:
        if ~jugador1_salto:
            jugador1_vel = 1.0
            jugador1_salto = ~jugador1_salto
    if keys[pygame.K_LEFT]:
        if jugador2_rect.x > limite_izq:
            jugador2_rect.x -= jugador2_vel
    elif keys[pygame.K_RIGHT]:
        if jugador2_rect.x < limite_der:
            jugador2_rect.x += jugador2_vel
    if keys[pygame.K_UP]:
        if ~jugador2_salto:
            jugador2_vel = 1.0
            jugador2_salto = ~jugador2_salto

    # Salto de los jugadores
    if jugador1_salto:
        t1_salto += 0.04
        jugador1_rect.y = jugador1_y0 - max_salto * t1_salto + 0.5 * g * t1_salto**2
        if jugador1_rect.y > 400:
            t1_salto = 0.0
            jugador1_vel = 2.0
            jugador1_salto = ~jugador1_salto
    
    if jugador2_salto:
        t2_salto += 0.04
        jugador2_rect.y = jugador2_y0 - max_salto * t2_salto + 0.5 * g * t2_salto**2
        if jugador2_rect.y > 400:
            t2_salto = 0.0
            jugador2_vel = 2.0
            jugador2_salto = ~jugador2_salto

    # Movimiento del balon
    t_balon += 0.04
    balon_rect.x = balon_x0 + v0x * t_balon
    balon_rect.y = balon_y0 - v0y * t_balon + 0.5 * g * t_balon**2

    # Colisiones con las paredes
    if balon_rect.bottom > 500 or balon_rect.top < 0:
        t_balon = 0.0
        v0y *= -1
        balon_x0 = balon_rect.x
        balon_y0 = balon_rect.y
    elif balon_rect.left < 0 or balon_rect.right > 1280:
        t_balon = 0.0
        v0x *= -1
        balon_x0 = balon_rect.x
        balon_y0 = balon_rect.y
    
    # Colisiones con el travesaño
    if balon_rect.colliderect(palo1):
        if ~palo1_colision:
            if balon_rect.x <= palo1.right:
                t_balon = 0.0
                v0y *= -1
                balon_x0 = balon_rect.x
                balon_y0 = balon_rect.y
            else:
                t_balon = 0.0
                v0y *= -1
                if v0x < 0:
                    v0x *= -1
                balon_x0 = balon_rect.x
                balon_y0 = balon_rect.y
            palo1_colision = ~palo1_colision
        else:
            palo1_colision = ~palo1_colision
    elif balon_rect.colliderect(palo2):
        if ~palo2_colision:
            if balon_rect.x >= palo2.left:
                t_balon = 0.0
                v0y *= -1
                balon_x0 = balon_rect.x
                balon_y0 = balon_rect.y
            else:
                t_balon = 0.0
                v0y *= -1
                if v0x > 0:
                    v0x *= -1
                balon_x0 = balon_rect.x
                balon_y0 = balon_rect.y
            palo2_colision = ~palo2_colision
        else:
            palo2_colision = ~palo2_colision
    
    # Colisiones con la red
    if balon_rect.colliderect(red1):
        # Aumentar contador de gol
        cont_jugador2 += 1
        text2 = font.render("Penaldo: " + str(cont_jugador2), True, (255, 255, 255))
        
        # Mostrar animacion de gol
        screen.blit(gol_image, gol_rect)
        pygame.display.update()
        pygame.mixer.music.load("ronaldo.wav")
        pygame.mixer.music.play()
        pygame.time.delay(2500)
        pygame.mixer.music.load("fut.wav")

# Reproduce la canción en bucle
        pygame.mixer.music.play(-1)
        pygame.time.delay(500)

        # Restablecer variables
        t_balon = 0.0
        t1_salto = 0.0
        t2_salto = 0.0
        theta = 90.0
        v0x = v0 * np.cos(np.deg2rad(theta))
        v0y = v0 * np.sin(np.deg2rad(theta))
        balon_rect.x = 600
        balon_rect.y = 450
        balon_x0 = balon_rect.x
        balon_y0 = balon_rect.y
        jugador1_rect.x = 200
        jugador1_rect.y = 400
        jugador2_rect.x = 970
        jugador2_rect.y = 400
    elif balon_rect.colliderect(red2):
        # Aumentar contador de gol
        cont_jugador1 += 1
        text1 = font.render("Frionel: " + str(cont_jugador1), True, (255, 255, 255))
        
        # Mostrar animacion de gol
        screen.blit(gol_image, gol_rect)
        pygame.display.update()
        pygame.mixer.music.load("messi.wav")
        pygame.mixer.music.play()
        pygame.time.delay(3000)
        pygame.mixer.music.load("fut.wav")

# Reproduce la canción en bucle
        pygame.mixer.music.play(-1)
        pygame.time.delay(500)

        # Restablecer variables
        t_balon = 0.0
        t1_salto = 0.0
        t2_salto = 0.0
        theta = 90.0
        v0x = v0 * np.cos(np.deg2rad(theta))
        v0y = v0 * np.sin(np.deg2rad(theta))
        balon_rect.x = 600
        balon_rect.y = 450
        balon_x0 = balon_rect.x
        balon_y0 = balon_rect.y
        jugador1_rect.x = 200
        jugador1_rect.y = 400
        jugador2_rect.x = 970
        jugador2_rect.y = 400
    
    # Coliciones con los jugadores
    if balon_rect.colliderect(jugador1_rect):
        if ~jugador1_colision:
            t_balon = 0.0
            balon_x0 = balon_rect.x
            balon_y0 = balon_rect.y
            c1 = jugador1_rect.y - balon_rect.y
            c2 = balon_rect.x - jugador1_rect.x
            theta = np.arctan(c1/c2)
            if c2 > 0:
                if c1 > 0:
                    v0x = v0 * np.cos(theta)
                    v0y = v0 * np.sin(theta)
                else:
                    v0x = v0 * np.cos(-theta)
                    v0y = v0 * np.sin(-theta)
            else:
                if c1 > 0:
                    v0x = v0 * np.cos(-theta + np.pi/2)
                    v0y = v0 * np.sin(-theta + np.pi/2)
                else:
                    v0x = v0 * np.cos(theta + np.pi/2)
                    v0y = v0 * np.sin(theta + np.pi/2)
            jugador1_colision = ~jugador1_colision
        else:
            jugador1_colision = ~jugador1_colision

    if balon_rect.colliderect(jugador2_rect):
        if ~jugador2_colision:
            t_balon = 0.0
            balon_x0 = balon_rect.x
            balon_y0 = balon_rect.y
            c1 = jugador2_rect.y - balon_rect.y
            c2 = jugador2_rect.x - balon_rect.x
            theta = np.arctan(c1/c2)
            if c2 > 0:
                if c1 > 0:
                    v0x = -v0 * np.cos(theta)
                    v0y = v0 * np.sin(theta)
                else:
                    v0x = -v0 * np.cos(-theta)
                    v0y = v0 * np.sin(-theta)
            else:
                if c1 > 0:
                    v0x = -v0 * np.cos(-theta + np.pi/2)
                    v0y = v0 * np.sin(-theta + np.pi/2)
                else:
                    v0x = -v0 * np.cos(theta + np.pi/2)
                    v0y = v0 * np.sin(theta + np.pi/2)
            jugador2_colision = ~jugador2_colision
        else:
            jugador2_colision = ~jugador2_colision

    # Dibujar objetos
    screen.blit(fondo_img, (0, 0))
    screen.blit(jugador1_img, jugador1_rect)
    screen.blit(jugador2_img, jugador2_rect)
    screen.blit(balon_img, balon_rect)
    screen.blit(porteria1_img, porteria1_rect)
    screen.blit(porteria2_img, porteria2_rect)
    screen.blit(text1, (0, 0))
    screen.blit(text2, (0, 20))


    # Actualizar pantalla
    pygame.display.flip()
