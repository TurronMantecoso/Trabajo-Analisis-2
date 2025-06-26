import random
import numpy as np

posibles_casos = ["💣","🔳","💊"]

Espacio = 10

Refugio = np.empty((Espacio, Espacio), dtype=object)


for i in range(Espacio):
    for j in range(Espacio):
        Refugio[i][j] = posibles_casos[random.randint(0, len(posibles_casos) - 1)]
        if i == 0 and j == 0:
            Refugio[i][j] = posibles_casos[random.randint(1, len(posibles_casos) - 1)]
        elif i == Espacio - 1 and j == Espacio - 1:
            Refugio[i][j] = posibles_casos[random.randint(1, len(posibles_casos) - 1)]


#print(posibles_casos[random.randint(0, len(posibles_casos) - 1)])

print(Refugio)