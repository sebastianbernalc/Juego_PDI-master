#--------------------------------------------------------------------------
#-----------------------------Football Head -------------------------------
#--------------------------------------------------------------------------
#-------------------------Coceptos básicos de PDI--------------------------
#--------------------------------------------------------------------------
#-------------------------Sebastian Bernal Cuaspa--------------------------
#----------------------sebastian.bernalc@udea.edu.co-----------------------
#--------------------------------------------------------------------------
#-----------------------Kevin David Martinez Zapata------------------------   
#-----------------------kevin.martinez1@udea.edu.co------------------------
#--------------------------------------------------------------------------
#------------------------Universidad De Antioquia--------------------------
#-------------------------Ingenieria Electronica---------------------------
#--------------------Procesamiento Digital De Imagenes I-------------------


#--------------------------------------------------------------------------
#--1. Inicializo el sistema -----------------------------------------------
#--------------------------------------------------------------------------

#Importamos las librerias necesarias 
import pygame      # Biblioteca de Python diseñada para la creación de videojuegos y aplicaciones multimedia interactivas.
import numpy as np # NumPy es una biblioteca de Python que se utiliza principalmente para la manipulación de matrices y vectores,
import cv2         # Permite realizar operaciones como la lectura y escritura de imágenes y vídeos, la detección de objetos, el seguimiento de objetos en movimiento...
import queue       # Permite la comunicación y sincronización de hilos en un programa de Python
import threading   # Proporciona un conjunto de herramientas para trabajar con hilos (threads) en Python.

# Inicializar el Pygame(GAME)
pygame.init() 
pygame.font.init()                      #Inicializa fuente para el juego
font = pygame.font.SysFont('Arial', 24) #Tipo de fuente del juego

# Configurar la pantalla a 1280x600.
tam_screen = (1280, 600)
screen = pygame.display.set_mode(tam_screen) #Ajusta el tamaño del juego (1280x600)
pygame.display.set_caption('Football Head')  #Titulo del juego en la pestaña del juego


#--------------------------------------------------------------------------
#--2. Camara en cola ------------------------------------------------------
#--------------------------------------------------------------------------

# Función que lee continuamente la cámara y escribe los fotogramas en la cola
def capture_frames(queue):
    camera = cv2.VideoCapture(0) #Captura de vídeo predeterminado (cámara web)
    while True:
        ret, frame = camera.read() #Si la captura fue exitosa
        if ret:
            queue.put(frame) #El fotograma capturado se agrega a la cola 
        else:
                             #De lo contrario, el bucle se rompe 
            break
    camera.release()  # libera la cámara

# Cargar imagenes
fondo_img = pygame.image.load('images/fondo.png') #Carga el fondo del juego
jugador1_img = pygame.image.load('images/jugador1.png') #Carga el jugador1
jugador2_img = pygame.image.load('images/jugador2.png') #Carga el jugador2
balon_img = pygame.image.load('images/balon.png')       #Carga el balon
porteria1_img = pygame.image.load('images/porteria1.png')#Carga la porteria1
porteria2_img = pygame.image.load('images/porteria2.png')#Carga la porteria2
gol_image = pygame.image.load("images/gol.png") #Carga la imagen de gol


# Redimensionar imagenes
fondo_img = pygame.transform.scale(fondo_img, tam_screen) # Redimensiona la pantalla del juego
jugador1_img = pygame.transform.scale(jugador1_img, (100, 100)) # Redimensionar el jugador 1
jugador2_img = pygame.transform.scale(jugador2_img, (100, 100)) # Redimensionar el jugador 2
balon_img = pygame.transform.scale(balon_img, (50, 50)) # Redimensionar el balon
porteria1_img = pygame.transform.scale(porteria1_img, (200, 250)) # Redimensionar la porteria 1
porteria2_img = pygame.transform.scale(porteria2_img, (200, 250)) # Redimensionar la porteria 2

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

#--------------------------------------------------------------------------
#--3. Almacenar frames ----------------------------------------------------
#--------------------------------------------------------------------------

frame_queue = queue.Queue() #crea una cola vacía para almacenar y acceder a elementos de manera ordenada
capture_thread = threading.Thread(target=capture_frames, args=(frame_queue,)) #se utiliza para ejecutar la función capture_frames en segundo plano como un hilo separado.
capture_thread.start() # inicia la ejecución del hilo 
pygame.mixer.music.load("fut.wav") #Carga musica al juego 

# Reproduce la canción en bucle
pygame.mixer.music.play(-1)
# Establecer el ciclo de juego
running = True
#--------------------------------------------------------------------------
#--4. Juego en marcha -----------------------------------------------------
#--------------------------------------------------------------------------
while running:
    
    for event in pygame.event.get(): #recorrer todos los eventos en la cola de eventos de Pygame
        if event.type == pygame.QUIT: #Verifica si el evento es de salida 
            running = False          #Sale del while 
            cv2.destroyAllWindows()  #Destruye todas las ventanas 
            pygame.quit()           #Cierra el juego
            quit()
    
    #--------------------------------------------------------------------------
    #--5. Inicializar la cola y el hilo de la cámara --------------------------
    #--------------------------------------------------------------------------
        
    if not frame_queue.empty():  #verifica si la cola está vacía o no. 
            kernel_erode = np.ones((10, 10), np.uint8) #crean kernel para las operaciones de erosión en una matriz de 10x10 elementos, todos los cuales son unos.
            kernel_dilate = np.ones((3, 3), np.uint8) #crean kernel para las operaciones de dilatacion en una matriz de 10x10 elementos, todos los cuales son unos.
            frame = frame_queue.get() #obtiene el siguiente marco de video de la cola
            frame = cv2.flip(frame, 1)# invierte la imagen
            
            #--------------------------------------------------------------------------
            #--6. Conversion de mascaras y aplicacion de erosion-dilatacion------------
            #--------------------------------------------------------------------------
            # Convertimos la imagen a HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Definimos el rango de colores que queremos detectar (en este caso, amarillo)
            lower_yellow = np.array([20, 100, 100]) #es el array de tres elementos que representa el límite inferior del rango de color amarillo. 
            upper_yellow = np.array([40, 255, 255]) #es el array de tres elementos que representa el límite superior del rango de color amarillo. 
            lower_blue = np.array([100, 50, 50]) #es el array de tres elementos que representa el límite inferior del rango de color azul. 
            upper_blue = np.array([130, 255, 255])#es el array de tres elementos que representa el límite superior del rango de color azul. 
            # Aplicamos mascaras
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow) # Aplicamos una máscara para obtener solo los píxeles de color amarillo
            mask2=cv2.inRange(hsv, lower_blue, upper_blue) # Aplicamos una máscara para obtener solo los píxeles de color azul
            # Aplicamos erosión y dilatación para eliminar el ruido y mejorar la detección
            mask = cv2.erode(mask, kernel_erode, iterations=2)  # Aplicamos erosión con el kernel anteriormente creado con dos iteraciones
            mask = cv2.dilate(mask, kernel_dilate, iterations=2) # Aplicamos dilatacion con el kernel anteriormente creado con dos iteraciones
            mask2 = cv2.erode(mask2, kernel_erode, iterations=2)  # Aplicamos erosión con el kernel anteriormente creado con dos iteraciones
            mask2 = cv2.dilate(mask2, kernel_dilate, iterations=2)# Aplicamos dilatacion con el kernel anteriormente creado con dos iteraciones

            # Buscamos el contorno 
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Buscamos el contorno del objeto de color amarillo
            contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Buscamos el contorno del objeto de color azul

            #--------------------------------------------------------------------------
            #--7. Usar posiciones y contorno de objeto---------------------------------
            #--------------------------------------------------------------------------
            # Si hemos encontrado algún contorno
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)# Obtenemos el contorno más grande (el objeto de color amarillo)
                x, y, w, h = cv2.boundingRect(largest_contour)# Obtenemos el rectángulo que engloba al contorno
                jugador1_rect.x = int(x * 3500 / 640)# Ajustamos la posición y tamaño del objeto de color amarillo para que se ajuste a la pantalla del juego
             
                for contour in contours: #representa un contorno en la imagen
                    x, y, w, h = cv2.boundingRect(contour) #obtener las coordenadas del rectángulo que encierra al contorno
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #dibuja un rectángulo en la imagen 
                    if(x>218): #Si el objeto sale de la pantalla 
                        jugador1_rect.x=1192 #Muestra el objeto en el extremo
                    # Comprobar si el objeto azul está por encima o por debajo de la mitad del eje y
                    if y<100:
                        if ~jugador1_salto:    #Bandera para saltar
                            jugador1_vel = 1.0 #Velocidad de salto
                            jugador1_salto = ~jugador1_salto #Negar bandera para que pueda volver a caer el objeto
                   
            # Si hemos encontrado algún contor
            if contours2:
                largest_contour = max(contours2, key=cv2.contourArea)# Obtenemos el contorno más grande (el objeto de color amarillo)
                x, y, w, h = cv2.boundingRect(largest_contour) # Obtenemos el rectángulo que engloba al contorno
                jugador2_rect.x = int(x*(3500/640)-1500)# Ajustamos la posición y tamaño del objeto de color amarillo para que se ajuste a la pantalla del juego
                
                for contour in contours2:  #representa un contorno en la imagen
                    x, y, w, h = cv2.boundingRect(contour)#obtener las coordenadas del rectángulo que encierra al contorno
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)#dibuja un rectángulo en la imagen 
                    cv2.imshow('Color detector', frame) #Muestra los contornos de los colores
                    if(jugador2_rect.x<9): #Si el objeto sale de la pantalla  
                        jugador2_rect.x=9 #Muestra el objeto en el extremo
                    
                    #Comprueba si supero limite en y para saltar
                    if y < 100:
                        if ~jugador2_salto: #Bandera para saltar
                            jugador2_vel = 1.0 #Velocidad de salto
                            jugador2_salto = ~jugador2_salto#Negar bandera para que pueda volver a caer el objeto
                        
    #--------------------------------------------------------------------------
    #--8. Teclas de juego en caso opcional ------------------------------------
    #--------------------------------------------------------------------------

    # Mover jugadores
    keys = pygame.key.get_pressed()     #Si se presiona una tecla
    if keys[pygame.K_a]:                #Si se presiona la tecla a
        if jugador1_rect.x > limite_izq: #si la posición del rectángulo "jugador1_rect" no supere el límite izquierdo
            jugador1_rect.x -= jugador1_vel  #mueve el rectángulo que representa al objeto "jugador1" hacia la izquierda,
    elif keys[pygame.K_d]:              #Si se presiona la tecla d
        if jugador1_rect.x < limite_der: # si la posición del rectángulo "jugador1_rect" no supere el límite derecho
            jugador1_rect.x += jugador1_vel#mueve el rectángulo que representa al objeto "jugador1" hacia la derecha
    if keys[pygame.K_w]:                #Si se presiona la tecla w
        if ~jugador1_salto:             #Bandera para saltar
            jugador1_vel = 1.0          #Velocidad de salto
            jugador1_salto = ~jugador1_salto #Negar bandera para que pueda volver a caer el objeto
    if keys[pygame.K_LEFT]:             #Si se presiona la tecla flecha izquiera
        if jugador2_rect.x > limite_izq:# si la posición del rectángulo "jugador2_rect" no supere el límite izquierdo
            jugador2_rect.x -= jugador2_vel#mueve el rectángulo que representa al objeto "jugador2" hacia la izquierda,
    elif keys[pygame.K_RIGHT]:           #Si se presiona la tecla flecha derecha
        if jugador2_rect.x < limite_der:# si la posición del rectángulo "jugador2_rect" no supere el límite derecho
            jugador2_rect.x += jugador2_vel#mueve el rectángulo que representa al objeto "jugador1" hacia la derecha
    if keys[pygame.K_UP]:               #Si se presiona la tecla flecha arriba
        if ~jugador2_salto:             #Bandera para saltar
            jugador2_vel = 1.0          #Velocidad de salto
            jugador2_salto = ~jugador2_salto#Negar bandera para que pueda volver a caer el objeto

    #--------------------------------------------------------------------------
    #--9. Salto de objetos y fisica del balon ---------------------------------
    #--------------------------------------------------------------------------
    # Salto de los jugadores
    if jugador1_salto:    #Si la bandera esta activa 
        t1_salto += 0.04  #función del tiempo de salto 
        jugador1_rect.y = jugador1_y0 - max_salto * t1_salto + 0.5 * g * t1_salto**2 #Movimiento parabolico de salto
        if jugador1_rect.y > 400: #Si el jugador alcanza una altura máxima y su posición vertical supera los 400 píxeles
            t1_salto = 0.0 #Resetea la funcion del tiempo 
            jugador1_vel = 2.0 #Velocidad de caiga
            jugador1_salto = ~jugador1_salto #Actualiza bandera
    
    if jugador2_salto:  #Si la bandera esta activa 
        t2_salto += 0.04 #función del tiempo de salto 
        jugador2_rect.y = jugador2_y0 - max_salto * t2_salto + 0.5 * g * t2_salto**2#Movimiento parabolico de salto
        if jugador2_rect.y > 400: #Si el jugador alcanza una altura máxima y su posición vertical supera los 400 píxeles
            t2_salto = 0.0#Resetea la funcion del tiempo 
            jugador2_vel = 2.0#Velocidad de caiga
            jugador2_salto = ~jugador2_salto#Actualiza bandera

    # Movimiento del balon
    t_balon += 0.04 #Funcion del tiempo del balon 
    balon_rect.x = balon_x0 + v0x * t_balon #Movimiento parabolico del balon en x
    balon_rect.y = balon_y0 - v0y * t_balon + 0.5 * g * t_balon**2#Movimiento parabolico del balon en y

    #--------------------------------------------------------------------------
    #--9. Colisiones de objetos con balon---- ---------------------------------
    #--------------------------------------------------------------------------
    # Colisiones con las paredes
    if balon_rect.bottom > 500 or balon_rect.top < 0: #Actualiza posicion del balon en x
        t_balon = 0.0 #Funcuon del tiempo 0 
        v0y *= -1 #Velocidad negativa para bajar 
        balon_x0 = balon_rect.x #Actualiza posicion del balon en x
        balon_y0 = balon_rect.y #Actualiza posicion del balon en y
    elif balon_rect.left < 0 or balon_rect.right > 1280: #Si el balon choca en el extremo derecho
        t_balon = 0.0#Funcuon del tiempo 0 
        v0x *= -1#Velocidad negativa para volver
        balon_x0 = balon_rect.x #Actualiza posicion del balon en x
        balon_y0 = balon_rect.y #Actualiza posicion del balon en y
    
    # Colisiones con el travesaño
    if balon_rect.colliderect(palo1): #Si el balon choca en el palo de la porteria 1
        if ~palo1_colision:  #Bandera de colision
            if balon_rect.x <= palo1.right: #Si choca con el palo de la derecha
                t_balon = 0.0#Funcuon del tiempo 0 
                v0y *= -1#Velocidad negativa para volver
                balon_x0 = balon_rect.x#Actualiza posicion del balon en x
                balon_y0 = balon_rect.y#Actualiza posicion del balon en y
            else:
                t_balon = 0.0 #Funcuon del tiempo 0 
                v0y *= -1#Velocidad negativa para volver
                if v0x < 0: #Si la velocidad es menor 
                    v0x *= -1#Velocidad negativa para volver
                balon_x0 = balon_rect.x#Actualiza posicion del balon en x
                balon_y0 = balon_rect.y#Actualiza posicion del balon en y
            palo1_colision = ~palo1_colision #Actualiza la bandera de colision del palo
        else:
            palo1_colision = ~palo1_colision #Actualiza la bandera de colision del palo
    elif balon_rect.colliderect(palo2):#Si el balon choca en el palo de la porteria 1
        if ~palo2_colision:#Bandera de colision
            if balon_rect.x >= palo2.left:#Si choca con el palo de la izquierda
                t_balon = 0.0#Funcuon del tiempo 0 
                v0y *= -1#Velocidad negativa para volver
                balon_x0 = balon_rect.x#Actualiza posicion del balon en x
                balon_y0 = balon_rect.y#Actualiza posicion del balon en y
            else:
                t_balon = 0.0#Funcuon del tiempo 0 
                v0y *= -1#Velocidad negativa para volver
                if v0x > 0:#Si la velocidad es menor 
                    v0x *= -1#Velocidad negativa para volver
                balon_x0 = balon_rect.x#Actualiza posicion del balon en x
                balon_y0 = balon_rect.y#Actualiza posicion del balon en x
            palo2_colision = ~palo2_colision#Actualiza la bandera de colision del palo
        else:
            palo2_colision = ~palo2_colision#Actualiza la bandera de colision del palo
    
    # Colisiones con la red
    if balon_rect.colliderect(red1):  #Si el balon entra a la porteria 1
        # Aumentar contador de gol
        cont_jugador2 += 1
        text2 = font.render("Penaldo: " + str(cont_jugador2), True, (255, 255, 255)) #Se actualiza el marcador para penaldo
        
        # Mostrar animacion de gol
        screen.blit(gol_image, gol_rect)
        pygame.display.update() #Actualiza la pantalla 
        pygame.mixer.music.load("ronaldo.wav") #Se carga audio
        pygame.mixer.music.play()#Se escucha narrador diciendo gol
        pygame.time.delay(2500) #Espera dos segundos y medio
        pygame.mixer.music.load("fut.wav") #Vuelve a cargar musica de fondo

        # Reproduce la canción en bucle
        pygame.mixer.music.play(-1)
        pygame.time.delay(500)#Espera medio segundo

        # Restablecer variables
        t_balon = 0.0  #Funcion del tiempo del balon
        t1_salto = 0.0 #Funcion del tiempo del salto jugador 1
        t2_salto = 0.0 #Funcion del tiempo del salto jugador 2
        theta = 90.0 #Angulo inicial 
        v0x = v0 * np.cos(np.deg2rad(theta)) #Velocidad en x
        v0y = v0 * np.sin(np.deg2rad(theta)) #Velocidad en y
        balon_rect.x = 600 #Posicion del balon en x
        balon_rect.y = 450 #Posicion del balon en y
        balon_x0 = balon_rect.x #Actualiza posicion del balon en x
        balon_y0 = balon_rect.y #Actualiza posicion del balon en y
        jugador1_rect.x = 200 #Posicion del jugador 1 en x
        jugador1_rect.y = 400 #Posicion del jugador 1 en y
        jugador2_rect.x = 970 #Posicion del jugador 2 en x
        jugador2_rect.y = 400 #Posicion del jugador 2 en y


    elif balon_rect.colliderect(red2): #Si el balon entra en la porteria 2 
        # Aumentar contador de gol
        cont_jugador1 += 1
        text1 = font.render("Frionel: " + str(cont_jugador1), True, (255, 255, 255)) #Se actualiza el marcador para frionel
        
        # Mostrar animacion de gol
        screen.blit(gol_image, gol_rect)
        pygame.display.update() #Se actualiza pantalla 
        pygame.mixer.music.load("messi.wav")#Se carga audio
        pygame.mixer.music.play()#Se escucha narrador diciendo gol
        pygame.time.delay(3000)#Se espera 3 segundos
        pygame.mixer.music.load("fut.wav")#Carga de nuevo la musica de fondo

        # Reproduce la canción en bucle
        pygame.mixer.music.play(-1)
        pygame.time.delay(500) #Se espera medio segundo

        # Restablecer variables
        t_balon = 0.0 #Funcion del tiempo del balon
        t1_salto = 0.0 #Funcion del tiempo del salto jugador 1
        t2_salto = 0.0 #Funcion del tiempo del salto jugador 2
        theta = 90.0 #Angulo inicial 
        v0x = v0 * np.cos(np.deg2rad(theta)) #Velocidad en x
        v0y = v0 * np.sin(np.deg2rad(theta)) #Velocidad en y
        balon_rect.x = 600 #Posicion del balon en x
        balon_rect.y = 450 #Posicion del balon en y
        balon_x0 = balon_rect.x #Actualiza posicion del balon en x
        balon_y0 = balon_rect.y #Actualiza posicion del balon en y
        jugador1_rect.x = 200 #Posicion del jugador 1 en x
        jugador1_rect.y = 400 #Posicion del jugador 1 en y
        jugador2_rect.x = 970 #Posicion del jugador 2 en x
        jugador2_rect.y = 400 #Posicion del jugador 2 en y
    
    # Coliciones con los jugadores
    if balon_rect.colliderect(jugador1_rect): #Si choca con el jugador 1
        if ~jugador1_colision: #Bandera de choque jugador 1
            t_balon = 0.0 #Funcuon del tiempo del balon 
            balon_x0 = balon_rect.x  #Actualiza posicion del balon en x
            balon_y0 = balon_rect.y  #Actualiza posicion del balon en y
            c1 = jugador1_rect.y - balon_rect.y # distancia de colision en x para que no atraviese el jugadro
            c2 = balon_rect.x - jugador1_rect.x # distancia de colision en y para que no atraviese el jugador
            theta = np.arctan(c1/c2)  #Nuevo angulo dependiendo del choque la posicion
            if c2 > 0:  # si la pelota está por encima del jugador2
                if c1 > 0: # si la pelota está por encima del jugador1
                    v0x = v0 * np.cos(theta) #calcula la velocidad en x del impacto en función de la posición de la pelota en relación con el jugador
                    v0y = v0 * np.sin(theta) #calcula el velocidad en y del impacto en función de la posición de la pelota en relación con el jugador
                else:
                    v0x = v0 * np.cos(-theta) #calcula el velocidad en x del impacto en función de la posición de la pelota en relación con el jugador
                    v0y = v0 * np.sin(-theta) #calcula el velocidad en y del impacto en función de la posición de la pelota en relación con el jugador
            else:
                if c1 > 0:  #Si la pelota está por encima del jugador1
                    v0x = v0 * np.cos(-theta + np.pi/2) #calcula el velocidad en x del impacto en función de la posición de la pelota en relación con el jugador
                    v0y = v0 * np.sin(-theta + np.pi/2) #calcula el velocidad en y del impacto en función de la posición de la pelota en relación con el jugador
                else:
                    v0x = v0 * np.cos(theta + np.pi/2) #calcula el velocidad en x del impacto en función de la posición de la pelota en relación con el jugador
                    v0y = v0 * np.sin(theta + np.pi/2) #calcula el velocidad en y del impacto en función de la posición de la pelota en relación con el jugador
            jugador1_colision = ~jugador1_colision #Actualiza bandera
        else:
            jugador1_colision = ~jugador1_colision #Actualiza bandera

    if balon_rect.colliderect(jugador2_rect): #Si choca con el jugador 2
        if ~jugador2_colision: #Bandera de choque jugador 2
            t_balon = 0.0 #Funcion del tiempo del balon 
            balon_x0 = balon_rect.x #Actualiza posicion del balon en x
            balon_y0 = balon_rect.y #Actualiza posicion del balon en y
            c1 = jugador2_rect.y - balon_rect.y # distancia de colision en x para que no atraviese el jugadro
            c2 = jugador2_rect.x - balon_rect.x# distancia de colision en y para que no atraviese el jugadro
            theta = np.arctan(c1/c2) #Nuevo angulo dependiendo del choque la posicion
            if c2 > 0: # si la pelota está por encima del jugador2
                if c1 > 0: # si la pelota está por encima del jugador1
                    v0x = -v0 * np.cos(theta)
                    v0y = v0 * np.sin(theta)
                else:
                    v0x = -v0 * np.cos(-theta)
                    v0y = v0 * np.sin(-theta)
            else:
                if c1 > 0: # si la pelota está por encima del jugador2
                    v0x = -v0 * np.cos(-theta + np.pi/2) #calcula la velocidad en x del impacto en función de la posición de la pelota en relación con el jugador
                    v0y = v0 * np.sin(-theta + np.pi/2) #calcula la velocidad en y del impacto en función de la posición de la pelota en relación con el jugador
                else:
                    v0x = -v0 * np.cos(theta + np.pi/2) #calcula la velocidad en x del impacto en función de la posición de la pelota en relación con el jugador
                    v0y = v0 * np.sin(theta + np.pi/2) #calcula la velocidad en y del impacto en función de la posición de la pelota en relación con el jugador
            jugador2_colision = ~jugador2_colision #Actualizo banderas
        else:
            jugador2_colision = ~jugador2_colision #Actualizo banderas

    #--------------------------------------------------------------------------
    #--10. Dibujo de objetos---------------------------------------------------
    #--------------------------------------------------------------------------
    # Dibujar objetos
    screen.blit(fondo_img, (0, 0)) # Dibujar fondo 
    screen.blit(jugador1_img, jugador1_rect) # Dibujar jugador 1
    screen.blit(jugador2_img, jugador2_rect) # Dibujar jugador 2
    screen.blit(balon_img, balon_rect) # Dibujar balon
    screen.blit(porteria1_img, porteria1_rect) # Dibujar porteria 1
    screen.blit(porteria2_img, porteria2_rect) # Dibujar porteria 2
    screen.blit(text1, (0, 0)) # Dibujar texto de marcador
    screen.blit(text2, (0, 20)) # Dibujar texto de marcador


    # Actualizar pantalla
    pygame.display.flip()

#--------------------------------------------------------------------------
#---------------------------  FIN DEL PROGRAMA ----------------------------
#--------------------------------------------------------------------------
