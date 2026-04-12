def warshall(matriz_adyacencia):
    
    n = len(matriz_adyacencia)
    matriz_cierre = [fila[:] for fila in matriz_adyacencia]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matriz_cierre[i][k] and matriz_cierre[k][j]:
                    matriz_cierre[i][j] = True
    
    return matriz_cierre

print("\n=== Algoritmo de Warshall ===")

grafo_adyacencia = [
    [False, True, False, False],  # A -> B
    [False, False, True, False],  # B -> C
    [False, False, False, True],  # C -> D
    [True, False, False, False]   # D -> A
]

nodos_w = ['A', 'B', 'C', 'D']

print("Matriz de adyacencia original:")
for i in range(len(grafo_adyacencia)):
    fila = [nodos_w[j] if grafo_adyacencia[i][j] else '.' for j in range(len(grafo_adyacencia))]
    print(f"{nodos_w[i]}: {fila}")

cierre = warshall(grafo_adyacencia)

print("\nMatriz de cierre transitivo (alcanzabilidad):")
for i in range(len(cierre)):
    fila = [nodos_w[j] if cierre[i][j] else '.' for j in range(len(cierre))]
    print(f"{nodos_w[i]}: {fila}")