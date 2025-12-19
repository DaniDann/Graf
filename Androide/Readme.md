# Centroide en tiempo real 

## Explicación
```python
cap = cv2.VideoCapture(0)
````
Inicializar la cámara
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
```
- Convertir a escala de grises
- Aplicar desenfoque para reducir ruido

```python 
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
```
- Umbralización adaptiva para mejor detección

```python
   contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
- para encontrar el contorno de las cosas

``` Python 
    resultado = frame.copy()
     for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area > 500:  
            M = cv2.moments(contorno)
```
- Creamos una copia de los frames
- Filtramos contornos
- reducimos el area 
- Calculamos momentos 

```python 
if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
```
- Calcular centroide

```python 
 cv2.drawContours(resultado, [contorno], -1, (0, 0, 255), 2)

 cv2.circle(resultado, (cx, cy), 8, (255, 0, 0), -1)
cv2.circle(resultado, (cx, cy), 3, (255, 255, 255), -1)

cv2.putText(resultado,f"({cx},{cy})",(cx - 50, cy - 20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255),1,

cv2.putText(resultado,f"Area: {int(area)}",(cx - 50, cy + 30),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0, 255, 255),1,

 ````
- Dibujamos el contorno de color rojo
- Dibujamos el centroide
- Mostramos sus coodenadas
- El area
