# Imagen

```python
import cv2 as cv
image = cv.imread('Imagenes/Arbolito.jpeg',0)
cv.imshow('First Image', image)
cv.waitKey()
cv.destroyAllWindows
```

#### Explicación


```python
import cv2 as cv
```

Importa la librería OpenCV, que permite trabajar con imágenes, videos y procesamiento digital.
Se usa as cv para abreviar su nombre.

```pyhon
image = cv.imread('Imagenes/Arbolito.jpeg',0)
```
Carga la imagen Arbolito.jpeg desde la carpeta Imagenes.

- *cv.imread()* → función para leer imágenes.

- *Primer parámetro*: ruta de la imagen.

- *Segundo parámetro*: modo de lectura.

- *0* → carga la imagen en escala de grises.


#### ¿Qué significa el parametro 0?

|Valor|Modo|Resultado|
|-|-|-|
|`0`|**Grayscale**| Carga la imagen en blanco y negro|
|`1`|**Color (BGR)**|Carga la imagen en color (por defecto)|
|`-1`| **Unchanged**| Carga la imagen con su alpha si lo tiene|

# Evidencia 

![Arbolito](primerin.png)
