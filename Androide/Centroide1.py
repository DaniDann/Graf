import cv2 as cv
import numpy as np

# =============================================================================
# PASO 1: CREAR EL LIENZO Y LA FIGURA
# =============================================================================

# Crear una imagen en negro de 500x500 píxeles
# np.uint8 significa que cada píxel puede tener valores de 0 a 255
img = np.zeros((500, 500), np.uint8)

# Dibujar un círculo blanco en el centro
# Parámetros: (imagen, centro, radio, color, grosor)
# -1 significa que el círculo estará relleno
cv.circle(img, (250, 250), 50, (255), -1)  # Círculo más grande para mejor visualización

# También podemos agregar otras figuras para probar
cv.rectangle(img, (100, 100), (150, 200), (255), -1)  # Rectángulo
cv.ellipse(img, (350, 350), (40, 60), 0, 0, 360, (255), -1)  # Elipse

cv.imshow("Figura Original", img)

# =============================================================================
# PASO 2: ANÁLISIS DE TU MÉTODO ORIGINAL (INCORRECTO)
# =============================================================================

print("=== ANÁLISIS DE TU MÉTODO ORIGINAL ===")
print("Tu idea era encontrar coordenadas extremas y calcular el centro...")
print("Pero esto solo funciona para figuras perfectamente simétricas.\n")

# Tu método original (modificado para que funcione)
# Encontrar el primer píxel blanco recorriendo por filas
primera_coord_x, primera_coord_y = None, None
for i in range(500):  # filas (coordenada y)
    for j in range(500):  # columnas (coordenada x)
        if img[i, j] == 255:
            primera_coord_y, primera_coord_x = i, j  # Nota: i es y, j es x
            break
    if primera_coord_x is not None:
        break

print(f"Primera coordenada encontrada (x, y): ({primera_coord_x}, {primera_coord_y})")

# =============================================================================
# PASO 3: MÉTODO CORRECTO - CALCULAR CENTROIDE REAL
# =============================================================================

print("\n=== MÉTODO CORRECTO ===")

# Encontrar TODAS las coordenadas que pertenecen a la figura
coordenadas_figura = []
for i in range(500):  # filas (y)
    for j in range(500):  # columnas (x)
        if img[i, j] == 255:  # Si el píxel es blanco (parte de la figura)
            coordenadas_figura.append((j, i))  # Guardamos como (x, y)

print(f"Total de píxeles que forman las figuras: {len(coordenadas_figura)}")

# Calcular el centroide como el promedio de todas las coordenadas
if coordenadas_figura:
    suma_x = sum(coord[0] for coord in coordenadas_figura)
    suma_y = sum(coord[1] for coord in coordenadas_figura)

    centroide_x = suma_x / len(coordenadas_figura)
    centroide_y = suma_y / len(coordenadas_figura)

    print(f"Centroide calculado (x, y): ({centroide_x:.2f}, {centroide_y:.2f})")
else:
    print("No se encontraron píxeles blancos")

# =============================================================================
# PASO 4: MÉTODO ALTERNATIVO USANDO MOMENTOS (MÁS EFICIENTE)
# =============================================================================

print("\n=== MÉTODO USANDO MOMENTOS (OpenCV) ===")

# Encontrar contornos de las figuras
contornos, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Crear imagen para mostrar resultados
img_resultado = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

for i, contorno in enumerate(contornos):
    # Calcular momentos del contorno
    M = cv.moments(contorno)

    # Calcular centroide usando momentos
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        print(f"Figura {i + 1} - Centroide con momentos (x, y): ({cx}, {cy})")

        # Dibujar el centroide en la imagen
        cv.circle(img_resultado, (cx, cy), 8, (0, 0, 255), -1)  # Punto rojo
        cv.circle(
            img_resultado, (cx, cy), 3, (255, 255, 255), -1
        )  # Punto blanco interior

        # Agregar texto con las coordenadas
        cv.putText(
            img_resultado,
            f"({cx},{cy})",
            (cx - 30, cy - 20),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )

# =============================================================================
# PASO 5: COMPARACIÓN Y EXPLICACIÓN MATEMÁTICA
# =============================================================================

print("\n=== EXPLICACIÓN MATEMÁTICA ===")
print("El centroide se define como:")
print("Cx = (suma de todas las coordenadas x) / (número total de puntos)")
print("Cy = (suma de todas las coordenadas y) / (número total de puntos)")
print()
print("Tu método original solo consideraba extremos, pero:")
print("- Para figuras irregulares, los extremos no representan el centro de masa")
print("- El centroide es el 'centro de gravedad' de todos los píxeles")
print("- Necesitas promediar TODAS las coordenadas, no solo algunas")

# =============================================================================
# PASO 6: DEMOSTRACIÓN CON FIGURA IRREGULAR
# =============================================================================

print("\n=== PRUEBA CON FIGURA IRREGULAR ===")

# Crear una figura irregular para demostrar la diferencia
img_irregular = np.zeros((500, 500), np.uint8)

# Triángulo irregular usando puntos
puntos = np.array([[100, 100], [300, 150], [200, 400]], np.int32)
cv.fillPoly(img_irregular, [puntos], 255)

# Calcular centroide de la figura irregular
contornos_irreg, _ = cv.findContours(
    img_irregular, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
)
img_irreg_resultado = cv.cvtColor(img_irregular, cv.COLOR_GRAY2BGR)

for contorno in contornos_irreg:
    M = cv.moments(contorno)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        print(f"Centroide del triángulo irregular: ({cx}, {cy})")

        # Marcar el centroide
        cv.circle(img_irreg_resultado, (cx, cy), 8, (0, 0, 255), -1)

        # Marcar los vértices del triángulo para comparar
        for punto in puntos:
            cv.circle(img_irreg_resultado, tuple(punto), 5, (0, 255, 0), -1)

# Mostrar todas las imágenes
cv.imshow("Figuras con Centroides", img_resultado)
cv.imshow("Triangulo Irregular", img_irreg_resultado)

print("\n=== CONCLUSIÓN ===")
print("Tu idea inicial era un buen punto de partida para figuras simétricas,")
print("pero el método correcto requiere considerar TODOS los píxeles de la figura.")
print("Los momentos de OpenCV son la forma más eficiente de calcularlo.")

cv.waitKey(0)
cv.destroyAllWindows()