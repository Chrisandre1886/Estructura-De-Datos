class Cola:
    def __init__(self, tamaño=None):
        self.elementos = []
        self.tamaño = tamaño
        self.limite_alcanzado = False
    
    def encolar(self, elemento):
        if self.tamaño is None or len(self.elementos) < self.tamaño:
            self.elementos.append(elemento)
            return True
        else:
            self.limite_alcanzado = True
            print(f"¡No se puede agregar más elementos! Límite de {self.tamaño} alcanzado.")
            return False
    
    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        return None
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def mostrar(self):
        return self.elementos
    
    def tamaño_actual(self):
        return len(self.elementos)

def sumar_colas(cola1, cola2):
    cola_resultado = Cola()
    
    while not cola1.esta_vacia() and not cola2.esta_vacia():
        suma = cola1.desencolar() + cola2.desencolar()
        cola_resultado.encolar(suma)
    
    return cola_resultado

def crear_colas_mismo_tamaño():
    print("\n--- CONFIGURACIÓN DE COLAS ---")
    
    while True:
        try:
            tamaño = int(input("Ingrese el tamaño de las colas (será el mismo para ambas): "))
            if tamaño <= 0:
                print("El tamaño debe ser un número positivo. Intente nuevamente.")
            else:
                break
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    print(f"\n--- PRIMERA COLA (tamaño: {tamaño}) ---")
    cola1 = Cola(tamaño)
    print(f"Ingrese {tamaño} números para la primera cola:")
    i = 0
    while i < tamaño:
        try:
            numero = int(input(f"Número {i+1}: "))
            cola1.encolar(numero)
            i += 1
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    print(f"\n--- SEGUNDA COLA (tamaño: {tamaño}) ---")
    cola2 = Cola(tamaño)
    print(f"Ingrese {tamaño} números para la segunda cola:")
    i = 0
    while i < tamaño:
        try:
            numero = int(input(f"Número {i+1}: "))
            cola2.encolar(numero)
            i += 1
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    return cola1, cola2

if __name__ == "__main__":
    print("=== PROGRAMA PARA SUMAR COLAS ===\n")
    
    cola_a, cola_b = crear_colas_mismo_tamaño()
    
    elementos_a = cola_a.mostrar().copy()
    elementos_b = cola_b.mostrar().copy()
    
    cola_resultado = sumar_colas(cola_a, cola_b)
    
    print("\n" + "="*50)
    print("RESULTADOS:")
    print("="*50)
    print(f"Cola A: {elementos_a}")
    print(f"Cola B: {elementos_b}")
    print(f"Cola Resultado: {cola_resultado.mostrar()}")
    
    print("\n--- DETALLE DE LA SUMA ---")
    for i in range(len(elementos_a)):
        suma = elementos_a[i] + elementos_b[i]
        print(f"{elementos_a[i]} + {elementos_b[i]} = {suma}")