import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class OrdenamientoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos de Ordenamiento")
        self.root.geometry("900x650")
        self.root.configure(bg='#1e1e2e')
        
        self.datos = []
        self.historial = []
        self.paso_actual = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Estilo
        style = ttk.Style()
        style.configure('TLabel', background='#1e1e2e', foreground='white')
        style.configure('TFrame', background='#1e1e2e')
        style.configure('TLabelframe', background='#1e1e2e', foreground='white')
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Datos", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Cantidad:").grid(row=0, column=0, padx=5)
        self.cantidad_entry = ttk.Entry(input_frame, width=10)
        self.cantidad_entry.grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Generar", command=self.generar_campos).grid(row=0, column=2, padx=5)
        
        self.numeros_frame = ttk.Frame(input_frame)
        self.numeros_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        # Frame de métodos
        metodo_frame = ttk.LabelFrame(main_frame, text="Método", padding="10")
        metodo_frame.pack(fill=tk.X, pady=5)
        
        self.metodo = tk.StringVar(value="ShellSort")
        metodos = [("ShellSort", "ShellSort"), ("Quicksort", "Quicksort"), 
                   ("Heapsort", "Heapsort"), ("RadixSort", "Radix")]
        
        for i, (text, val) in enumerate(metodos):
            ttk.Radiobutton(metodo_frame, text=text, variable=self.metodo, 
                           value=val).grid(row=0, column=i, padx=10)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Ordenar", command=self.ordenar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reiniciar", command=self.reiniciar).pack(side=tk.LEFT, padx=5)
        
        # Navegación
        self.nav_frame = ttk.Frame(main_frame)
        ttk.Button(self.nav_frame, text="◀", command=self.paso_anterior, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.nav_frame, text="▶", command=self.paso_siguiente, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.nav_frame, text="⟪", command=self.ir_inicio, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.nav_frame, text="⟫", command=self.ir_fin, width=3).pack(side=tk.LEFT, padx=2)
        self.step_label = ttk.Label(self.nav_frame, text="")
        self.step_label.pack(side=tk.LEFT, padx=10)
        
        # Gráfico
        self.figure = plt.Figure(figsize=(9, 4), facecolor='#1e1e2e')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#2a2a3e')
        self.canvas = FigureCanvasTkAgg(self.figure, main_frame)
        
        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 10))
        self.status_label.pack(pady=5)
    
    def generar_campos(self):
        for widget in self.numeros_frame.winfo_children():
            widget.destroy()
        
        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0 or cantidad > 100:
                messagebox.showerror("Error", "Cantidad entre 1 y 100")
                return
            
            self.campos = []
            for i in range(cantidad):
                ttk.Label(self.numeros_frame, text=f"{i+1}:").grid(row=i//15, column=(i%15)*2, padx=1)
                entry = ttk.Entry(self.numeros_frame, width=6)
                entry.grid(row=i//15, column=(i%15)*2+1, padx=1)
                entry.insert(0, str(np.random.randint(1, 100)))
                self.campos.append(entry)
        except:
            messagebox.showerror("Error", "Ingrese un número válido")
    
    def obtener_datos(self):
        datos = []
        for entry in self.campos:
            try:
                datos.append(int(entry.get()))
            except:
                messagebox.showerror("Error", "Todos los campos deben ser números")
                return None
        return datos
    
    def ordenar(self):
        datos = self.obtener_datos()
        if not datos:
            return
        
        self.datos = datos.copy()
        self.historial = []
        
        metodo = self.metodo.get()
        if metodo == "ShellSort":
            self.shellsort(datos.copy())
        elif metodo == "Quicksort":
            self.quicksort(datos.copy())
        elif metodo == "Heapsort":
            self.heapsort(datos.copy())
        elif metodo == "Radix":
            self.radixsort(datos.copy())
        
        self.paso_actual = 0
        self.nav_frame.pack(fill=tk.X, pady=5)
        self.canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)
        self.mostrar_grafico()
        self.actualizar_info()
    
    def shellsort(self, arr):
        self.historial.append({'datos': arr.copy(), 'msg': f"Inicio: {arr}"})
        n = len(arr)
        gap = n // 2
        
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j-gap] > temp:
                    arr[j] = arr[j-gap]
                    j -= gap
                arr[j] = temp
                self.historial.append({'datos': arr.copy(), 'msg': f"Gap={gap}, insertando {temp}"})
            gap //= 2
        self.historial.append({'datos': arr.copy(), 'msg': f"Completado: {arr}"})
    
    def quicksort(self, arr, low=0, high=None):
        if high is None:
            high = len(arr)-1
            self.historial.append({'datos': arr.copy(), 'msg': f"Inicio: {arr}"})
        
        if low < high:
            pi = self.particion(arr, low, high)
            self.quicksort(arr, low, pi-1)
            self.quicksort(arr, pi+1, high)
        
        if low == 0 and high == len(arr)-1:
            self.historial.append({'datos': arr.copy(), 'msg': f"Completado: {arr}"})
    
    def particion(self, arr, low, high):
        pivote = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivote:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.historial.append({'datos': arr.copy(), 'msg': f"Pivote={pivote}, intercambio {arr[i]} y {arr[j]}"})
        arr[i+1], arr[high] = arr[high], arr[i+1]
        self.historial.append({'datos': arr.copy(), 'msg': f"Pivote {pivote} en posición {i+1}"})
        return i+1
    
    def heapsort(self, arr):
        self.historial.append({'datos': arr.copy(), 'msg': f"Inicio: {arr}"})
        n = len(arr)
        
        for i in range(n//2-1, -1, -1):
            self.heapify(arr, n, i)
        
        for i in range(n-1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self.historial.append({'datos': arr.copy(), 'msg': f"Máximo {arr[i]} a posición {i}"})
            self.heapify(arr, i, 0)
        
        self.historial.append({'datos': arr.copy(), 'msg': f"Completado: {arr}"})
    
    def heapify(self, arr, n, i):
        mayor = i
        izq = 2*i+1
        der = 2*i+2
        
        if izq < n and arr[izq] > arr[mayor]:
            mayor = izq
        if der < n and arr[der] > arr[mayor]:
            mayor = der
        
        if mayor != i:
            arr[i], arr[mayor] = arr[mayor], arr[i]
            self.historial.append({'datos': arr.copy(), 'msg': f"Heapify: intercambio {arr[i]} y {arr[mayor]}"})
            self.heapify(arr, n, mayor)
    
    def radixsort(self, arr):
        self.historial.append({'datos': arr.copy(), 'msg': f"Inicio: {arr}"})
        max_val = max(arr)
        exp = 1
        
        while max_val // exp > 0:
            self.counting_sort(arr, exp)
            exp *= 10
        
        self.historial.append({'datos': arr.copy(), 'msg': f"Completado: {arr}"})
    
    def counting_sort(self, arr, exp):
        n = len(arr)
        output = [0]*n
        count = [0]*10
        
        for i in range(n):
            idx = (arr[i]//exp)%10
            count[idx] += 1
        
        for i in range(1,10):
            count[i] += count[i-1]
        
        for i in range(n-1,-1,-1):
            idx = (arr[i]//exp)%10
            output[count[idx]-1] = arr[i]
            count[idx] -= 1
        
        for i in range(n):
            arr[i] = output[i]
        
        self.historial.append({'datos': arr.copy(), 'msg': f"Ordenado por dígito {exp}: {arr}"})
    
    def mostrar_grafico(self):
        if len(self.datos) > 50:
            return
        
        self.ax.clear()
        datos = self.historial[self.paso_actual]['datos']
        
        # Colores degradados según valor
        norm = plt.Normalize(min(datos), max(datos))
        colores = plt.cm.viridis(norm(datos))
        
        bars = self.ax.bar(range(len(datos)), datos, color=colores, edgecolor='white', linewidth=0.5)
        self.ax.set_xticks([])
        self.ax.set_ylabel('Valor', color='white')
        self.ax.tick_params(colors='white')
        self.ax.set_title(f'{self.metodo.get()} - Paso {self.paso_actual}', color='white', fontsize=12, fontweight='bold')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        
        # Valores sobre las barras
        if len(datos) <= 30:
            for bar, val in zip(bars, datos):
                self.ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+max(datos)*0.02,
                           str(val), ha='center', va='bottom', fontsize=8, color='white')
        
        self.canvas.draw()
    
    def actualizar_info(self):
        total = len(self.historial)-1
        self.step_label.config(text=f"{self.paso_actual}/{total}")
        self.status_label.config(text=self.historial[self.paso_actual]['msg'])
        self.mostrar_grafico()
    
    def paso_siguiente(self):
        if self.paso_actual < len(self.historial)-1:
            self.paso_actual += 1
            self.actualizar_info()
    
    def paso_anterior(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.actualizar_info()
    
    def ir_inicio(self):
        self.paso_actual = 0
        self.actualizar_info()
    
    def ir_fin(self):
        self.paso_actual = len(self.historial)-1
        self.actualizar_info()
    
    def reiniciar(self):
        self.datos = []
        self.historial = []
        self.nav_frame.pack_forget()
        self.canvas.get_tk_widget().pack_forget()
        self.status_label.config(text="")
        messagebox.showinfo("Reiniciar", "Listo para nuevos datos")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenamientoApp(root)
    root.mainloop()