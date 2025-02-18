import pygame
import random
import math
from pygame import mixer
import io

# Inicai pygame
pygame.init()

# Crea pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título, ícono, fondo
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo.jpg")


# agregar música
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)


# Pasarlo a ser una app, 1° cambiar letras a Bytes
def fuente_bytes(fuente):
    # abre archivo letras TTF en modo lectura binaria
    with open(fuente, 'rb') as f:
        # leer bytes y guardar en variable
        ttf_bytes = f.read()
        # crear objeto BytesIO
        return io.BytesIO(ttf_bytes)


# Crar Jugador y variables
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 510
jugador_x_cambio = 0

# Crar Enemigo y variables
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)


# Crar Bala y variables
img_bala = pygame.image.load("sala.png")
bala_x = 0
bala_y = 510
bala_x_cambio = 0
bala_y_cambio = 1.5
bala_visible = False


# puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("FreeSansBold.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10


# Texto fin del juego
fuente_final = pygame.font.Font(fuente_como_bytes, 50)


def texto_final():
    mi_fuente_fin = fuente_final.render(
        "JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_fin, (100, 200))


# func mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# incluir jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# incluir enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# func disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+16, y+10))


# func calcular colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# loop del juego ejecutándose
se_ejecuta = True

while se_ejecuta:
    # imagen de fondo
    pantalla.blit(fondo, (0, 0))
    # Cerrar el programa
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        # presionar teclas mov
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        # soltar felcha
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # mover jugador
    jugador_x += jugador_x_cambio

    # mantener dentro de los bordes jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # mover bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    # mover enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # mantener dentro de los bordes enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)
        # llamar enemigo
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # llamar jugador
    jugador(jugador_x, jugador_y)

    # mostara puntaje
    mostrar_puntaje(texto_x, texto_y)

    # actualiza pantalla
    pygame.display.update()
