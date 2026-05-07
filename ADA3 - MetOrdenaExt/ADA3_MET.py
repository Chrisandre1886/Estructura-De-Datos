import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
import time

class VisualSorting:
    def __init__(self):
        self.fig, self.axs = plt.subplots(1, 3, figsize=(15, 5))
        self.fig.suptitle('Métodos de Ordenamiento', fontsize=16, fontweight='bold')
        
    def intercalacion_sort(self, arr):
        """Método de Intercalación (Insertion Sort)"""
        n = len(arr)
        steps = []
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                steps.append(arr.copy())
            arr[j + 1] = key
            steps.append(arr.copy())
            
        return steps
    
    def mezcla_directa_sort(self, arr):
        """Método de Mezcla Directa (Bubble Sort)"""
        n = len(arr)
        steps = []
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps.append(arr.copy())
                    
        return steps
    
    def mezcla_equilibrada_sort(self, arr):
        """Método de Mezcla Equilibrada (Merge Sort)"""
        steps = []
        
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def merge_sort(arr):
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            
            merged = merge(left, right)
            steps.append(merged.copy())
            return merged
        
        merge_sort(arr.copy())
        return steps
    
    def generar_datos(self, n=20):
        """Genera datos aleatorios para ordenar"""
        return [random.randint(1, 100) for _ in range(n)]
    
    def visualizar_con_datos_personalizados(self, datos_usuario):
        """Visualiza los algoritmos con datos ingresados por el usuario"""
        # Crear copias para cada algoritmo
        datos_intercalacion = datos_usuario.copy()
        datos_mezcla_directa = datos_usuario.copy()
        datos_mezcla_equilibrada = datos_usuario.copy()
        
        # Obtener los pasos de cada algoritmo
        steps_intercalacion = self.intercalacion_sort(datos_intercalacion)
        steps_mezcla_directa = self.mezcla_directa_sort(datos_mezcla_directa)
        steps_mezcla_equilibrada = self.mezcla_equilibrada_sort(datos_mezcla_equilibrada)
        
        # Configurar colores
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                  '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
        
        # Función para actualizar todos los subplots
        def update_all(frame):
            # Actualizar Intercalación
            if frame < len(steps_intercalacion):
                self.axs[0].clear()
                bars1 = self.axs[0].bar(range(len(steps_intercalacion[frame])), 
                                       steps_intercalacion[frame],
                                       color=[colors[i % len(colors)] for i in range(len(steps_intercalacion[frame]))])
                self.axs[0].set_title(f'Intercalación (Insertion Sort)\nPaso {frame + 1}/{len(steps_intercalacion)}')
                self.axs[0].set_xlabel('Índice')
                self.axs[0].set_ylabel('Valor')
                self.axs[0].set_ylim(0, max(max(step) for step in steps_intercalacion) + 10)
                self.axs[0].grid(True, alpha=0.3)
            
            # Actualizar Mezcla Directa
            if frame < len(steps_mezcla_directa):
                self.axs[1].clear()
                bars2 = self.axs[1].bar(range(len(steps_mezcla_directa[frame])), 
                                       steps_mezcla_directa[frame],
                                       color=[colors[i % len(colors)] for i in range(len(steps_mezcla_directa[frame]))])
                self.axs[1].set_title(f'Mezcla Directa (Bubble Sort)\nPaso {frame + 1}/{len(steps_mezcla_directa)}')
                self.axs[1].set_xlabel('Índice')
                self.axs[1].set_ylabel('Valor')
                self.axs[1].set_ylim(0, max(max(step) for step in steps_mezcla_directa) + 10)
                self.axs[1].grid(True, alpha=0.3)
            
            # Actualizar Mezcla Equilibrada
            if frame < len(steps_mezcla_equilibrada):
                self.axs[2].clear()
                bars3 = self.axs[2].bar(range(len(steps_mezcla_equilibrada[frame])), 
                                       steps_mezcla_equilibrada[frame],
                                       color=[colors[i % len(colors)] for i in range(len(steps_mezcla_equilibrada[frame]))])
                self.axs[2].set_title(f'Mezcla Equilibrada (Merge Sort)\nPaso {frame + 1}/{len(steps_mezcla_equilibrada)}')
                self.axs[2].set_xlabel('Índice')
                self.axs[2].set_ylabel('Valor')
                self.axs[2].set_ylim(0, max(max(step) for step in steps_mezcla_equilibrada) + 10)
                self.axs[2].grid(True, alpha=0.3)
        
        max_frames = max(len(steps_intercalacion), 
                        len(steps_mezcla_directa), 
                        len(steps_mezcla_equilibrada))
        
        anim = FuncAnimation(self.fig, update_all, frames=max_frames, 
                           interval=300, repeat=False)
        
        plt.tight_layout()
        plt.show()
        return anim
    
    def mostrar_todos(self, datos_personalizados=None):
        """Muestra los tres algoritmos simultáneamente"""
        if datos_personalizados:
            datos_originales = datos_personalizados
        else:
            datos_originales = self.generar_datos(15)
        
        # Crear copias para cada algoritmo
        datos_intercalacion = datos_originales.copy()
        datos_mezcla_directa = datos_originales.copy()
        datos_mezcla_equilibrada = datos_originales.copy()
        
        # Obtener los pasos de cada algoritmo
        steps_intercalacion = self.intercalacion_sort(datos_intercalacion)
        steps_mezcla_directa = self.mezcla_directa_sort(datos_mezcla_directa)
        steps_mezcla_equilibrada = self.mezcla_equilibrada_sort(datos_mezcla_equilibrada)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                  '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
        
        # Función para actualizar todos los subplots
        def update_all(frame):
            # Actualizar Intercalación
            if frame < len(steps_intercalacion):
                self.axs[0].clear()
                bars1 = self.axs[0].bar(range(len(steps_intercalacion[frame])), 
                                       steps_intercalacion[frame],
                                       color=[colors[i % len(colors)] for i in range(len(steps_intercalacion[frame]))])
                self.axs[0].set_title(f'Intercalación (Insertion Sort)\nPaso {frame + 1}/{len(steps_intercalacion)}')
                self.axs[0].set_xlabel('Índice')
                self.axs[0].set_ylabel('Valor')
                self.axs[0].set_ylim(0, max(max(step) for step in steps_intercalacion) + 10)
                self.axs[0].grid(True, alpha=0.3)
            
            # Actualizar Mezcla Directa
            if frame < len(steps_mezcla_directa):
                self.axs[1].clear()
                bars2 = self.axs[1].bar(range(len(steps_mezcla_directa[frame])), 
                                       steps_mezcla_directa[frame],
                                       color=[colors[i % len(colors)] for i in range(len(steps_mezcla_directa[frame]))])
                self.axs[1].set_title(f'Mezcla Directa (Bubble Sort)\nPaso {frame + 1}/{len(steps_mezcla_directa)}')
                self.axs[1].set_xlabel('Índice')
                self.axs[1].set_ylabel('Valor')
                self.axs[1].set_ylim(0, max(max(step) for step in steps_mezcla_directa) + 10)
                self.axs[1].grid(True, alpha=0.3)
            
            # Actualizar Mezcla Equilibrada
            if frame < len(steps_mezcla_equilibrada):
                self.axs[2].clear()
                bars3 = self.axs[2].bar(range(len(steps_mezcla_equilibrada[frame])), 
                                       steps_mezcla_equilibrada[frame],
                                       color=[colors[i % len(colors)] for i in range(len(steps_mezcla_equilibrada[frame]))])
                self.axs[2].set_title(f'Mezcla Equilibrada (Merge Sort)\nPaso {frame + 1}/{len(steps_mezcla_equilibrada)}')
                self.axs[2].set_xlabel('Índice')
                self.axs[2].set_ylabel('Valor')
                self.axs[2].set_ylim(0, max(max(step) for step in steps_mezcla_equilibrada) + 10)
                self.axs[2].grid(True, alpha=0.3)
        
        max_frames = max(len(steps_intercalacion), 
                        len(steps_mezcla_directa), 
                        len(steps_mezcla_equilibrada))
        
        anim = FuncAnimation(self.fig, update_all, frames=max_frames, 
                           interval=300, repeat=False)
        
        plt.tight_layout()
        plt.show()
        return anim

class SortingAnalyzer:
    """Clase para analizar y comparar los algoritmos"""
    
    @staticmethod
    def comparar_rendimiento(tamaños=[10, 50, 100, 200]):
        """Compara el rendimiento de los tres algoritmos"""
        resultados = {'tamaños': tamaños, 
                     'intercalacion': [], 
                     'mezcla_directa': [], 
                     'mezcla_equilibrada': []}
        
        visual = VisualSorting()
        
        for n in tamaños:
            datos = visual.generar_datos(n)
            
            # Medir Intercalación
            start = time.time()
            visual.intercalacion_sort(datos.copy())
            resultados['intercalacion'].append(time.time() - start)
            
            # Medir Mezcla Directa
            start = time.time()
            visual.mezcla_directa_sort(datos.copy())
            resultados['mezcla_directa'].append(time.time() - start)
            
            # Medir Mezcla Equilibrada
            start = time.time()
            visual.mezcla_equilibrada_sort(datos.copy())
            resultados['mezcla_equilibrada'].append(time.time() - start)
        
        # Graficar resultados
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(tamaños, resultados['intercalacion'], 'o-', label='Intercalación (O(n²))', linewidth=2, markersize=8)
        ax.plot(tamaños, resultados['mezcla_directa'], 's-', label='Mezcla Directa (O(n²))', linewidth=2, markersize=8)
        ax.plot(tamaños, resultados['mezcla_equilibrada'], '^-', label='Mezcla Equilibrada (O(n log n))', linewidth=2, markersize=8)
        
        ax.set_xlabel('Tamaño del Array', fontsize=12)
        ax.set_ylabel('Tiempo de Ejecución (segundos)', fontsize=12)
        ax.set_title('Comparación de Rendimiento de Algoritmos de Ordenamiento', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return resultados

def ingresar_datos_usuario():
    """Función para que el usuario ingrese sus propios datos"""
    print("\n--- INGRESO DE DATOS PERSONALIZADOS ---")
    print("Puedes ingresar números separados por espacios o comas")
    
    while True:
        entrada = input("\nIngresa los números (ejemplo: 5 3 8 1 9 2): ")
        
        # Limpiar la entrada y convertir a números
        entrada = entrada.replace(',', ' ')
        numeros = entrada.split()
        
        try:
            datos = [int(num) for num in numeros]
            if len(datos) == 0:
                print("Error: No ingresaste ningún número. Intenta de nuevo.")
                continue
            if len(datos) > 30:
                print("Advertencia: Has ingresado muchos números (>30). La visualización puede ser lenta.")
                respuesta = input("¿Deseas continuar de todas formas? (s/n): ")
                if respuesta.lower() != 's':
                    continue
            print(f"\nDatos ingresados: {datos}")
            return datos
        except ValueError:
            print("Error: Por favor ingresa solo números enteros válidos.")
            continue

def main():
    """Función principal del programa"""
    print("=== PROGRAMA DE VISUALIZACIÓN DE ALGORITMOS DE ORDENAMIENTO ===\n")
    print("Algoritmos implementados:")
    print("1. Intercalación (Insertion Sort)")
    print("2. Mezcla Directa (Bubble Sort)")
    print("3. Mezcla Equilibrada (Merge Sort)\n")
    
    visualizador = VisualSorting()
    analizador = SortingAnalyzer()
    datos_usuario = None
    
    while True:
        print("\n" + "="*50)
        print("--- MENÚ PRINCIPAL ---")
        print("1. Usar datos aleatorios (visualización)")
        print("2. Ingresar mis propios datos")
        print("3. Ver datos actuales")
        print("4. Analizar rendimiento de los algoritmos")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción (1-5): ")
        
        if opcion == '1':
            if datos_usuario:
                print(f"\nUsando datos personalizados: {datos_usuario}")
                visualizador.mostrar_todos(datos_usuario)
            else:
                print("\nGenerando visualización con datos aleatorios...")
                visualizador.mostrar_todos()
            
        elif opcion == '2':
            datos_usuario = ingresar_datos_usuario()
            print("\nVisualizando con tus datos...")
            visualizador.visualizar_con_datos_personalizados(datos_usuario)
            
        elif opcion == '3':
            if datos_usuario:
                print(f"\nDatos actuales (personalizados): {datos_usuario}")
                
                # Mostrar resultados de cada algoritmo con los datos actuales
                datos_inter = datos_usuario.copy()
                visualizador.intercalacion_sort(datos_inter)
                print(f"Intercalación ordenado: {datos_inter}")
                
                datos_directa = datos_usuario.copy()
                visualizador.mezcla_directa_sort(datos_directa)
                print(f"Mezcla Directa ordenado: {datos_directa}")
                
                datos_equilibrada = datos_usuario.copy()
                visualizador.mezcla_equilibrada_sort(datos_equilibrada)
                print(f"Mezcla Equilibrada ordenado: {datos_equilibrada}")
            else:
                print("\nNo hay datos personalizados. Generando datos aleatorios...")
                datos_aleatorios = visualizador.generar_datos(15)
                print(f"Datos aleatorios generados: {datos_aleatorios}")
                
                # Mostrar resultados con datos aleatorios
                datos_inter = datos_aleatorios.copy()
                visualizador.intercalacion_sort(datos_inter)
                print(f"Intercalación ordenado: {datos_inter}")
                
                datos_directa = datos_aleatorios.copy()
                visualizador.mezcla_directa_sort(datos_directa)
                print(f"Mezcla Directa ordenado: {datos_directa}")
                
                datos_equilibrada = datos_aleatorios.copy()
                visualizador.mezcla_equilibrada_sort(datos_equilibrada)
                print(f"Mezcla Equilibrada ordenado: {datos_equilibrada}")
            
        elif opcion == '4':
            print("\n--- ANÁLISIS DE RENDIMIENTO ---")
            print("Este análisis mostrará gráficos comparativos de velocidad")
            print("entre los tres algoritmos con diferentes tamaños de datos.\n")
            
            # Preguntar si quiere usar sus datos para el análisis
            if datos_usuario and len(datos_usuario) > 0:
                print(f"Tus datos actuales tienen {len(datos_usuario)} elementos.")
                respuesta = input("¿Quieres analizar el rendimiento con tus datos? (s/n): ")
                if respuesta.lower() == 's':
                    print("\nAnalizando rendimiento con tus datos...")
                    # Análisis personalizado con los datos del usuario
                    tiempos = {'intercalacion': 0, 'mezcla_directa': 0, 'mezcla_equilibrada': 0}
                    
                    start = time.time()
                    visualizador.intercalacion_sort(datos_usuario.copy())
                    tiempos['intercalacion'] = time.time() - start
                    
                    start = time.time()
                    visualizador.mezcla_directa_sort(datos_usuario.copy())
                    tiempos['mezcla_directa'] = time.time() - start
                    
                    start = time.time()
                    visualizador.mezcla_equilibrada_sort(datos_usuario.copy())
                    tiempos['mezcla_equilibrada'] = time.time() - start
                    
                    print(f"\nTiempos de ejecución con {len(datos_usuario)} elementos:")
                    print(f"  Intercalación: {tiempos['intercalacion']:.6f} seg")
                    print(f"  Mezcla Directa: {tiempos['mezcla_directa']:.6f} seg")
                    print(f"  Mezcla Equilibrada: {tiempos['mezcla_equilibrada']:.6f} seg")
                    
                    # Crear gráfico de barras para comparación rápida
                    fig, ax = plt.subplots(figsize=(8, 5))
                    algoritmos = list(tiempos.keys())
                    valores = list(tiempos.values())
                    colores = ['#FF6B6B', '#4ECDC4', '#45B7D1']
                    
                    ax.bar(algoritmos, valores, color=colores)
                    ax.set_ylabel('Tiempo (segundos)')
                    ax.set_title(f'Comparación de tiempo con {len(datos_usuario)} elementos')
                    ax.grid(True, alpha=0.3)
                    
                    plt.tight_layout()
                    plt.show()
                else:
                    analizador.comparar_rendimiento()
            else:
                analizador.comparar_rendimiento()
            
        elif opcion == '5':
            print("\n¡Gracias por usar el programa!")
            print("Desarrollado con Python y Matplotlib")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione 1-5.")

if __name__ == "__main__":
    main()