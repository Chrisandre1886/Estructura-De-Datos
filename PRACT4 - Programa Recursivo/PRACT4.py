import time

def fibonacci_recursivo(n):
    """
    Versión recursiva de Fibonacci
    """
    if n <= 1:
        return n
    return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)

def fibonacci_iterativo(n):
    """
    Versión iterativa de Fibonacci
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def medir_tiempo(funcion, n):
    """
    Mide el tiempo de ejecución de una función
    """
    inicio = time.perf_counter()
    resultado = funcion(n)
    fin = time.perf_counter()
    tiempo = (fin - inicio) * 1000  # Convertir a milisegundos
    return resultado, tiempo

def mostrar_serie(n, usar_recursivo=True):
    """
    Muestra la serie Fibonacci hasta el término n
    """
    print(f"\n--- Serie Fibonacci hasta término {n} ---")
    
    if usar_recursivo:
        print("Método: Recursivo")
        for i in range(n + 1):
            resultado, tiempo = medir_tiempo(fibonacci_recursivo, i)
            print(f"F({i}) = {resultado:<10} | Tiempo: {tiempo:.6f} ms")
    else:
        print("Método: Iterativo")
        a, b = 0, 1
        for i in range(n + 1):
            inicio = time.perf_counter()
            if i == 0:
                valor = a
            elif i == 1:
                valor = b
            else:
                a, b = b, a + b
                valor = b
            fin = time.perf_counter()
            tiempo = (fin - inicio) * 1000
            print(f"F({i}) = {valor:<10} | Tiempo: {tiempo:.6f} ms")

def menu_interactivo():
    """
    Menú interactivo principal
    """
    while True:
        print("\n" + "="*50)
        print(" PROGRAMA FIBONACCI - COMPARACIÓN DE MÉTODOS")
        print("="*50)
        print("1. Calcular un término específico (comparar métodos)")
        print("2. Mostrar serie completa (recursivo)")
        print("3. Mostrar serie completa (iterativo)")
        print("4. Comparar tiempos de ejecución")
        print("5. Salir")
        print("="*50)
        
        opcion = input("Selecciona una opción (1-5): ").strip()
        
        if opcion == '1':
            try:
                n = int(input("Ingresa el término a calcular (n): "))
                if n < 0:
                    print("Por favor ingresa un número no negativo.")
                    continue
                
                print(f"\n--- Calculando F({n}) ---")
                
                # Método recursivo
                resultado_rec, tiempo_rec = medir_tiempo(fibonacci_recursivo, n)
                print(f"Recursivo: F({n}) = {resultado_rec}")
                print(f"Tiempo: {tiempo_rec:.6f} ms")
                
                # Método iterativo
                resultado_it, tiempo_it = medir_tiempo(fibonacci_iterativo, n)
                print(f"Iterativo: F({n}) = {resultado_it}")
                print(f"Tiempo: {tiempo_it:.6f} ms")
                
                # Comparación
                if tiempo_rec > tiempo_it:
                    print(f"\nEl método iterativo fue {tiempo_rec/tiempo_it:.2f} veces más rápido")
                else:
                    print(f"\nEl método recursivo fue {tiempo_it/tiempo_rec:.2f} veces más rápido")
                    
            except ValueError:
                print("Error: Ingresa un número válido.")
                
        elif opcion == '2':
            try:
                n = int(input("¿Hasta qué término quieres ver la serie? "))
                if n < 0:
                    print("Por favor ingresa un número no negativo.")
                    continue
                if n > 30:
                    print("⚠️  ADVERTENCIA: n > 30 puede tomar mucho tiempo con el método recursivo")
                    confirmar = input("¿Continuar? (s/n): ").lower()
                    if confirmar != 's':
                        continue
                mostrar_serie(n, usar_recursivo=True)
            except ValueError:
                print("Error: Ingresa un número válido.")
                
        elif opcion == '3':
            try:
                n = int(input("¿Hasta qué término quieres ver la serie? "))
                if n < 0:
                    print("Por favor ingresa un número no negativo.")
                    continue
                mostrar_serie(n, usar_recursivo=False)
            except ValueError:
                print("Error: Ingresa un número válido.")
                
        elif opcion == '4':
            print("\n--- COMPARACIÓN DE TIEMPOS ---")
            print("n\tRecursivo (ms)\tIterativo (ms)\tDiferencia")
            print("-" * 50)
            
            for n in range(0, 36, 5):
                if n > 30:
                    print(f"{n}\tN/A (muy lento)\t?", end="")
                    _, tiempo_it = medir_tiempo(fibonacci_iterativo, n)
                    print(f"\t{tiempo_it:.6f}")
                else:
                    _, tiempo_rec = medir_tiempo(fibonacci_recursivo, n)
                    _, tiempo_it = medir_tiempo(fibonacci_iterativo, n)
                    print(f"{n}\t{tiempo_rec:.6f}\t\t{tiempo_it:.6f}\t\t{tiempo_rec/tiempo_it:.2f}x")
                    
        elif opcion == '5':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor selecciona 1-5.")

# Ejecutar el programa
if __name__ == "__main__":
    menu_interactivo()