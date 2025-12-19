def cuadrado_magico_siames(n):

    if n % 2 == 0:
        return None

    #matriz vacía
    cuadrado = [[0 for _ in range(n)] for _ in range(n)]

    # Posición inicial: medio de la primera fila
    fila = 0
    col = n // 2

    for num in range(1, n * n + 1):
        cuadrado[fila][col] = num

        # Calcular siguiente posición
        nueva_fila = (fila - 1) % n
        nueva_col = (col + 1) % n

        # Si la celda está ocupada, mover hacia abajo desde la posición actual
        if cuadrado[nueva_fila][nueva_col] != 0:
            fila = (fila + 1) % n
        else:
            fila = nueva_fila
            col = nueva_col

    return cuadrado


def imprimir_cuadrado(cuadrado):
    n = len(cuadrado)

    for fila in cuadrado:
        print("  ", end="")
        for num in fila:
            print(f"{num:3}", end=" ")
        print()

    constante = sum(cuadrado[0])

    print(f"Constante mágica: {constante}")



def verificar_cuadrado(cuadrado):
    """Verifica si es un cuadrado mágico válido"""
    n = len(cuadrado)
    constante = sum(cuadrado[0])

    # Verificar filas
    for fila in cuadrado:
        if sum(fila) != constante:
            return False

    # Verificar columnas
    for col in range(n):
        if sum(cuadrado[fila][col] for fila in range(n)) != constante:
            return False

    # Verificar diagonal principal
    if sum(cuadrado[i][i] for i in range(n)) != constante:
        return False

    # Verificar diagonal secundaria
    if sum(cuadrado[i][n - 1 - i] for i in range(n)) != constante:
        return False

    return True


# Programa principal
if __name__ == "__main__":
    cuadrado = cuadrado_magico_siames(3)

    if cuadrado:
        imprimir_cuadrado(cuadrado)