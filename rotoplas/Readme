# Rotación Manual de Imagen 

Este proyecto implementa una **rotación manual de imágenes en escala de grises** utilizando únicamente operaciones matemáticas básicas, bucles y acceso directo a píxeles. No se utilizan funciones avanzadas de OpenCV como `warpAffine`, cumpliendo con un enfoque **didáctico y académico**.

El resultado es un efecto visual tipo **caleidoscopio**, donde la imagen original aparece **duplicada y rotada múltiples veces** en un mismo canvas.

---

## Objetivo

* Aplicar transformaciones geométricas manuales
* Comprender la rotación de puntos en el plano
* Manipular imágenes a nivel de píxel
* Reforzar el uso de coordenadas cartesianas

---

## Herramientas

* **Python 3**
* **OpenCV (cv2)**
* **NumPy**
* **math**

---

## Formnulas y detalles matematicos

La rotación de un punto ((x, y)) alrededor de un centro ((c_x, c_y)) se realiza mediante:

```
x' = (x - c_x) cos(θ) - (y - c_y) sin(θ) + c_x
y' = (x - c_x) sin(θ) + (y - c_y) cos(θ) + c_y
```

En este programa:

* Se usan **dos ángulos distintos**
* Se dibujan varias versiones de la misma imagen
* Se aplica un desplazamiento manual para evitar sobreposición

---

## Descripcion rapida del programa

1. Se carga una imagen en escala de grises
2. Se obtiene su tamaño
3. Se crea un canvas más grande para evitar recortes
4. Se calcula el centro de la imagen
5. Se recorren todos los píxeles
6. Cada píxel se rota usando dos ángulos diferentes
7. Las imágenes rotadas se colocan en distintas posiciones

---

## 💻 Código principal

```python
import math
import cv2 as cv
import numpy as np

img = cv.imread('Imagenes/Arbolito.jpeg', 0)

x, y = img.shape
rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)

cx, cy = x // 2, y // 2

angle1 = 30
angle2 = 60
theta1 = math.radians(angle1)
theta2 = math.radians(angle2)

for i in range(x):
    for j in range(y):

        new_x1 = int((j - cx) * math.cos(theta1) - (i - cy) * math.sin(theta1) + cx + 200)
        new_y1 = int((j - cx) * math.sin(theta1) + (i - cy) * math.cos(theta1) + cy + 200)

        new_x2 = int((j - cx) * math.cos(theta2) - (i - cy) * math.sin(theta2) + cx + 600)
        new_y2 = int((j - cx) * math.sin(theta2) + (i - cy) * math.cos(theta2) + cy + 200)

        new_x3 = j + 200
        new_y3 = i + 600

        if 0 <= new_x1 < y*2 and 0 <= new_y1 < x*2:
            rotated_img[new_y1, new_x1] = img[i, j]

        if 0 <= new_x2 < y*2 and 0 <= new_y2 < x*2:
            rotated_img[new_y2, new_x2] = img[i, j]

        if 0 <= new_x3 < y*2 and 0 <= new_y3 < x*2:
            rotated_img[new_y3, new_x3] = img[i, j]

cv.imshow('Imagen Original', img)
cv.imshow('Modo LOCO - Multiples Rotaciones', rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()
```

---

## Resultados

* Imagen original sin modificaciones
* Imagen resultante con:

  * Dos rotaciones distintas
  * Una copia sin rotación
  * Efecto visual tipo caleidoscopio
---

