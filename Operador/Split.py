import cv2 as cv  # Importa OpenCV, que es útil para procesamiento de imágenes.
import numpy as np  # Importa NumPy, que es útil para trabajar con matrices y operaciones numéricas.

img = cv.imread("Imagenes/Arbolito.jpeg", 1)

# Crea una imagen vacía (llena de ceros, que representa color negro) con el mismo tamaño que la imagen original.
# La imagen vacía tiene un solo canal (escala de grises), por lo que se usa `img.shape[:2]` para obtener las dimensiones de la imagen (alto, ancho).
img2 = np.zeros((img.shape[:2]), dtype=np.uint8)

# Imprime las dimensiones de la imagen en la terminal (alto, ancho).
print(img.shape[:2])

# Separa los canales rojo (r), verde (g) y azul (b) de la imagen utilizando la función `cv.split()`.
r, g, b = cv.split(img)

# Recombina los canales, pero los reorganiza como rojo, azul y verde (RBG en lugar de RGB).
r2 = cv.merge([img2, img2, r])
g2 = cv.merge([img2, g, img2])
b2 = cv.merge([b, img2, img2])
img3 = cv.merge([b, r, g])
# Crea una imagen que contiene solo el canal rojo, llenando los otros dos canales (verde y azul) con ceros (negro).
# r = cv.merge([r, img2, img2])

# Crea una imagen que contiene solo el canal verde, llenando los otros dos canales (rojo y azul) con ceros.
# g = cv.merge([img2, g, img2])

# Crea una imagen que contiene solo el canal azul, llenando los otros dos canales (rojo y verde) con ceros.#
# b = cv.merge([img2, img2, b])

# Muestra la imagen original en una ventana llamada 'ejemplo'.
cv.imshow("ejemplo", img)
cv.imshow("r2", r2)
cv.imshow("g2", g2)
cv.imshow("b2", b2)

# Muestra la imagen que contiene solo el canal rojo.
# cv.imshow('r', r)
# cv.imshow('r2', r2)


# Muestra la imagen que contiene solo el canal verde.
# cv.imshow('g', g)
# cv.imshow('g2', g2)

# Muestra la imagen que contiene solo el canal azul.
# cv.imshow('b', b)
# cv.imshow('b2', b2)

# Muestra la imagen con los canales reorganizados (RBG en lugar de RGB).
cv.imshow("img3", img3)

# Espera indefinidamente a que el usuario presione una tecla.
cv.waitKey(0)

# Cierra todas las ventanas abiertas por OpenCV.
cv.destroyAllWindows()