# Bolita con obstaculo (Ping pong)

Este proyecto implementa una simulación tipo **Pong** usando **Python**, **OpenCV** y **NumPy**, donde una pelota rebota dentro de un canvas y un **obstáculo central inteligente** se mueve dinámicamente para bloquear su paso.

Es un ejemplo práctico de:

* Gráficos por primitivas
* Movimiento 2D
* Detección de colisiones
* Distancia euclidiana
* Animación en tiempo real

---

## Vista general

* Canvas: **500 × 500 píxeles**
* Pelota: círculo rojo que rebota
* Obstáculo: barra negra que reacciona al movimiento de la pelota

---

## Lógica principal

### 1. Canvas

Se crea una imagen blanca de 500×500 con 3 canales (RGB):

```python
img = np.ones((500, 500, 3), np.uint8) * 255
```

---

### 2. Pelota

La pelota se define por:

* Posición `(pos_x, pos_y)`
* Velocidad `(vel_x, vel_y)`
* Radio

Se actualiza en cada iteración del bucle principal.

---

### 3. Obstáculo inteligente

El obstáculo es un rectángulo vertical ubicado al centro del canvas.

Se mueve **solo cuando la pelota se acerca**, usando la **distancia euclidiana**:

```python
distancia = sqrt((x_pelota - x_obs)^2 + (y_pelota - y_obs)^2)
```

Si la distancia es menor a un umbral, el obstáculo intenta alinearse con la pelota para bloquearla.

---

### 4. Colisiones

#### Rebote con bordes

* La pelota rebota al tocar los límites del canvas.

#### Rebote con obstáculo

* Si la pelota impacta el obstáculo, se invierte la velocidad horizontal.

