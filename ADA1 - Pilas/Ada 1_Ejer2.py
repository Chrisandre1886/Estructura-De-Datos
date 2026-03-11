class Pila:
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.esta_vacia():
            return self.items.pop()
        return None
    
    def ver_tope(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None
    
    def mostrar(self):
        return self.items

def mover_disco(origen, destino):
    disco = origen.pop()
    destino.push(disco)
    print(f"Mover disco {disco} de {origen.nombre} a {destino.nombre}")

def hanoi(n, origen, destino, auxiliar):
    if n == 1:
        mover_disco(origen, destino)
    else:
        hanoi(n-1, origen, auxiliar, destino)
        mover_disco(origen, destino)
        hanoi(n-1, auxiliar, destino, origen)

# Inicializar las torres con 3 discos
torre_a = Pila("A")
torre_b = Pila("B")
torre_c = Pila("C")

# Agregar discos (3,2,1 donde 3 es el más grande)
torre_a.push(3)
torre_a.push(2)
torre_a.push(1)

print("Estado inicial:")
print(f"Torre A: {torre_a.mostrar()}")
print(f"Torre B: {torre_b.mostrar()}")
print(f"Torre C: {torre_c.mostrar()}")
print("\nResolviendo Hanoi con 3 discos:\n")

# Resolver el problema
hanoi(3, torre_a, torre_c, torre_b)

print("\nEstado final:")
print(f"Torre A: {torre_a.mostrar()}")
print(f"Torre B: {torre_b.mostrar()}")
print(f"Torre C: {torre_c.mostrar()}")