import heapq

def dijkstra(grafo, inicio):
    
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]  
    visitados = set()
    
    while cola_prioridad:
        dist_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual in visitados:
            continue
            
        visitados.add(nodo_actual)
        
        for vecino, peso in grafo[nodo_actual]:
            distancia = dist_actual + peso
            
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola_prioridad, (distancia, vecino))
    
    return distancias

grafo_ejemplo = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}

print("=== Algoritmo de Dijkstra ===")
distancias = dijkstra(grafo_ejemplo, 'A')
for nodo, distancia in distancias.items():
    print(f"Distancia de A a {nodo}: {distancia}")