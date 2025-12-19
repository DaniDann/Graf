import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


def crear_arbol_navidad_pixel_art():
    ancho, alto = 35, 45
    arbol = np.full((alto, ancho), 240, dtype=np.uint8)

    VERDE_OSCURO = 60
    VERDE_CLARO = 100
    MARRON = 80
    ROJO = 30
    AMARILLO = 200
    AZUL = 170
    BLANCO = 255
    DORADO = 180

    # ESTRELLA EN LA PUNTA
    estrella_pixels = [
        (2, [17]),
        (3, [16, 17, 18]),
        (4, [15, 16, 17, 18, 19]),
        (5, [16, 17, 18]),
    ]

    for y, x_positions in estrella_pixels:
        for x in x_positions:
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = AMARILLO

    arbol[4, 17] = DORADO

    # ÁRBOL - Sección superior (usando rangos)
    centro_x = ancho // 2
    for i in range(5):
        y = 6 + i
        mitad_ancho = (3 + i * 2) // 2
        x_inicio = centro_x - mitad_ancho
        x_fin = centro_x + mitad_ancho + 1

        for x in range(x_inicio, x_fin):
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = VERDE_OSCURO

    # ÁRBOL - Sección media (usando rangos)
    for i in range(6):
        y = 11 + i
        mitad_ancho = (7 + i * 2) // 2
        x_inicio = centro_x - mitad_ancho
        x_fin = centro_x + mitad_ancho + 1

        for x in range(x_inicio, x_fin):
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = VERDE_OSCURO

    # ÁRBOL - Sección inferior (usando rangos)
    centro_x = ancho // 2
    fila_inicio = 17
    ancho_inicial = 11

    for i in range(8):
        y = fila_inicio + i
        mitad_ancho = (ancho_inicial + i * 2) // 2
        x_inicio = centro_x - mitad_ancho
        x_fin = centro_x + mitad_ancho + 1

        for x in range(x_inicio, x_fin):
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = VERDE_OSCURO

    # Profundidad
    profundidad_pixels = [
        (7, [16, 17, 18]),
        (9, [14, 15, 19, 20]),
        (12, [14, 15, 19, 20]),
        (14, [12, 13, 21, 22]),
        (16, [11, 12, 22, 23]),
        (19, [12, 13, 21, 22]),
        (21, [10, 11, 23, 24]),
        (23, [8, 9, 25, 26]),
    ]

    for y, x_positions in profundidad_pixels:
        for x in x_positions:
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = VERDE_CLARO

    # ADORNOS ROJOS
    adornos_rojos = [
        (8, 17),
        (10, 14), (10, 20),
        (13, 15), (13, 19),
        (16, 12), (16, 22),
        (19, 14), (19, 20),
        (22, 10), (22, 24),
    ]

    for y, x in adornos_rojos:
        if 0 <= y < alto and 0 <= x < ancho:
            arbol[y, x] = ROJO
            if x + 1 < ancho:
                arbol[y, x + 1] = ROJO

    # ADORNOS AZULES
    adornos_azules = [
        (9, 16), (9, 18),
        (12, 17),
        (15, 13), (15, 21),
        (18, 16),
        (21, 13), (21, 21),
        (23, 17),
    ]

    for y, x in adornos_azules:
        if 0 <= y < alto and 0 <= x < ancho:
            arbol[y, x] = AZUL
            if x + 1 < ancho:
                arbol[y, x + 1] = AZUL

    # ADORNOS DORADOS
    adornos_dorados = [
        (11, 16),
        (14, 17),
        (17, 15), (17, 19),
        (20, 17),
    ]

    for y, x in adornos_dorados:
        if 0 <= y < alto and 0 <= x < ancho:
            arbol[y, x] = DORADO

    # TRONCO
    tronco_pixels = [
        (25, [15, 16, 17, 18, 19]),
        (26, [15, 16, 17, 18, 19]),
        (27, [15, 16, 17, 18, 19]),
        (28, [15, 16, 17, 18, 19]),
        (29, [15, 16, 17, 18, 19]),
    ]

    for y, x_positions in tronco_pixels:
        for x in x_positions:
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = MARRON

    arbol[26, 16] = MARRON - 20
    arbol[27, 18] = MARRON - 20
    arbol[28, 17] = MARRON - 20

    # BASE
    base_pixels = [
        (30, [13, 14, 15, 16, 17, 18, 19, 20, 21]),
        (31, [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]),
        (32, [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]),
        (33, [13, 14, 15, 16, 17, 18, 19, 20, 21]),
    ]

    for y, x_positions in base_pixels:
        for x in x_positions:
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = ROJO

    for x in [14, 15, 16, 17, 18, 19, 20]:
        arbol[31, x] = ROJO - 10

    # NIEVE
    for y in [34, 35, 36]:
        for x in range(0, 35):
            if 0 <= y < alto and 0 <= x < ancho:
                arbol[y, x] = BLANCO

    # COPOS DE NIEVE
    copos_nieve = [
        (5, 8), (7, 27), (10, 5), (12, 30),
        (15, 3), (18, 32), (20, 7), (22, 29),
    ]

    for y, x in copos_nieve:
        if 0 <= y < alto and 0 <= x < ancho:
            arbol[y, x] = BLANCO

    return arbol


def mostrar_arbol(imagen):
    factor_escala = 12
    alto, ancho = imagen.shape
    arbol_escalado = cv.resize(imagen, (ancho * factor_escala, alto * factor_escala),
                               interpolation=cv.INTER_NEAREST)

    cv.imshow('Arbol de Navidad - Pixel Art', arbol_escalado)
    return arbol_escalado


def guardar_imagen(imagen, nombre_archivo='arbol_navidad_pixel_art.png', escala=15):
    alto, ancho = imagen.shape
    imagen_hd = cv.resize(imagen, (ancho * escala, alto * escala),
                          interpolation=cv.INTER_NEAREST)
    cv.imwrite(nombre_archivo, imagen_hd)


def main():
    arbol_imagen = crear_arbol_navidad_pixel_art()
    guardar_imagen(arbol_imagen)
    mostrar_arbol(arbol_imagen)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()