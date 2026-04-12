def floyd(grafo):
   
    n = len(grafo)
    dist = [fila[:] for fila in grafo]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist

INF = float('inf')
grafo_matriz = [
    [0, 3, INF, 5],
    [2, 0, INF, 4],
    [INF, 1, 0, INF],
    [INF, INF, 2, 0]
]

nodos = ['A', 'B', 'C', 'D']

print("\n=== Algoritmo de Floyd ===")
print("Matriz de distancias original:")
for i in range(len(grafo_matriz)):
    print([f"{x:3}" if x != INF else " INF" for x in grafo_matriz[i]])

distancias_floyd = floyd(grafo_matriz)

print("\nMatriz de distancias mínimas:")
for i in range(len(distancias_floyd)):
    print([f"{x:3}" if x != INF else " INF" for x in distancias_floyd[i]])