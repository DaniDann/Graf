import cv2
import numpy as np

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Crear un lienzo para dibujar
canvas = None
points = []  # Lista para almacenar puntos del trazado

# Rangos de colores en HSV para diferentes colores
colores_hsv = {
    "rojo1": ([0, 50, 50], [10, 255, 255]),  # Rojo (parte 1)
    "rojo2": ([170, 50, 50], [180, 255, 255]),  # Rojo (parte 2)
    "azul": ([100, 50, 50], [130, 255, 255]),  # Azul
    "verde": ([40, 50, 50], [80, 255, 255]),  # Verde
    "amarillo": ([20, 50, 50], [40, 255, 255]),  # Amarillo
}

# Colores BGR para dibujar
colores_bgr = {
    "rojo1": (0, 0, 255),
    "rojo2": (0, 0, 255),
    "azul": (255, 0, 0),
    "verde": (0, 255, 0),
    "amarillo": (0, 255, 255),
}


def detectar_color(frame, hsv):
    """Detecta el color y devuelve la posición del centroide"""
    for nombre_color, (lower, upper) in colores_hsv.items():
        # Convertir a numpy array
        lower = np.array(lower)
        upper = np.array(upper)

        # Crear máscara para el color
        mask = cv2.inRange(hsv, lower, upper)

        # Aplicar operaciones morfológicas para limpiar la máscara
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Encontrar contornos
        contornos, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if contornos:
            # Encontrar el contorno más grande
            contorno_max = max(contornos, key=cv2.contourArea)
            area = cv2.contourArea(contorno_max)

            # Filtrar por área mínima
            if area > 300:
                # Calcular centroide
                M = cv2.moments(contorno_max)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Dibujar contorno del objeto detectado
                    cv2.drawContours(
                        frame, [contorno_max], -1, colores_bgr[nombre_color], 2
                    )
                    cv2.circle(frame, (cx, cy), 10, colores_bgr[nombre_color], -1)

                    # Agregar texto con el color detectado
                    cv2.putText(
                        frame,
                        f"{nombre_color.upper()}",
                        (cx - 30, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        colores_bgr[nombre_color],
                        2,
                    )

                    return (cx, cy), colores_bgr[nombre_color], nombre_color

    return None, None, None


def dibujar_trazo(canvas, points, color):
    """Dibuja líneas conectando los puntos"""
    if len(points) > 1:
        for i in range(1, len(points)):
            cv2.line(canvas, points[i - 1], points[i], color, 5)


# Crear lienzo inicial
ret, frame = cap.read()
if ret:
    canvas = np.zeros_like(frame)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar video")
        break

    # Voltear horizontalmente para efecto espejo
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detectar color y posición
    posicion, color_bgr, nombre_color = detectar_color(frame, hsv)

    if posicion is not None:
        # Agregar punto a la lista
        points.append(posicion)

        # Mantener solo los últimos 50 puntos para evitar acumulación excesiva
        if len(points) > 50:
            points.pop(0)

        # Dibujar el trazo en el lienzo
        if len(points) > 1:
            cv2.line(canvas, points[-2], points[-1], color_bgr, 8)
    else:
        # Si no se detecta color, limpiar la lista de puntos
        points = []

    # Combinar el frame original con el lienzo de dibujo
    resultado = cv2.addWeighted(frame, 0.7, canvas, 0.8, 0)

    # Agregar instrucciones en pantalla
    cv2.putText(
        resultado,
        "Presiona 'c' para limpiar",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        resultado,
        "Presiona 'q' para salir",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    # Mostrar las ventanas
    cv2.imshow("Varita Magica", resultado)
    cv2.imshow("Lienzo", canvas)

    # Controles de teclado
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("c"):
        # Limpiar el lienzo
        canvas = np.zeros_like(frame)
        points = []
        print("Lienzo limpiado")

# Limpiar recursos
cap.release()
cv2.destroyAllWindows()