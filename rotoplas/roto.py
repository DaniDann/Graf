import math
import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('Imagenes/Arbolito.jpeg', 0)

# Obtener el tamaño de la imagen
x, y = img.shape

# Crear una imagen vacía más grande (canvas)
rotated_img = np.zeros((x * 3, y * 3), dtype=np.uint8)

# Calcular el centro de la imagen original
cx, cy = x // 2, y // 2

# Definir angulos de rotación
angle1 = 30
angle2 = 60

theta1 = math.radians(angle1)
theta2 = math.radians(angle2)

# Rotar y duplicar la imagen
for i in range(x):
    for j in range(y):

        # Primera rotacion
        new_x1 = int((j - cx) * math.cos(theta1) - (i - cy) * math.sin(theta1) + cx + y)
        new_y1 = int((j - cx) * math.sin(theta1) + (i - cy) * math.cos(theta1) + cy)

        # Segunda rotacion
        new_x2 = int((j - cx) * math.cos(theta2) - (i - cy) * math.sin(theta2) + cx + y)
        new_y2 = int((j - cx) * math.sin(theta2) + (i - cy) * math.cos(theta2) + cy + x)



        # Dibujar pixeles si estan dentro del canvas
        if 0 <= new_x1 < y * 3 and 0 <= new_y1 < x * 3:
            rotated_img[new_y1, new_x1] = img[i, j]

        if 0 <= new_x2 < y * 3 and 0 <= new_y2 < x * 3:
            rotated_img[new_y2, new_x2] = img[i, j]


# Mostrar resultados
cv.imshow('Imagen Original', img)
cv.imshow('Rotaciones Manuales Multiples', rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()