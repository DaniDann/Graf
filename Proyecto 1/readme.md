# Pizarra Virtual  - Proyecto 1

## Descripción del Proyecto

Este es un programa de pizarra virtual que usa la cámara para detectar objetos de colores y dibujar en la pantalla. El proyecto está basado en seguimiento por color (Color Tracking) en el espacio HSV y usa OpenCV para dibujar figuras primitivas.

La idea es que uses objetos de colores (como papeles, marcadores o cualquier cosa de color amarillo y azul) para controlar el dibujo en la pantalla. Es como pintar en el aire pero con tu cámara.

## ¿Qué hace el programa?

El programa tiene 2 modos principales:

### 1. Modo Trazo Libre (Dibujo de Nebulosas)
- Detecta un objeto AMARILLO y lo usa como "pincel"
- Dibuja líneas continuas con efecto de nebulosa espacial
- El trazo tiene colores degradados y grosor variable
- Es como pintar en el aire dejando un rastro espacial

### 2. Modo Figuras Geométricas
- Dibuja 4 tipos de figuras espaciales:
  - **Planeta** (círculo con anillos)
  - **Nave Espacial** (rectángulo con bordes)
  - **Cometa** (triángulo)
  - **Estrella** (estrella de 5 puntas)

- **Control del Tamaño**: Mueve el objeto amarillo arriba o abajo para hacer la figura más grande o pequeña
- **Control de Rotación**: Mueve el objeto amarillo a los lados para rotar la figura
- El color de las figuras cambia según el tamaño

## ¿Cómo funciona técnicamente?

### Seguimiento por Color (Landmark)
El programa busca objetos de colores específicos en cada cuadro del video:

1. **Conversión a HSV**: Convierte la imagen de BGR a HSV porque es más fácil detectar colores
2. **Máscaras de Color**: Crea máscaras para filtrar solo los colores que nos interesan
3. **Procesamiento Morfológico**: Limpia la imagen con erosión y dilatación para quitar ruido
4. **Detección de Contornos**: Encuentra el contorno más grande del color
5. **Cálculo del Centroide**: Calcula el centro del objeto usando momentos de imagen

El centroide del objeto amarillo es nuestro **Landmark** - el punto de control principal.

### Dibujo de Primitivas
Usa funciones de OpenCV para dibujar:

- `cv2.line()` - Para el trazo continuo entre puntos
- `cv2.circle()` - Para los planetas
- `cv2.fillPoly()` - Para rectángulos, triángulos y estrellas
- `cv2.polylines()` - Para los bordes de las figuras

### Control de Transformaciones

**Vector de Movimiento**: 
```
dx = posicion_actual_x - posicion_anterior_x
dy = posicion_actual_y - posicion_anterior_y
magnitud = sqrt(dx² + dy²)
```

**Escalamiento**: 
- Se suma/resta el cambio vertical (dy) al tamaño actual
- Limitado entre 20 y 150 píxeles

**Rotación**: 
- Se suma el cambio horizontal (dx) a la rotación actual
- La rotación se aplica usando matrices de rotación:
```
x_nuevo = x * cos(ángulo) - y * sin(ángulo)
y_nuevo = x * sin(ángulo) + y * cos(ángulo)
```

## Requisitos del Sistema

### Librerías necesarias:
```bash
pip install opencv-python
pip install numpy
```

O instalar todo junto:
```bash
pip install opencv-python numpy
```

### Hardware:
- Cámara web (cualquier cámara USB o integrada)
- Objetos de color amarillo y azul

## Cómo Usar el Programa

### 1. Preparar los objetos de colores
Necesitas:
- **Un objeto AMARILLO** (papel, marcador, post-it, juguete, etc.)
- **Un objeto AZUL** (para cambiar de modo)

Los objetos deben ser de colores brillantes y sólidos para que la cámara los detecte bien.

### 2. Ejecutar el programa
```bash
python pizarra_cosmica.py
```

### 3. Controles

**Objetos de Color:**
- 🟡 **Objeto Amarillo** = Landmark para dibujar/controlar figuras
- 🔵 **Objeto Azul** = Cambiar entre modo trazo libre y modo figuras

**Teclado:**
- `C` = Limpiar todo el canvas
- `1` = Cambiar a figura Planeta (círculo)
- `2` = Cambiar a figura Nave (rectángulo)
- `3` = Cambiar a figura Cometa (triángulo)
- `4` = Cambiar a figura Estrella
- `Q` = Salir del programa

### 4. Consejos para mejor detección
- Usar objetos de colores brillantes y sólidos
- Tener buena iluminación (luz natural o lámparas)
- Evitar fondos del mismo color que los objetos
- No usar objetos muy pequeños
- Si no detecta bien, puedes ajustar los rangos de color en el código

## Estructura del Código

```
pizarra_cosmica.py
├── Variables globales (captura, lienzo, rangos de color, etc.)
├── detectar_color_amarillo() - Detecta el landmark amarillo
├── detectar_color_azul() - Detecta el objeto de cambio de modo
├── dibujar_trazo_libre() - Modo de dibujo continuo
├── calcular_movimiento() - Calcula vector de desplazamiento
├── dibujar_circulo() - Dibuja planetas
├── dibujar_rectangulo() - Dibuja naves espaciales
├── dibujar_triangulo() - Dibuja cometas
├── dibujar_estrella() - Dibuja estrellas
├── modo_figuras() - Controla el modo de figuras geométricas
├── dibujar_interfaz() - Dibuja la información en pantalla
└── Loop principal - Captura video y coordina todo
```

## Posibles Problemas y Soluciones

### ❌ "No detecta mi objeto amarillo"
**Solución**: Ajusta los rangos de color HSV en el código:
```python
rango_amarillo_bajo = np.array([20, 100, 100])  # Puedes cambiar estos valores
rango_amarillo_alto = np.array([30, 255, 255])
```

### ❌ "La cámara no funciona"
**Solución**: Cambia el índice de la cámara:
```python
captura = cv2.VideoCapture(0)  # Prueba con 1, 2, etc.
```

### ❌ "El programa va muy lento"
**Solución**: Reduce la resolución:
```python
captura.set(3, 640)   # Ancho
captura.set(4, 480)   # Alto
```

### ❌ "Detecta muchas cosas que no son mi objeto"
**Solución**: Aumenta el área mínima:
```python
if area > 500:  # Cambia 500 a 1000 o más
```

## Ajustes Personalizables

### Cambiar colores de detección
Puedes usar diferentes colores modificando los rangos HSV:
```python
# Rojo
rango_rojo_bajo = np.array([0, 100, 100])
rango_rojo_alto = np.array([10, 255, 255])

# Verde
rango_verde_bajo = np.array([40, 100, 100])
rango_verde_alto = np.array([80, 255, 255])
```

### Cambiar tamaños y velocidades
```python
tamaño_figura = 50  # Tamaño inicial de figuras
puntos_trazo = deque(maxlen=50)  # Cantidad de puntos en el trazo
grosor = int(np.sqrt(50 / float(i + 1)) * 8)  # Grosor del trazo
```

## Cumplimiento de Requisitos

✅ **Actividad 1: Modo Trazado Libre**
- Implementa captura de video
- Usa seguimiento por color HSV con `cv2.inRange()`
- Aísla el landmark amarillo
- Dibuja líneas continuas con `cv2.line()` entre puntos consecutivos
- Simula trazo de pintura tipo nebulosa

✅ **Actividad 2: Figuras Primitivas**
- Integra 4 tipos de figuras geométricas
- Usa detección de segundo color (azul) para alternar modos
- **Traslación**: Las figuras siguen directamente al landmark
- **Escalamiento**: Movimiento vertical controla el tamaño
- **Rotación**: Movimiento horizontal controla el ángulo
- Dibuja con `cv2.circle()`, `cv2.fillPoly()`, etc.

