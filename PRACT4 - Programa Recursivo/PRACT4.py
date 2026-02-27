import time

def fib_recursivo(n):
    if n <= 1:
        return n
    return fib_recursivo(n-1) + fib_recursivo(n-2)

def fib_iterativo(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


n = int(input("Ingresa el número: "))

if n > 35:
    print("Advertencia: valores mayores a 35 pueden tardar mucho con el método recursivo.")


inicio = time.time()
resultado_rec = fib_recursivo(n)
tiempo_rec = time.time() - inicio

inicio = time.time()
resultado_it = fib_iterativo(n)
tiempo_it = time.time() - inicio


print(f"\nFibonacci recursivo: {resultado_rec}")
print(f"Tiempo recursivo: {tiempo_rec:.5f} segundos")

print(f"\nFibonacci iterativo: {resultado_it}")
print(f"Tiempo iterativo: {tiempo_it:.5f} segundos")