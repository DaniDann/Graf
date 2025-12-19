import cv2 as cv
import numpy as np

# Crear el canvas
img = np.ones((600, 1000, 3), np.uint8) * 255  # Fondo blanco

# CUERPO DEL CARRO
# Base del carro
cv.rectangle(img, (200, 350), (800, 450), (255, 0, 0), -1)

# Parte superior
cv.rectangle(img, (350, 250), (650, 350), (255, 0, 0), -1)


# VENTANAS
cv.rectangle(img, (370, 270), (460, 340), (200, 200, 200), -1)
cv.rectangle(img, (490, 270), (630, 340), (200, 200, 200), -1)

# RUEDAS
# Rueda izquierda
cv.circle(img, (350, 450), 50, (0, 0, 0), -1)
cv.circle(img, (350, 450), 25, (150, 150, 150), -1)

# Rueda derecha
cv.circle(img, (650, 450), 50, (0, 0, 0), -1)
cv.circle(img, (650, 450), 25, (150, 150, 150), -1)


# FAROS
cv.circle(img, (800, 400), 15, (0, 255, 255), -1)
cv.circle(img, (200, 400), 15, (0, 255, 255), -1)

cv.imshow("Carrito con primitivas", img)
cv.waitKey(0)
cv.destroyAllWindows()