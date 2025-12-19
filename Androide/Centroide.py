import cv2 as cv
import numpy as np


def calcular_centroide_global_manual(imagen):
    # Lista para almacenar TODAS las coordenadas blancas de toda la imagen
    todas_las_coordenadas = []

    print("Recorriendo cada píxel de la imagen...")

    # Recorrer cada píxel de la imagen sin distinguir figuras
    for fila in range(imagen.shape[0]):  # altura (y)
        for columna in range(imagen.shape[1]):  # ancho (x)
            # Si encontramos un píxel blanco, lo agregamos a nuestra lista
            if imagen[fila, columna] == 255:
                todas_las_coordenadas.append((columna, fila))  # (x, y)

    print(f"Total de píxeles blancos encontrados: {len(todas_las_coordenadas)}")

    # Si no hay píxeles blancos, retornar None
    if not todas_las_coordenadas:
        print("No se encontraron píxeles blancos")
        return None

    # Calcular el centroide global manualmente
    suma_x = 0
    suma_y = 0

    # Sumar todas las coordenadas X e Y
    for x, y in todas_las_coordenadas:
        suma_x += x
        suma_y += y

    # Calcular el promedio (centroide)
    centroide_x = suma_x / len(todas_las_coordenadas)
    centroide_y = suma_y / len(todas_las_coordenadas)

    print(f"Suma total de coordenadas X: {suma_x}")
    print(f"Suma total de coordenadas Y: {suma_y}")
    print(f"Centroide global: ({centroide_x:.2f}, {centroide_y:.2f})")

    return (int(centroide_x), int(centroide_y))


def separar_figuras_por_conectividad(imagen):
    """
    Método alternativo: separar figuras sin usar contornos,
    usando conectividad de píxeles (flood fill)
    """
    print("\n=== MÉTODO ALTERNATIVO: SEPARACIÓN POR CONECTIVIDAD ===")

    # Crear una copia de la imagen para trabajar
    imagen_trabajo = imagen.copy()
    figuras_separadas = []
    numero_figura = 1

    # Recorrer la imagen buscando píxeles blancos no procesados
    for fila in range(imagen.shape[0]):
        for columna in range(imagen.shape[1]):
            # Si encontramos un píxel blanco no procesado
            if imagen_trabajo[fila, columna] == 255:
                print(
                    f"\nEncontrada nueva figura {numero_figura} en posición ({columna}, {fila})"
                )

                # Usar flood fill para encontrar toda la figura conectada
                # Crear una máscara para el flood fill
                mascara = np.zeros((imagen.shape[0] + 2, imagen.shape[1] + 2), np.uint8)

                # Aplicar flood fill desde este punto
                cv.floodFill(
                    imagen_trabajo, mascara, (columna, fila), 128
                )  # Cambiar a gris

                # Encontrar todas las coordenadas de esta figura específica
                coordenadas_figura = []
                for f in range(imagen.shape[0]):
                    for c in range(imagen.shape[1]):
                        if (
                            imagen_trabajo[f, c] == 128
                        ):  # Píxeles marcados por flood fill
                            coordenadas_figura.append((c, f))  # (x, y)

                print(f"Píxeles en figura {numero_figura}: {len(coordenadas_figura)}")

                # Calcular centroide de esta figura específica
                if coordenadas_figura:
                    suma_x = sum(coord[0] for coord in coordenadas_figura)
                    suma_y = sum(coord[1] for coord in coordenadas_figura)

                    centroide_x = suma_x / len(coordenadas_figura)
                    centroide_y = suma_y / len(coordenadas_figura)

                    print(
                        f"Centroide figura {numero_figura}: ({centroide_x:.2f}, {centroide_y:.2f})"
                    )

                    figuras_separadas.append(
                        {
                            "numero": numero_figura,
                            "coordenadas": coordenadas_figura,
                            "centroide": (int(centroide_x), int(centroide_y)),
                            "area": len(coordenadas_figura),
                        }
                    )

                numero_figura += 1

    return figuras_separadas


# =============================================================================
# CREAR FIGURAS DE PRUEBA
# =============================================================================

print("=== CREANDO FIGURAS DE PRUEBA ===")

# Crear un lienzo
canvas = np.zeros((500, 600), np.uint8)

# Crear diferentes figuras para demostrar ambos métodos
print("Agregando diferentes figuras al lienzo...")

# Figura 1: Círculo en la esquina superior izquierda
cv.circle(canvas, (100, 100), 40, 255, -1)
print("• Círculo en (100, 100)")

# Figura 2: Rectángulo en el centro
cv.rectangle(canvas, (250, 150), (350, 250), 255, -1)
print("• Rectángulo centrado")

# Figura 3: Triángulo en la derecha
puntos_triangulo = np.array([[450, 80], [550, 150], [480, 180]], np.int32)
cv.fillPoly(canvas, [puntos_triangulo], 255)
print("• Triángulo a la derecha")

# Figura 4: Forma irregular abajo
puntos_irregular = np.array(
    [[150, 350], [200, 320], [280, 360], [250, 420], [180, 400]], np.int32
)
cv.fillPoly(canvas, [puntos_irregular], 255)
print("• Forma irregular en la parte inferior")

# Mostrar la imagen original
cv.imshow("Figuras Originales", canvas)

# =============================================================================
# APLICAR EL MÉTODO SIN CONTORNOS
# =============================================================================

print("\n" + "=" * 60)

# Método 1: Centroide global (todas las figuras como una masa)
centroide_global = calcular_centroide_global_manual(canvas)

# =============================================================================
# VISUALIZAR EL RESULTADO DEL MÉTODO GLOBAL
# =============================================================================

# Convertir a color para visualización
canvas_global = cv.cvtColor(canvas, cv.COLOR_GRAY2BGR)

if centroide_global:
    cx_global, cy_global = centroide_global

    # Dibujar el centroide global
    cv.circle(
        canvas_global, (cx_global, cy_global), 10, (0, 0, 255), -1
    )  # Punto rojo grande
    cv.circle(
        canvas_global, (cx_global, cy_global), 4, (255, 255, 255), -1
    )  # Centro blanco

    # Agregar etiqueta
    cv.putText(
        canvas_global,
        f"Centroide Global: ({cx_global},{cy_global})",
        (cx_global - 100, cy_global - 20),
        cv.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        1,
    )

cv.imshow("Centroide Global (Sin Contornos)", canvas_global)

# =============================================================================
# APLICAR EL MÉTODO DE CONECTIVIDAD
# =============================================================================

print("\n" + "=" * 60)

# Método 2: Separar figuras por conectividad
figuras_por_conectividad = separar_figuras_por_conectividad(canvas)

# =============================================================================
# VISUALIZAR LOS RESULTADOS DE CONECTIVIDAD
# =============================================================================

# Crear imagen para mostrar centroides individuales
canvas_conectividad = cv.cvtColor(canvas, cv.COLOR_GRAY2BGR)

colores_figuras = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

for i, figura in enumerate(figuras_por_conectividad):
    cx, cy = figura["centroide"]
    color = colores_figuras[i % len(colores_figuras)]

    # Dibujar centroide de cada figura
    cv.circle(canvas_conectividad, (cx, cy), 8, color, -1)
    cv.circle(canvas_conectividad, (cx, cy), 3, (255, 255, 255), -1)

    # Etiqueta para cada figura
    cv.putText(
        canvas_conectividad,
        f"Fig{figura['numero']}: ({cx},{cy})",
        (cx - 40, cy - 15),
        cv.FONT_HERSHEY_SIMPLEX,
        0.4,
        color,
        1,
    )

cv.imshow("Centroides por Conectividad", canvas_conectividad)


print("\n--- ANÁLISIS COMPARATIVO ---")
print("¿Cuál es la diferencia entre estos métodos?")
print()

print("MÉTODO GLOBAL (sin contornos):")
print("• Trata TODAS las figuras como una sola masa")
print("• Calcula UN solo centroide para toda la imagen")
print("• Es más simple pero menos informativo")
if centroide_global:
    print(f"• Resultado: {centroide_global}")
print()

print("MÉTODO DE CONECTIVIDAD:")
print("• Separa automáticamente las figuras conectadas")
print("• Calcula un centroide para cada figura individual")
print("• Es más complejo pero más útil para análisis detallado")
print(f"• Encontró {len(figuras_por_conectividad)} figuras separadas")
for figura in figuras_por_conectividad:
    print(
        f"  - Figura {figura['numero']}: centroide en {figura['centroide']}, área = {figura['area']} píxeles"
    )

print("\n--- REFLEXIÓN PEDAGÓGICA ---")
print("¿Cuándo usar cada método?")
print()
print("Usa el MÉTODO GLOBAL cuando:")
print("• Solo te interese el 'centro de masa' de todo el contenido")
print("• Las figuras estén muy dispersas y quieras encontrar el punto central")
print("• Estés analizando una sola figura compleja")
print()
print("Usa el MÉTODO DE CONECTIVIDAD cuando:")
print("• Tengas múltiples objetos separados")
print("• Necesites analizar cada objeto individualmente")
print("• Quieras contar cuántos objetos hay en la imagen")

print("\nObserva las tres ventanas para comparar los métodos.")
print("Presiona cualquier tecla para continuar...")

cv.waitKey(0)
cv.destroyAllWindows()
