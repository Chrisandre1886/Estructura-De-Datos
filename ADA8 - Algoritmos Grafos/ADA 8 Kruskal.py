def kruskal(nodos, aristas):
    aristas.sort(key=lambda x: x[2])

    padre = {nodo: nodo for nodo in nodos}

    def encontrar(nodo):
        if padre[nodo] != nodo:
            padre[nodo] = encontrar(padre[nodo])
        return padre[nodo]

    def unir(n1, n2):
        raiz1 = encontrar(n1)
        raiz2 = encontrar(n2)
        if raiz1 != raiz2:
            padre[raiz2] = raiz1
            return True
        return False

    arbol = []
    costo = 0

    for u, v, peso in aristas:
        if unir(u, v):
            arbol.append((u, v, peso))
            costo += peso

    return arbol, costo


nodos = ['A', 'B', 'C', 'D']
aristas = [
    ('A', 'B', 1),
    ('A', 'C', 5),
    ('B', 'C', 3),
    ('B', 'D', 7),
    ('C', 'D', 2)
]

arbol, costo = kruskal(nodos, aristas)
print("Árbol:", arbol)
print("Costo total:", costo)