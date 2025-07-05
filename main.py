import random
import numpy as np
from time import process_time
import matplotlib.pyplot as plt

# Elementos del refugio
posibles_casos = ["B",".","R"]  # B=Bomba, .=Espacio vacío, R=cápsula de Remedio

def crear_refugio(Espacio):
    """
    Genera un refugio completamente aleatorio de tamaño n x n, sin garantizar ningún camino seguro ni restricciones especiales para ninguna celda.
    Args:
        Espacio (int): Tamaño del refugio (n).
    Returns:
        np.ndarray: Matriz del refugio.
    """
    Refugio = np.empty((Espacio, Espacio), dtype=object)
    for i in range(Espacio):
        for j in range(Espacio):
            r = random.uniform(0, 1)
            if r < 0.2:
                Refugio[i][j] = "💣"  # Bomba
            elif r < 0.3:
                Refugio[i][j] = "💊"  # Cápsula
            else:
                Refugio[i][j] = "⬜"  # Espacio vacío
    return Refugio

def mostrar_refugio(Refugio):
    print("Refugio:")
    for fila in Refugio:
        print(' '.join(fila))
    print()


def resolver(x, y, pasos, Refugio, tamano, max_pasos, memo):
    """
    Resuelve el problema usando programación dinámica y memoización con arreglo.
    Calcula el máximo número de cápsulas recolectables desde (x, y) hasta la meta,
    en un máximo de max_pasos, evitando bombas.
    Args:
        x (int): Fila actual.
        y (int): Columna actual.
        pasos (int): Pasos dados hasta ahora.
        Refugio (np.ndarray): Matriz del refugio.
        tamano (int): Tamaño del refugio (n).
        max_pasos (int): Máximo de pasos permitidos.
        memo (np.ndarray): Arreglo para memoización.
    Returns:
        int: Máximo de cápsulas recolectables o -inf si no hay camino.
    """
    if x < 0 or y < 0 or x >= tamano or y >= tamano:
        return -float('inf')  # Fuera de límites
    if Refugio[x][y] == "💣":
        return -float('inf')  # Bomba
    if pasos > max_pasos:
        return -float('inf')  # Excede pasos
    if memo[x][y][pasos] is not None:
        return memo[x][y][pasos]
    if x == tamano - 1 and y == tamano - 1:
        # Llegó a la meta
        memo[x][y][pasos] = 1 if Refugio[x][y] == "💊" else 0
        return memo[x][y][pasos]
    valor = 1 if Refugio[x][y] == "💊" else 0
    # Calcula el mejor resultado moviéndose derecha o abajo
    mejor = max(
        resolver(x + 1, y, pasos + 1, Refugio, tamano, max_pasos, memo),
        resolver(x, y + 1, pasos + 1, Refugio, tamano, max_pasos, memo)
    )
    memo[x][y][pasos] = valor + mejor
    return memo[x][y][pasos]

def resolucion_array(Refugio):
    """
    Inicializa la memoización con arreglo y resuelve el refugio.
    Args:
        Refugio (np.ndarray): Matriz del refugio.
    Returns:
        int: Máximo de cápsulas recolectables o -inf si no hay camino.
    """
    tamano = len(Refugio)
    max_pasos = 2 * tamano - 2
    memo = np.full((tamano, tamano, max_pasos + 1), None, dtype=object)
    resultado = resolver(0, 0, 0, Refugio, tamano, max_pasos, memo)
    return resultado


def resolver_diccionario(x, y, pasos, Refugio, tamano, max_pasos, memo):
    """
    Resuelve el problema usando programación dinámica y memoización con diccionario.
    Calcula el máximo número de cápsulas recolectables desde (x, y) hasta la meta,
    en un máximo de max_pasos, evitando bombas.
    Args:
        x (int): Fila actual.
        y (int): Columna actual.
        pasos (int): Pasos dados hasta ahora.
        Refugio (np.ndarray): Matriz del refugio.
        tamano (int): Tamaño del refugio (n).
        max_pasos (int): Máximo de pasos permitidos.
        memo (dict): Diccionario para memoización.
    Returns:
        int: Máximo de cápsulas recolectables o -inf si no hay camino.
    """
    key = (x, y, pasos)
    if key in memo:
        return memo[key]
    if x < 0 or y < 0 or x >= tamano or y >= tamano:
        return -float('inf')  # Fuera de límites
    if Refugio[x][y] == "💣":
        return -float('inf')  # Bomba
    if pasos > max_pasos:
        return -float('inf')  # Excede pasos
    if x == tamano - 1 and y == tamano - 1:
        # Llegó a la meta
        memo[key] = 1 if Refugio[x][y] == "💊" else 0
        return memo[key]
    valor = 1 if Refugio[x][y] == "💊" else 0
    # Calcula el mejor resultado moviéndose derecha o abajo
    mejor = max(
        resolver_diccionario(x + 1, y, pasos + 1, Refugio, tamano, max_pasos, memo),
        resolver_diccionario(x, y + 1, pasos + 1, Refugio, tamano, max_pasos, memo)
    )
    memo[key] = valor + mejor
    return memo[key]

def resolucion_diccionario(Refugio):
    """
    Inicializa la memoización con diccionario y resuelve el refugio.
    Args:
        Refugio (np.ndarray): Matriz del refugio.
    Returns:
        int: Máximo de cápsulas recolectables o -inf si no hay camino.
    """
    tamano = len(Refugio)
    max_pasos = 2 * tamano - 2
    memo = dict()
    resultado = resolver_diccionario(0, 0, 0, Refugio, tamano, max_pasos, memo)
    return resultado



def main():
    """
    Ejecuta pruebas incrementando el tamaño del refugio y muestra resultados usando memoización con diccionario.
    Detiene la prueba si el tiempo por instancia excede el límite o si hay error/memoria insuficiente.
    """
    limite_tiempo = 10  # segundos por instancia
    tamanos = []
    resultados = []
    tiempos = []
    memorias = []
    print(f"{'n':>4} | {'Cápsulas':>10} | {'Tiempo (s)':>10} | {'Memoria (MB)':>13} | {'% Bombas':>9} | {'% Cápsulas':>10}")
    print('-'*75)
    for n in range(10, 50, 10):  # Incrementa de 10 en 10 hasta 50
        Refugio = crear_refugio(n)
        mostrar_refugio(Refugio)
        # Calcular % bombas y % cápsulas
        total = n * n
        bombas = np.sum(Refugio == '💣')
        capsulas = np.sum(Refugio == '💊')
        pct_bombas = 100 * bombas / total
        pct_capsulas = 100 * capsulas / total
        import tracemalloc
        tracemalloc.start()
        inicio = process_time()
        try:
            resultado = resolucion_array(Refugio)
            fin = process_time()
            tiempo = fin - inicio
            mem = tracemalloc.get_traced_memory()[1] / (1024*1024)
            tracemalloc.stop()
            if resultado == -float('inf'):
                res_str = "No posible"
            else:
                res_str = str(resultado)
            print(f"{n:>4} | {res_str:>10} | {tiempo:10.4f} | {mem:13.2f} | {pct_bombas:9.2f} | {pct_capsulas:10.2f}")
            tamanos.append(n)
            resultados.append(resultado)
            tiempos.append(tiempo)
            memorias.append(mem)
            if tiempo > limite_tiempo:
                print(f"Tiempo excedido para n={n} (>{limite_tiempo}s). Se detiene la prueba.")
                break
        except Exception as e:
            tracemalloc.stop()
            print(f"No se pudo calcular el valor para n={n}: {e}")
            break

    # Graficar tiempo de ejecución vs tamaño n (X=n, Y=tiempo de ejecución real)
    plt.figure(figsize=(8, 5))
    plt.plot(tamanos, tiempos, marker='o', linestyle='-', color='blue', label='Tiempo de ejecución')
    for x, y in zip(tamanos, tiempos):
        plt.text(x, y, f"{y:.2f}", fontsize=8, ha='center', va='bottom')
    plt.xlabel('Valor de N')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title('Tiempo de ejecución vs Valor de N')
    plt.grid(True, which='both', axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
