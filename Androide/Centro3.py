import cv2 as cv
import numpy as np


def calcular_centroide_manual(imagen):
    """
    Función que calcula el centroide de forma manual encontrando
    TODAS las coordenadas que pertenecen a las figuras blancas

    Parámetros:
    - imagen: matriz numpy con la imagen en escala de grises

    Retorna:
    - lista de centroides encontrados, cada uno como (x, y)
    """

    # Encontrar contornos para separar cada figura individual
    # Esto nos permitirá calcular el centroide de cada figura por separado
    contornos, _ = cv.findContours(imagen, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    centroides = []

    # Procesar cada contorno (cada figura) individualmente
    for i, contorno in enumerate(contornos):
        print(f"\n--- Procesando Figura {i + 1} ---")

        # Crear una máscara para aislar solo esta figura
        mascara = np.zeros_like(imagen)
        cv.drawContours(mascara, [contorno], -1, 255, -1)

        # Encontrar TODAS las coordenadas que pertenecen a esta figura específica
        coordenadas_figura = []

        # Recorrer cada píxel de la imagen
        for fila in range(imagen.shape[0]):  # altura de la imagen
            for columna in range(imagen.shape[1]):  # ancho de la imagen
                # Si el píxel está dentro de esta figura (es blanco en la máscara)
                if mascara[fila, columna] == 255:
                    # Agregar la coordenada como (x, y)
                    # Recordar: columna = x, fila = y
                    coordenadas_figura.append((columna, fila))

        print(f"Píxeles encontrados en esta figura: {len(coordenadas_figura)}")

        # Calcular el centroide usando el método manual
        if coordenadas_figura:
            # Sumar todas las coordenadas X
            suma_x = 0
            for coord in coordenadas_figura:
                suma_x += coord[0]  # coord[0] es la coordenada X

            # Sumar todas las coordenadas Y
            suma_y = 0
            for coord in coordenadas_figura:
                suma_y += coord[1]  # coord[1] es la coordenada Y

            # Calcular el promedio (esto es el centroide)
            centroide_x = suma_x / len(coordenadas_figura)
            centroide_y = suma_y / len(coordenadas_figura)

            print(f"Suma total X: {suma_x}")
            print(f"Suma total Y: {suma_y}")
            print(f"Total de píxeles: {len(coordenadas_figura)}")
            print(f"Centroide calculado: ({centroide_x:.2f}, {centroide_y:.2f})")

            centroides.append((int(centroide_x), int(centroide_y)))

    return centroides


# =============================================================================
# CREAR DIFERENTES FIGURAS PARA PROBAR EL MÉTODO
# =============================================================================

print("=== CREANDO DIFERENTES FIGURAS GEOMÉTRICAS ===")

# Crear un lienzo grande para nuestras pruebas
canvas = np.zeros((600, 800), np.uint8)

# 1. CÍRCULO - Figura perfectamente simétrica
print("\n1. Agregando un círculo...")
cv.circle(canvas, (150, 150), 60, 255, -1)
print("   Un círculo es simétrico, su centroide debe estar exactamente en su centro")

# 2. RECTÁNGULO - Figura simétrica pero diferente forma
print("\n2. Agregando un rectángulo...")
cv.rectangle(canvas, (300, 100), (450, 200), 255, -1)
print("   Un rectángulo también es simétrico, centroide en el centro geométrico")

# 3. TRIÁNGULO - Figura asimétrica
print("\n3. Agregando un triángulo...")
puntos_triangulo = np.array([[500, 100], [650, 200], [550, 250]], np.int32)
cv.fillPoly(canvas, [puntos_triangulo], 255)
print(
    "   Un triángulo es asimétrico, el centroide no está en el centro de los vértices"
)

# 4. ELIPSE - Figura simétrica pero elongada
print("\n4. Agregando una elipse...")
cv.ellipse(canvas, (150, 350), (80, 40), 0, 0, 360, 255, -1)
print("   Una elipse es simétrica pero elongada")

# 5. FORMA IRREGULAR - La prueba más difícil
print("\n5. Agregando una forma completamente irregular...")
puntos_irregular = np.array(
    [
        [350, 300],
        [420, 280],
        [480, 320],
        [470, 380],
        [400, 400],
        [340, 370],
        [320, 340],
    ],
    np.int32,
)
cv.fillPoly(canvas, [puntos_irregular], 255)
print("   Una forma irregular donde tu método original definitivamente fallaría")

# 6. FIGURA EN L - Forma no convexa
print("\n6. Agregando una figura en forma de L...")
# Crear la L usando dos rectángulos
cv.rectangle(canvas, (550, 350), (580, 450), 255, -1)  # Parte vertical
cv.rectangle(canvas, (580, 420), (650, 450), 255, -1)  # Parte horizontal
print("   Una forma en L es no convexa, muy interesante para el cálculo del centroide")

# Mostrar la imagen original con todas las figuras
cv.imshow("Figuras Originales", canvas)

# =============================================================================
# APLICAR NUESTRO MÉTODO MANUAL A TODAS LAS FIGURAS
# =============================================================================

print("\n" + "=" * 60)
print("CALCULANDO CENTROIDES CON EL MÉTODO MANUAL")
print("=" * 60)

# Calcular centroides usando nuestro método manual
centroides = calcular_centroide_manual(canvas)

# =============================================================================
# VISUALIZAR LOS RESULTADOS
# =============================================================================

# Convertir la imagen a color para poder dibujar centroides en rojo
canvas_resultado = cv.cvtColor(canvas, cv.COLOR_GRAY2BGR)

print("\n--- RESULTADOS FINALES ---")
print(f"Se encontraron {len(centroides)} figuras")

# Dibujar cada centroide encontrado
for i, (cx, cy) in enumerate(centroides):
    # Dibujar el centroide como un punto rojo grande
    cv.circle(canvas_resultado, (cx, cy), 8, (0, 0, 255), -1)

    # Dibujar un punto blanco más pequeño en el centro para mejor visibilidad
    cv.circle(canvas_resultado, (cx, cy), 3, (255, 255, 255), -1)

    # Agregar las coordenadas como texto
    cv.putText(
        canvas_resultado,
        f"Figura {i + 1}: ({cx},{cy})",
        (cx - 50, cy - 25),
        cv.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
    )

    print(f"Figura {i + 1}: Centroide en ({cx}, {cy})")

# =============================================================================
# ANÁLISIS EDUCATIVO DE LOS RESULTADOS
# =============================================================================

print("\n--- ANÁLISIS DE LOS RESULTADOS ---")
print("Observa cómo cada tipo de figura tiene comportamientos diferentes:")
print()
print(
    "• CÍRCULO Y RECTÁNGULO: Sus centroides están exactamente en el centro geométrico"
)
print("• TRIÁNGULO: El centroide NO está en el centro de los vértices, sino desplazado")
print("• ELIPSE: Centroide en el centro, pero la forma elongada es visible")
print("• FORMA IRREGULAR: El centroide está donde se concentra más 'masa' de píxeles")
print(
    "• FIGURA EN L: Centroide en una posición que puede parecer 'extraña' pero es correcta"
)
print()
print("¿Por qué es importante entender esto?")
print("- En visión por computadora, el centroide nos ayuda a ubicar objetos")
print("- En física, representa el centro de masa")
print("- En robótica, es crucial para el agarre de objetos")



print("\n--- ¿FUNCIONARÍA TU MÉTODO ORIGINAL? ---")
print("Tu idea de usar solo extremos funcionaría bien para:")
print("• El círculo (simétrico)")
print("• El rectángulo (simétrico y alineado)")
print()
print("Pero fallaría completamente para:")
print("• El triángulo (asimétrico)")
print("• La forma irregular (muy asimétrica)")
print("• La figura en L (no convexa)")
print()
print("Por eso necesitamos considerar TODOS los píxeles, no solo los extremos.")

# Mostrar el resultado final
cv.imshow("Centroides Calculados Manualmente", canvas_resultado)

print("\n--- INSTRUCCIONES ---")
print("Observa las dos ventanas:")
print("1. 'Figuras Originales': Las figuras en blanco")
print("2. 'Centroides Calculados': Los puntos rojos son los centroides")
print("Presiona cualquier tecla para cerrar...")

cv.waitKey(0)
cv.destroyAllWindows()