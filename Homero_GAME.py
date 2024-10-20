import pygame
import random
import time

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Homero y Sus Donas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (238, 238, 0)  # Fondo amarillo del inicio

# Fuente para texto
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Función para mostrar texto
def mostrar_texto(texto, fuente, color, x, y):
    text = fuente.render(texto, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, y))
    screen.blit(text, text_rect)
# Pantalla de inicio
def pantalla_de_inicio():
    inicio_activo = True
    while inicio_activo:
        screen.fill(YELLOW)  # Fondo para el inicio

        # Mostrar el nombre del juego y opciones
        mostrar_texto("Homero y Sus Donas", font, BLACK, WIDTH // 6, HEIGHT // 4)
        mostrar_texto("1. Jugar", small_font, BLACK, WIDTH // 3, HEIGHT // 2)
        mostrar_texto("2. Ajustes", small_font, BLACK, WIDTH // 3, HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True  # Comenzar el juego
                if event.key == pygame.K_2:
                    pantalla_ajustes()

        pygame.display.flip()

# Función de Ajustes
def pantalla_ajustes():
    ajustes_activo = True
    while ajustes_activo:
        screen.fill(WHITE)  # Fondo blanco para los ajustes

        # Mostrar opciones de ajustes
        mostrar_texto("Ajustes", font, BLACK, WIDTH // 3, HEIGHT // 4)
        mostrar_texto("Presiona ESC para volver", small_font, BLACK, WIDTH // 3, HEIGHT // 2)
        mostrar_texto("usar las teclas direccionales derecha y izquierda para jugar", small_font, BLACK, WIDTH , HEIGHT// 2 + 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ajustes_activo = False

        pygame.display.flip()

# Función del juego
def juego():
    # Cargar imágenes
    homero_img = pygame.image.load(r'd:\Homero_GAME\homero.png')
    dona_img = pygame.image.load(r'd:\Homero_GAME\dona.png')
    dona_malvada_img = pygame.image.load(r'd:\Homero_GAME\dona_malvada.jpg')  # Cambiado a .jpg

    # Cambiar el tamaño de las imágenes
    homero_img = pygame.transform.scale(homero_img, (150, 150))  # Cambia el tamaño de Homero a 150x150 píxeles
    dona_img = pygame.transform.scale(dona_img, (50, 50))  # Cambia el tamaño de la dona a 50x50 píxeles
    dona_malvada_img = pygame.transform.scale(dona_malvada_img, (50, 50))  # Cambia el tamaño de la dona malvada a 50x50 píxeles

    homero_rect = homero_img.get_rect()
    homero_rect.midbottom = (WIDTH // 2, HEIGHT - 10)  # Posición inicial de Homero en la parte inferior

    # Lista de donas
    donas = []
    dona_rect = dona_img.get_rect()

    # Contadores
    donas_comidas = 0
    donas_perdidas = 0
    velocidad_donas = 1  # Reducir aún más la velocidad de las donas
    tiempo_inicio = time.time()

    # Función para crear una nueva dona
    def crear_dona():
        x = random.randint(0, WIDTH - dona_rect.width)
        y = -dona_rect.height
        tipo = random.choice(['normal', 'malvada'])
        return pygame.Rect(x, y, dona_rect.width, dona_rect.height), tipo

    # Crear la primera dona
    donas.append(crear_dona())

    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pantalla_de_inicio()

        # Funciona mientras las teclas están presionadas
        lista_teclas = pygame.key.get_pressed()
        if True in lista_teclas:
            if lista_teclas[pygame.K_RIGHT]:
                homero_rect.x += 5  # Se mueve 5 píxeles mientras la tecla está presionada
            if lista_teclas[pygame.K_LEFT]:
                homero_rect.x -= 5
            if lista_teclas[pygame.K_UP]:
                homero_rect.y -= 5
            if lista_teclas[pygame.K_DOWN]:
                homero_rect.y += 5

        # Mantener a Homero dentro de los límites de la pantalla
        if homero_rect.left < 0:
            homero_rect.left = 0
        if homero_rect.right > WIDTH:
            homero_rect.right = WIDTH
        if homero_rect.top < 0:
            homero_rect.top = 0
        if homero_rect.bottom > HEIGHT:
            homero_rect.bottom = HEIGHT

        # Mover las donas
        for dona in donas:
            dona[0].y += velocidad_donas  # Velocidad de caída de las donas
            if dona[0].y > HEIGHT:
                donas.remove(dona)
                donas.append(crear_dona())
                donas_perdidas += 1
                if donas_perdidas > 3:
                    mostrar_texto("¡Perdiste!", font, BLACK, WIDTH // 3, HEIGHT // 3)
                    pygame.display.flip()
                    time.sleep(2)
                    pantalla_de_inicio()

        # Detectar colisiones
        for dona in donas:
            if homero_rect.colliderect(dona[0]):
                donas.remove(dona)
                donas.append(crear_dona())
                donas_comidas += 1
                if dona[1] == 'malvada':
                    velocidad_donas += 1  # Aumenta la velocidad de las donas

        # Verificar si ganó
        if time.time() - tiempo_inicio > 15:
            if donas_comidas >= 10:  # Ajusta este número según la dificultad deseada
                mostrar_texto("¡Ganaste!", font, BLACK, WIDTH // 3, HEIGHT // 3)
                pygame.display.flip()
                time.sleep(2)
                pantalla_de_inicio()

        # Dibuja todo en la pantalla
        screen.fill((135, 206, 250))  # Fondo azul claro durante el juego
        screen.blit(homero_img, homero_rect)  # Dibuja a Homero
        for dona in donas:
            if dona[1] == 'malvada':
                screen.blit(dona_malvada_img, dona[0])  # Dibuja las donas malvadas
            else:
                screen.blit(dona_img, dona[0])  # Dibuja las donas normales

        # Mostra contadores
        mostrar_texto(f"Comidas: {donas_comidas}", small_font, BLACK, 10, 10)
        mostrar_texto(f"Perdidas: {donas_perdidas}", small_font, BLACK, 10, 50)

        pygame.display.flip()  # Actualiza la pantalla

    pygame.quit()

if __name__ == "__main__":
    if pantalla_de_inicio():
        juego()