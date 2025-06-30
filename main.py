import random
import numpy as np
import copy

#Se declaran 
posibles_casos = ["💣","🔳","💊"]
#posibles_casos = [".","B","R"]

Espacio = 10

Refugio = np.empty((Espacio, Espacio), dtype=object)

def crear_refugio(Espacio):
    Refugio = np.empty((Espacio, Espacio), dtype=object)
    for i in range(Espacio):
        for j in range(Espacio):
            #Agregar un caso aleatorio a cada celda del refugio
            Refugio[i][j] = posibles_casos[random.randint(0, len(posibles_casos) - 1)]

            #Asegurar que las esquinas tengan un caso diferente
            if i == 0 and j == 0:
                Refugio[i][j] = posibles_casos[random.randint(1, len(posibles_casos) - 1)]
            elif i == Espacio - 1 and j == Espacio - 1:
                Refugio[i][j] = posibles_casos[random.randint(1, len(posibles_casos) - 1)]

    return Refugio

Refugio = crear_refugio(Espacio)

def resolver(x, y, pasos, Refugio, tamano, max_pasos, memo, visitados=None):
    # Inicializar el conjunto de visitados si es la primera llamada
    if visitados is None:
        visitados = set()
    # Si está fuera del refugio, no es válido
    if x < 0 or x >= tamano or y < 0 or y >= tamano:
        return None
    # Si hay una bomba, no es válido
    if Refugio[x][y] == "💣":
        return None
    # Si se exceden los pasos máximos, no es válido
    if pasos > max_pasos:
        return None
    # Si ya visitamos esta celda en este camino, evitar ciclos
    if (x, y) in visitados:
        return None
    # Si llegó a la meta, cuenta la cápsula si hay
    if (x, y) == (tamano-1, tamano-1):
        # Contar si hay una cápsula en la meta
        if Refugio[x][y] == "💊":
            return 1  # Hay una cápsula en la meta
        else:
            return 0  # No hay cápsula en la meta

    # Si ya calculamos este estado, devolvemos el resultado guardado
    if memo[x][y][pasos] is not None:
        return memo[x][y][pasos]

    # Marcar la celda como visitada en este camino
    visitados.add((x, y))
    # Probar moverse en las 4 direcciones
    direcciones = [(-1,0), (1,0), (0,-1), (0,1)]
    mejores = []
    for mov_x, mov_y in direcciones:
        nuevo_x, nuevo_y = x + mov_x, y + mov_y
        resultado = resolver(nuevo_x, nuevo_y, pasos+1, Refugio, tamano, max_pasos, memo, visitados.copy())
        if resultado is not None:
            mejores.append(resultado)
    # Desmarcar la celda (no necesario por el uso de copy, pero por claridad)
    # Si no hay caminos válidos desde aquí, guardar y retornar None
    if not mejores:
        memo[x][y][pasos] = None
        return None
    # Tomar el mejor camino posible
    mejor_cantidad = max(mejores)
    # Sumar cápsula si hay en la celda actual
    if Refugio[x][y] == "💊":
        mejor_cantidad += 1
    memo[x][y][pasos] = mejor_cantidad
    return mejor_cantidad

def resolucion_array(Refugio):
    tamano = len(Refugio)
    print(f"Tamaño del Refugio: {tamano}")
    max_pasos = 2 * tamano - 2  # Máximo de pasos permitidos para llegar a la meta
    memo = np.full((tamano, tamano, max_pasos + 1), None, dtype=object)
    resultado = resolver(0, 0, 0, Refugio, tamano, max_pasos, memo)
    return resultado

resultado = resolucion_array(Refugio)
print("Refugio:")
for fila in Refugio:
    print(' '.join(fila))

if resultado is None:
    print("\nNo hay camino posible para recolectar cápsulas.")
else:
    print(f"\nMáximo de cápsulas recolectables: {resultado}")
