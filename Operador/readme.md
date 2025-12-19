# Operador puntual 

Este código aplica un umbralizado binario  a una imagen en escala de grises.

```python 
img = cv.imread("Imagenes/Arbolito.jpeg", 0)
```
Lee la imagen en escala de grises (el 0 indica modo grayscale). Los píxeles tienen valores entre 0 (negro) y 255 (blanco).

```python 
img = cv.imread("Imagenes/Arbolito.jpeg", 0)
```
Muestra la imagen original en una ventana llamada 'salida'.

Obtención de dimensiones
```python
x,y=img.shape
```
Obtiene el alto (x) y ancho (y) de la imagen en píxeles.
Proceso de umbralizado

```python
for i in range(x):
    for j in range(y):
        if(img[i,j]>150):
            img[i,j]=255
        else:
            img[i,j]=0
```
Este doble bucle recorre cada píxel de la imagen y aplica una regla simple:

Si el valor del píxel es mayor a 150 → lo convierte a 255 (blanco)
Si es menor o igual a 150 → lo convierte a 0 (negro).
Esto crea una imagen binaria con solo dos colores.

Resultado
```pyhton
pythoncv.imshow('negativo', img)
```
Muestra la imagen umbralizada (aunque el nombre 'negativo' es engañoso, ya que no es un negativo sino una binarización).
## Codigo completo
```pyhton
import cv2 as cv

img = cv.imread("Imagenes/Arbolito.jpeg", 0)
cv.imshow('salida', img)
x,y=img.shape
for i in range(x):
        for j in range(y):
                if(img[i,j]>150):
                        img[i,j]=255
                else:
                        img[i,j]=0


cv.imshow('negativo', img)
print( img.shape, x , y)
cv.waitKey(0)
cv.destroyAllWindows()

```
---
# Canales

```pyhton
img = cv.imread("Imagenes/Arbolito.jpeg", 1)
```
Carga la imagen 'arbolito.jpeg' en color (1 para color, 0 para escala de grises).

```python
img2 = np.zeros((img.shape[:2]), dtype=np.uint8)
```
 Crea una imagen vacía (llena de ceros, que representa color negro) con el mismo tamaño que la imagen original.
La imagen vacía tiene un solo canal (escala de grises), por lo que se usa `img.shape[:2]` para obtener las dimensiones de la imagen (alto, ancho).

```python
print(img.shape[:2])
```
Imprime las dimensiones de la imagen en la terminal (alto, ancho).

```python
r, g, b = cv.split(img)
```
Separa los canales rojo (r), verde (g) y azul (b) de la imagen utilizando la función `cv.split()`.

```python
r2 = cv.merge([img2, img2, r])
g2 = cv.merge([img2, g, img2])
b2 = cv.merge([b, img2, img2])
img3 = cv.merge([b, r, g])
```
Recombina los canales, pero los reorganiza como rojo, azul y verde (RBG en lugar de RGB).
```python
cv.imshow("ejemplo", img)
cv.imshow("r2", r2)
cv.imshow("g2", g2)
cv.imshow("b2", b2)
```
 Muestra la imagen original en una ventana llamada 'ejemplo'.
```python
cv.imshow("img3", img3)
```
Muestra la imagen con los canales reorganizados (RBG en lugar de RGB).
```python
cv.imshow("img3", img3)
```
Espera indefinidamente a que el usuario presione una tecla.
```python
cv.waitKey(0)
````
Cierra todas las ventanas abiertas por OpenCV.
```python
cv.destroyAllWindows()
```

# Video y canales 

Este código captura video de tu webcam y manipula los canales de color. Te explico cada parte:
Captura de video
```python
cap = cv.VideoCapture(0)  # Abre la cámara (0 = cámara predeterminada)
```
Bucle principal
```python
while True:
    ret, img = cap.read()  # Lee un frame de la cámara
```
*ret:* booleano que indica si se leyó correctamente

*img:* imagen capturada en formato BGR (Blue, Green, Red)

Separación de canales
```python
r, g, b = cv.split(img)  # Separa la imagen en 3 canales
```
Divide la imagen en tres matrices separadas, cada una conteniendo la intensidad de un color (azul, verde, rojo).

```python
img3 = cv.merge([g, b, r])  # Mezcla los canales en OTRO orden
```
Aquí está la magia

#### ¿Por qué cambian los colores al reordenar RGB?
OpenCV usa el formato BGR (no RGB como otros sistemas). Cuando reordenas los canales, estás asignando cada color a una posición diferente:
Ejemplo visual:
Original (BGR en OpenCV):

Posición 0 (Blue): canal azul

Posición 1 (Green): canal verde

Posición 2 (Red): canal rojo

Tu código hace [g, b, r]:

Posición 0 (Blue): pones verde 

Posición 1 (Green): pones azul 

Posición 2 (Red): pones rojo 

Entonces:

Lo que debería ser azul → se vuelve verde

Lo que debería ser verde → se vuelve azul
Lo rojo se mantiene rojo

Ejemplo práctico:
Si tu camiseta es azul cielo :

Canal azul = alta intensidad
Canal verde = media intensidad
Canal rojo = baja intensidad

Al reordenar a [g, b, r], OpenCV interpreta:

Verde (posición Blue) = media → parece cian 
La camiseta cambia de color completamente
