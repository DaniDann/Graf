import cv2
import numpy as np
from collections import deque

# Variables globales
captura = cv2.VideoCapture(0)
captura.set(3, 1280)
captura.set(4, 720)

# Estado del programa
modo_actual = "dibujar"  # "dibujar" o "figuras"
tipo_figura = "circulo"  # "circulo", "rectangulo", "triangulo", "estrella"

# Rangos de color en HSV
rango_amarillo_bajo = np.array([20, 100, 100])
rango_amarillo_alto = np.array([30, 255, 255])
rango_azul_bajo = np.array([100, 100, 100])
rango_azul_alto = np.array([130, 255, 255])

# Canvas donde dibujamos
lienzo = np.zeros((720, 1280, 3), dtype=np.uint8)
puntos_trazo = deque(maxlen=50)

# Variables para figuras
tamaño_figura = 50
rotacion_figura = 0
posicion_anterior = None


def detectar_color_amarillo(cuadro):
    """Detecta el objeto amarillo y devuelve su centro"""
    hsv = cv2.cvtColor(cuadro, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, rango_amarillo_bajo, rango_amarillo_alto)

    # Limpiar ruido
    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.erode(mascara, kernel, iterations=2)
    mascara = cv2.dilate(mascara, kernel, iterations=2)

    # Buscar contornos
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contornos) > 0:
        contorno_grande = max(contornos, key=cv2.contourArea)
        area = cv2.contourArea(contorno_grande)

        if area > 500:
            momentos = cv2.moments(contorno_grande)
            if momentos["m00"] != 0:
                centro_x = int(momentos["m10"] / momentos["m00"])
                centro_y = int(momentos["m01"] / momentos["m00"])
                return (centro_x, centro_y)

    return None


def detectar_color_azul(cuadro):
    """Detecta el objeto azul"""
    hsv = cv2.cvtColor(cuadro, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, rango_azul_bajo, rango_azul_alto)

    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.erode(mascara, kernel, iterations=2)
    mascara = cv2.dilate(mascara, kernel, iterations=2)

    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contornos) > 0:
        contorno_grande = max(contornos, key=cv2.contourArea)
        if cv2.contourArea(contorno_grande) > 500:
            momentos = cv2.moments(contorno_grande)
            if momentos["m00"] != 0:
                centro_x = int(momentos["m10"] / momentos["m00"])
                centro_y = int(momentos["m01"] / momentos["m00"])
                return (centro_x, centro_y)

    return None


def dibujar_trazo_libre(cuadro, centro):
    """Dibuja el trazo continuo con efecto de nebulosa"""
    global puntos_trazo

    puntos_trazo.append(centro)

    # Dibujar líneas entre puntos
    for i in range(1, len(puntos_trazo)):
        if puntos_trazo[i - 1] is None or puntos_trazo[i] is None:
            continue

        # Calcular grosor y color
        grosor = int(np.sqrt(50 / float(i + 1)) * 8)
        intensidad = 255 - int(i * 255 / len(puntos_trazo))

        # Color espacial
        color_r = int(intensidad * 0.5)
        color_g = int(intensidad * 0.3)
        color_b = intensidad

        cv2.line(lienzo, puntos_trazo[i - 1], puntos_trazo[i],
                 (color_b, color_g, color_r), grosor)
        cv2.line(cuadro, puntos_trazo[i - 1], puntos_trazo[i],
                 (color_b, color_g, color_r), grosor)


def calcular_movimiento(posicion_actual):
    """Calcula el vector de movimiento del landmark"""
    global posicion_anterior

    if posicion_anterior is None:
        posicion_anterior = posicion_actual
        return 0, 0, 0

    diferencia_x = posicion_actual[0] - posicion_anterior[0]
    diferencia_y = posicion_actual[1] - posicion_anterior[1]
    magnitud = np.sqrt(diferencia_x ** 2 + diferencia_y ** 2)

    posicion_anterior = posicion_actual
    return diferencia_x, diferencia_y, magnitud


def dibujar_circulo(superficie, centro, tamaño, color):
    """Dibuja un círculo (planeta)"""
    cv2.circle(superficie, centro, tamaño, color, -1)
    cv2.circle(superficie, centro, tamaño + 5, (255, 255, 255), 2)
    cv2.circle(superficie, centro, int(tamaño * 0.7), (100, 100, 100), 1)


def dibujar_rectangulo(superficie, centro, tamaño, rotacion, color):
    """Dibuja un rectángulo rotado (nave)"""
    ancho = int(tamaño * 1.5)
    alto = tamaño

    # Puntos del rectángulo sin rotar
    puntos = np.array([
        [-ancho // 2, -alto // 2],
        [ancho // 2, -alto // 2],
        [ancho // 2, alto // 2],
        [-ancho // 2, alto // 2]
    ], dtype=np.float32)

    # Rotar puntos
    angulo_rad = np.radians(rotacion)
    cos_a = np.cos(angulo_rad)
    sin_a = np.sin(angulo_rad)

    puntos_rotados = []
    for punto in puntos:
        x_nuevo = punto[0] * cos_a - punto[1] * sin_a
        y_nuevo = punto[0] * sin_a + punto[1] * cos_a
        puntos_rotados.append([x_nuevo + centro[0], y_nuevo + centro[1]])

    puntos_rotados = np.array(puntos_rotados, dtype=np.int32)

    cv2.fillPoly(superficie, [puntos_rotados], color)
    cv2.polylines(superficie, [puntos_rotados], True, (255, 255, 255), 2)


def dibujar_triangulo(superficie, centro, tamaño, rotacion, color):
    """Dibuja un triángulo rotado (cometa)"""
    altura = int(tamaño * 1.5)

    # Puntos del triángulo
    puntos = np.array([
        [0, -altura],
        [-tamaño, altura // 2],
        [tamaño, altura // 2]
    ], dtype=np.float32)

    # Rotar
    angulo_rad = np.radians(rotacion)
    cos_a = np.cos(angulo_rad)
    sin_a = np.sin(angulo_rad)

    puntos_rotados = []
    for punto in puntos:
        x_nuevo = punto[0] * cos_a - punto[1] * sin_a
        y_nuevo = punto[0] * sin_a + punto[1] * cos_a
        puntos_rotados.append([x_nuevo + centro[0], y_nuevo + centro[1]])

    puntos_rotados = np.array(puntos_rotados, dtype=np.int32)

    cv2.fillPoly(superficie, [puntos_rotados], color)
    cv2.polylines(superficie, [puntos_rotados], True, (255, 255, 255), 2)


def dibujar_estrella(superficie, centro, tamaño, rotacion, color):
    """Dibuja una estrella de 5 puntas"""
    radio_exterior = tamaño
    radio_interior = int(tamaño * 0.4)
    numero_puntas = 5

    puntos = []
    for i in range(numero_puntas * 2):
        angulo = np.radians(rotacion + i * 360 / (numero_puntas * 2) - 90)
        radio = radio_exterior if i % 2 == 0 else radio_interior
        x = centro[0] + int(radio * np.cos(angulo))
        y = centro[1] + int(radio * np.sin(angulo))
        puntos.append([x, y])

    puntos = np.array(puntos, dtype=np.int32)
    cv2.fillPoly(superficie, [puntos], color)
    cv2.polylines(superficie, [puntos], True, (255, 255, 255), 2)


def modo_figuras(cuadro, centro):
    """Dibuja figuras geométricas controladas por el landmark"""
    global tamaño_figura, rotacion_figura

    dx, dy, magnitud = calcular_movimiento(centro)

    # Ajustar tamaño con movimiento vertical
    if magnitud > 2:
        cambio_tamaño = int(dy * 0.3)
        tamaño_figura = tamaño_figura + cambio_tamaño
        if tamaño_figura < 20:
            tamaño_figura = 20
        if tamaño_figura > 150:
            tamaño_figura = 150

    # Ajustar rotación con movimiento horizontal
    if magnitud > 2:
        rotacion_figura = rotacion_figura + dx * 0.5
        rotacion_figura = rotacion_figura % 360

    # Color que cambia según tamaño
    matiz = int((tamaño_figura - 20) / 130 * 180)
    color_hsv = np.uint8([[[matiz, 255, 255]]])
    color_bgr = cv2.cvtColor(color_hsv, cv2.COLOR_HSV2BGR)[0][0]
    color = (int(color_bgr[0]), int(color_bgr[1]), int(color_bgr[2]))

    # Dibujar según tipo
    if tipo_figura == "circulo":
        dibujar_circulo(lienzo, centro, tamaño_figura, color)
        dibujar_circulo(cuadro, centro, tamaño_figura, color)
    elif tipo_figura == "rectangulo":
        dibujar_rectangulo(lienzo, centro, tamaño_figura, rotacion_figura, color)
        dibujar_rectangulo(cuadro, centro, tamaño_figura, rotacion_figura, color)
    elif tipo_figura == "triangulo":
        dibujar_triangulo(lienzo, centro, tamaño_figura, rotacion_figura, color)
        dibujar_triangulo(cuadro, centro, tamaño_figura, rotacion_figura, color)
    elif tipo_figura == "estrella":
        dibujar_estrella(lienzo, centro, tamaño_figura, rotacion_figura, color)
        dibujar_estrella(cuadro, centro, tamaño_figura, rotacion_figura, color)


def dibujar_interfaz(cuadro):
    """Dibuja la información en pantalla"""
    global modo_actual, tipo_figura, tamaño_figura, rotacion_figura

    # Panel negro de fondo
    cv2.rectangle(cuadro, (10, 10), (350, 180), (0, 0, 0), -1)
    cv2.rectangle(cuadro, (10, 10), (350, 180), (255, 255, 255), 2)

    # Mostrar modo
    texto_modo = "MODO: " + ("TRAZO LIBRE" if modo_actual == "dibujar" else "FIGURAS")
    cv2.putText(cuadro, texto_modo, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    if modo_actual == "figuras":
        nombres_figuras = {
            "circulo": "Planeta",
            "rectangulo": "Nave",
            "triangulo": "Cometa",
            "estrella": "Estrella"
        }
        cv2.putText(cuadro, f"Figura: {nombres_figuras[tipo_figura]}",
                    (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(cuadro, f"Tamano: {tamaño_figura}",
                    (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(cuadro, f"Rotacion: {int(rotacion_figura)} grados",
                    (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Instrucciones
    cv2.putText(cuadro, "Amarillo: Dibujar | Azul: Cambiar modo",
                (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    # Controles abajo
    cv2.putText(cuadro, "Teclas: C=Limpiar | 1-4=Figuras | Q=Salir",
                (10, 710), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


# Programa principal
print("=== Pizarra Virtual Cosmica ===")
print("Controles:")
print("- Objeto AMARILLO: Para dibujar")
print("- Objeto AZUL: Cambia de modo")
print("- Tecla 'c': Limpiar todo")
print("- Teclas '1-4': Cambiar figura")
print("- Tecla 'q': Salir")
print("\nEn modo figuras:")
print("- Mueve arriba/abajo: Cambia tamano")
print("- Mueve izquierda/derecha: Cambia rotacion")

while True:
    ret, cuadro = captura.read()
    if not ret:
        print("Error al capturar video")
        break

    # Voltear imagen
    cuadro = cv2.flip(cuadro, 1)

    # Detectar colores
    centro_amarillo = detectar_color_amarillo(cuadro)
    centro_azul = detectar_color_azul(cuadro)

    # Cambiar modo si detecta azul
    if centro_azul is not None:
        if modo_actual == "dibujar":
            modo_actual = "figuras"
        else:
            modo_actual = "dibujar"
        puntos_trazo.clear()
        cv2.waitKey(500)  # Esperar para no cambiar muchas veces

    # Si detecta amarillo, dibujar
    if centro_amarillo is not None:
        # Marcar el landmark
        cv2.circle(cuadro, centro_amarillo, 15, (0, 255, 255), 3)
        cv2.circle(cuadro, centro_amarillo, 5, (0, 255, 255), -1)

        # Ejecutar según modo
        if modo_actual == "dibujar":
            dibujar_trazo_libre(cuadro, centro_amarillo)
        else:
            modo_figuras(cuadro, centro_amarillo)

    # Combinar lienzo con cuadro
    imagen_final = cv2.addWeighted(cuadro, 0.7, lienzo, 0.3, 0)

    # Dibujar interfaz
    dibujar_interfaz(imagen_final)

    # Mostrar
    cv2.imshow('Pizarra Virtual Cosmica', imagen_final)

    # Manejar teclas
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('q'):
        break
    elif tecla == ord('c'):
        lienzo = np.zeros((720, 1280, 3), dtype=np.uint8)
        puntos_trazo.clear()
    elif tecla == ord('1'):
        tipo_figura = "circulo"
    elif tecla == ord('2'):
        tipo_figura = "rectangulo"
    elif tecla == ord('3'):
        tipo_figura = "triangulo"
    elif tecla == ord('4'):
        tipo_figura = "estrella"

# Limpiar
captura.release()
cv2.destroyAllWindows()
print("Programa terminado")