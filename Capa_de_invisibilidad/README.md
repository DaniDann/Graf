# Capa de harry potter con OpenCV
### Explicación

Este programa en Python, apoyado en OpenCV y NumPy, genera un efecto de “capa invisible” como el que aparece en películas de fantasía. Su funcionamiento se basa en identificar un color determinado (en este ejemplo, el verde) y sustituirlo por una imagen del fondo que se capturó previamente.

---

## librerías

```python
import cv2
import numpy as np
```

* **cv2**:captura de video, procesamiento de imágenes.
* **numpy**:  utilizada aquí para definir rangos de colores.

## Captura de video 

```python
cap = cv2.VideoCapture(0)
cv2.waitKey(3000)
```

*`cv2.VideoCapture(0)`* abre la cámara dispositivo, índice `0` se refiere a la primer camara que detecte.
*`cv2.waitKey(2000)`* espera **3 segundos** para que la cámara se estabilice antes de tomar el fondo.


## Fondo de referencia

```python
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()
```

* Se toma una imagen del fondo 
* Si la captura falla (*ret == False*), se libera la cámara y se cierra el programa.

## Bucle principal 

```python
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
```

 El programa entra en un bucle mientras la cámara esté encendida.`frame` es cada cuadro de video capturado.

## Conversión a espacio de color HSV

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

* Se convierte la imagen de BGR a HSV.
* HSV facilita la detección de colores específicos 

## Rango de color verde

```python
lower_green = np.array([80, 40, 40])
upper_green = np.array([145, 255, 255])
```

* Se define un rango de verde en HSV.
* Los valores pueden ajustarse dependiendo de la tela usada y la iluminación.

## Máscara del color verde

```python
mask = cv2.inRange(hsv, lower_green, upper_green)
```

* `cv2.inRange()` genera una máscara binaria:

  * Blanco (255): píxeles dentro del rango verde.
  * Negro (0): píxeles fuera del rango.

## Contraste de la mascara

```python
mask_inv = cv2.bitwise_not(mask)
```

* Se invierte la máscara:

  * verdes → Negro
  * No verde→ Blanco

## Regiones visibles y ocultas

```python
res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)
res2 = cv2.bitwise_and(background, background, mask=mask)
```

`res1`:  objetos que *no son verdes*.

`res2`:  áreas donde *había verde*, pero reemplazadas con el fondo.

## Combinación 

```python
final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
```

* Se realiza la combinacion de ambas imagenes (`res1` y `res2`) para crear "**invisibilidad**":

La persona aparece completa, excepto en las zonas cubiertas con verde, donde se muestra el fondo.

## Resultados

```python
cv2.imshow("Capa de Invisibilidad", final_output)
cv2.imshow('mask', mask)
```

* Ventana 1: Muestra el efecto final de invisibilidad.
* Ventana 2: Muestra la máscara binaria usada para detectar el color verde.

## Salida del programa

* Se espera la tecla *`q`* para salir del bucle.
* Se liberan los recursos (cap.release()) y se cierran todas las ventanas (cv2.destroyAllWindows()).
