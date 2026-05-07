import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import time
import os
import threading

class VisualSorting:
    """Clase principal con los algoritmos de ordenamiento"""
    
    @staticmethod
    def intercalacion_sort(arr, paso_callback=None):
        """Método de Intercalación (Insertion Sort)"""
        n = len(arr)
        pasos = []
        arr_temp = arr.copy()
        
        for i in range(1, n):
            key = arr_temp[i]
            j = i - 1
            while j >= 0 and arr_temp[j] > key:
                arr_temp[j + 1] = arr_temp[j]
                j -= 1
                paso = arr_temp.copy()
                pasos.append(paso)
                if paso_callback:
                    paso_callback(paso)
            arr_temp[j + 1] = key
            paso = arr_temp.copy()
            pasos.append(paso)
            if paso_callback:
                paso_callback(paso)
        
        return pasos, arr_temp
    
    @staticmethod
    def mezcla_directa_sort(arr, paso_callback=None):
        """Método de Mezcla Directa (Bubble Sort)"""
        n = len(arr)
        pasos = []
        arr_temp = arr.copy()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr_temp[j] > arr_temp[j + 1]:
                    arr_temp[j], arr_temp[j + 1] = arr_temp[j + 1], arr_temp[j]
                    paso = arr_temp.copy()
                    pasos.append(paso)
                    if paso_callback:
                        paso_callback(paso)
        
        return pasos, arr_temp
    
    @staticmethod
    def mezcla_equilibrada_sort(arr, paso_callback=None):
        """Método de Mezcla Equilibrada (Merge Sort)"""
        pasos = []
        
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
        
        def merge_sort(arr, depth=0):
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = merge_sort(arr[:mid], depth + 1)
            right = merge_sort(arr[mid:], depth + 1)
            
            merged = merge(left, right)
            paso = merged.copy()
            pasos.append(paso)
            if paso_callback:
                paso_callback(paso)
            return merged
        
        resultado = merge_sort(arr.copy())
        return pasos, resultado

class OrdenamientoGUI:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Visualizador de Algoritmos de Ordenamiento")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg='#f0f0f0')
        
        self.datos_actuales = []
        self.animacion_activa = False
        self.paso_actual = 0
        self.pasos_intercalacion = []
        self.pasos_mezcla_directa = []
        self.pasos_mezcla_equilibrada = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame superior para controles
        frame_superior = tk.Frame(self.ventana, bg='#f0f0f0', pady=10)
        frame_superior.pack(fill=tk.X, padx=10)
        
        # Título
        titulo = tk.Label(frame_superior, text="MÉTODOS DE ORDENAMIENTO", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=5)
        
        # Frame para botones
        frame_botones = tk.Frame(frame_superior, bg='#f0f0f0')
        frame_botones.pack(pady=5)
        
        botones = [
            ("📊 Datos Aleatorios", self.datos_aleatorios),
            ("✏️ Ingresar Manual", self.ingresar_manual),
            ("📁 Cargar Archivo", self.cargar_archivo),
            ("▶️ Iniciar Animación", self.iniciar_animacion),
            ("⏹️ Detener", self.detener_animacion),
            ("💾 Guardar Resultados", self.guardar_resultados),
            ("📈 Comparar Rendimiento", self.comparar_rendimiento)
        ]
        
        for texto, comando in botones:
            btn = tk.Button(frame_botones, text=texto, command=comando,
                          font=('Arial', 10), bg='#3498db', fg='white',
                          padx=10, pady=5, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        
        # Frame para mostrar datos actuales
        frame_datos = tk.Frame(self.ventana, bg='white', relief=tk.RAISED, bd=1)
        frame_datos.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_datos, text="Datos Actuales:", font=('Arial', 11, 'bold'),
                bg='white').pack(side=tk.LEFT, padx=10, pady=5)
        
        self.label_datos = tk.Label(frame_datos, text="Sin datos", font=('Arial', 10),
                                   bg='white', fg='#2c3e50')
        self.label_datos.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Canvas para visualización
        self.frame_canvas = tk.Frame(self.ventana, bg='white')
        self.frame_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Crear 3 áreas para los algoritmos
        self.canvas_intercalacion = tk.Canvas(self.frame_canvas, bg='white', 
                                              relief=tk.SUNKEN, bd=2)
        self.canvas_mezcla_directa = tk.Canvas(self.frame_canvas, bg='white',
                                               relief=tk.SUNKEN, bd=2)
        self.canvas_mezcla_equilibrada = tk.Canvas(self.frame_canvas, bg='white',
                                                   relief=tk.SUNKEN, bd=2)
        
        self.canvas_intercalacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_mezcla_directa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_mezcla_equilibrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Títulos de los canvas
        self.canvas_intercalacion.create_text(10, 20, anchor='nw', 
                                             text="Intercalación (Insertion Sort)",
                                             font=('Arial', 12, 'bold'), fill='#e74c3c')
        self.canvas_mezcla_directa.create_text(10, 20, anchor='nw',
                                              text="Mezcla Directa (Bubble Sort)",
                                              font=('Arial', 12, 'bold'), fill='#27ae60')
        self.canvas_mezcla_equilibrada.create_text(10, 20, anchor='nw',
                                                  text="Mezcla Equilibrada (Merge Sort)",
                                                  font=('Arial', 12, 'bold'), fill='#3498db')
        
        # Frame inferior para información
        frame_inferior = tk.Frame(self.ventana, bg='#f0f0f0', height=80)
        frame_inferior.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.label_info = tk.Label(frame_inferior, text="Listo", 
                                  font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
        self.label_info.pack(pady=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(frame_inferior, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
    
    def dibujar_barras(self, canvas, datos, titulo_y=40):
        """Dibuja gráfico de barras en el canvas"""
        canvas.delete("barra")
        canvas.delete("texto")
        
        if not datos:
            return
        
        ancho = canvas.winfo_width()
        if ancho < 100:
            ancho = 400
        
        alto = canvas.winfo_height() - titulo_y - 20
        if alto < 100:
            alto = 300
        
        n = len(datos)
        if n == 0:
            return
        
        ancho_barra = max(10, (ancho - 20) / n - 2)
        max_valor = max(datos) if datos else 1
        
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
                   '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
        
        for i, valor in enumerate(datos):
            x0 = 10 + i * (ancho_barra + 2)
            y0 = alto + titulo_y - (valor / max_valor) * alto
            x1 = x0 + ancho_barra
            y1 = alto + titulo_y
            
            color = colores[i % len(colores)]
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="barra")
            
            # Mostrar valor sobre la barra si el canvas es suficientemente grande
            if ancho_barra > 15 and n < 20:
                canvas.create_text(x0 + ancho_barra/2, y0 - 5, text=str(valor),
                                  font=('Arial', 8), tags="texto")
    
    def actualizar_visualizacion(self):
        """Actualiza todos los canvases con los datos actuales"""
        if self.datos_actuales:
            max_valor = max(self.datos_actuales) if self.datos_actuales else 100
            
            # Redibujar todos los canvases
            for canvas in [self.canvas_intercalacion, self.canvas_mezcla_directa, 
                          self.canvas_mezcla_equilibrada]:
                self.dibujar_barras(canvas, self.datos_actuales)
    
    def datos_aleatorios(self):
        """Genera datos aleatorios"""
        try:
            n = simpledialog.askinteger("Cantidad", "Número de elementos (5-30):", 
                                       minvalue=5, maxvalue=30, initialvalue=15)
            if n:
                self.datos_actuales = [random.randint(1, 100) for _ in range(n)]
                self.label_datos.config(text=str(self.datos_actuales))
                self.actualizar_visualizacion()
                self.label_info.config(text=f"✓ Generados {n} datos aleatorios")
        except:
            pass
    
    def ingresar_manual(self):
        """Permite ingresar datos manualmente"""
        dialog = tk.Toplevel(self.ventana)
        dialog.title("Ingresar Datos")
        dialog.geometry("400x200")
        dialog.configure(bg='#f0f0f0')
        
        tk.Label(dialog, text="Ingrese números separados por espacios o comas:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(pady=10)
        
        entry = tk.Entry(dialog, width=50, font=('Arial', 10))
        entry.pack(pady=10)
        
        def aceptar():
            texto = entry.get()
            texto = texto.replace(',', ' ')
            numeros = texto.split()
            try:
                datos = [int(n) for n in numeros]
                if 1 <= len(datos) <= 30:
                    self.datos_actuales = datos
                    self.label_datos.config(text=str(self.datos_actuales))
                    self.actualizar_visualizacion()
                    self.label_info.config(text=f"✓ Ingresados {len(datos)} datos manualmente")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Ingrese entre 1 y 30 números")
            except:
                messagebox.showerror("Error", "Ingrese solo números válidos")
        
        tk.Button(dialog, text="Aceptar", command=aceptar, bg='#3498db', 
                 fg='white', padx=20, pady=5).pack(pady=10)
    
    def cargar_archivo(self):
        """Carga datos desde archivo de texto"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'r') as f:
                    contenido = f.read()
                
                # Extraer números
                import re
                numeros = re.findall(r'-?\d+', contenido)
                datos = [int(n) for n in numeros]
                
                if datos:
                    if len(datos) > 50:
                        if not messagebox.askyesno("Advertencia", 
                                                  f"Se encontraron {len(datos)} números. ¿Continuar?"):
                            return
                    
                    self.datos_actuales = datos[:50]  # Limitar a 50 para mejor visualización
                    self.label_datos.config(text=str(self.datos_actuales[:20]) + 
                                           ("..." if len(datos) > 20 else ""))
                    self.actualizar_visualizacion()
                    self.label_info.config(text=f"✓ Cargados {len(self.datos_actuales)} datos desde archivo")
                else:
                    messagebox.showerror("Error", "No se encontraron números en el archivo")
            except Exception as e:
                messagebox.showerror("Error", f"Error al leer archivo: {str(e)}")
    
    def actualizar_paso(self, algoritmo, datos):
        """Callback para actualizar cada paso del algoritmo"""
        if algoritmo == 'intercalacion':
            self.dibujar_barras(self.canvas_intercalacion, datos)
            self.canvas_intercalacion.update()
        elif algoritmo == 'mezcla_directa':
            self.dibujar_barras(self.canvas_mezcla_directa, datos)
            self.canvas_mezcla_directa.update()
        elif algoritmo == 'mezcla_equilibrada':
            self.dibujar_barras(self.canvas_mezcla_equilibrada, datos)
            self.canvas_mezcla_equilibrada.update()
        
        time.sleep(0.05)  # Pequeña pausa para visualización
    
    def ejecutar_animacion(self):
        """Ejecuta la animación de los tres algoritmos"""
        if not self.datos_actuales:
            messagebox.showwarning("Advertencia", "Primero cargue o genere datos")
            return
        
        self.animacion_activa = True
        self.label_info.config(text="🔄 Ejecutando algoritmos...")
        
        # Crear hilos para cada algoritmo
        hilos = []
        
        def ejecutar_intercalacion():
            pasos, resultado = VisualSorting.intercalacion_sort(
                self.datos_actuales, 
                lambda d: self.actualizar_paso('intercalacion', d)
            )
            return resultado
        
        def ejecutar_mezcla_directa():
            pasos, resultado = VisualSorting.mezcla_directa_sort(
                self.datos_actuales,
                lambda d: self.actualizar_paso('mezcla_directa', d)
            )
            return resultado
        
        def ejecutar_mezcla_equilibrada():
            pasos, resultado = VisualSorting.mezcla_equilibrada_sort(
                self.datos_actuales,
                lambda d: self.actualizar_paso('mezcla_equilibrada', d)
            )
            return resultado
        
        # Ejecutar en hilos separados
        hilo1 = threading.Thread(target=ejecutar_intercalacion)
        hilo2 = threading.Thread(target=ejecutar_mezcla_directa)
        hilo3 = threading.Thread(target=ejecutar_mezcla_equilibrada)
        
        hilo1.start()
        hilo2.start()
        hilo3.start()
        
        hilo1.join()
        hilo2.join()
        hilo3.join()
        
        self.label_info.config(text="✓ Animación completada")
        self.animacion_activa = False
    
    def iniciar_animacion(self):
        """Inicia la animación en un hilo separado"""
        if self.animacion_activa:
            messagebox.showwarning("Advertencia", "Ya hay una animación en curso")
            return
        
        if not self.datos_actuales:
            messagebox.showwarning("Advertencia", "Primero cargue o genere datos")
            return
        
        thread = threading.Thread(target=self.ejecutar_animacion)
        thread.daemon = True
        thread.start()
    
    def detener_animacion(self):
        """Detiene la animación actual"""
        self.animacion_activa = False
        self.label_info.config(text="⏹️ Animación detenida")
    
    def guardar_resultados(self):
        """Guarda los resultados en un archivo"""
        if not self.datos_actuales:
            messagebox.showwarning("Advertencia", "No hay datos para guardar")
            return
        
        archivo = filedialog.asksaveasfilename(
            title="Guardar resultados",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            # Calcular resultados
            _, resultado_inter = VisualSorting.intercalacion_sort(self.datos_actuales.copy())
            _, resultado_directa = VisualSorting.mezcla_directa_sort(self.datos_actuales.copy())
            _, resultado_equilibrada = VisualSorting.mezcla_equilibrada_sort(self.datos_actuales.copy())
            
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("RESULTADOS DE ORDENAMIENTO\n")
                f.write("="*60 + "\n\n")
                f.write(f"Datos originales ({len(self.datos_actuales)} elementos):\n")
                f.write(f"{self.datos_actuales}\n\n")
                f.write("Intercalación (Insertion Sort):\n")
                f.write(f"{resultado_inter}\n\n")
                f.write("Mezcla Directa (Bubble Sort):\n")
                f.write(f"{resultado_directa}\n\n")
                f.write("Mezcla Equilibrada (Merge Sort):\n")
                f.write(f"{resultado_equilibrada}\n\n")
                f.write("="*60 + "\n")
            
            self.label_info.config(text=f"✓ Resultados guardados en {os.path.basename(archivo)}")
            messagebox.showinfo("Éxito", "Resultados guardados correctamente")
    
    def comparar_rendimiento(self):
        """Compara el rendimiento de los tres algoritmos"""
        if not self.datos_actuales or len(self.datos_actuales) < 2:
            messagebox.showwarning("Advertencia", 
                                  "Se necesitan al menos 2 elementos para la comparación")
            return
        
        # Medir tiempos
        datos_copy = self.datos_actuales.copy()
        
        start = time.time()
        _, _ = VisualSorting.intercalacion_sort(datos_copy.copy())
        tiempo_inter = time.time() - start
        
        start = time.time()
        _, _ = VisualSorting.mezcla_directa_sort(datos_copy.copy())
        tiempo_directa = time.time() - start
        
        start = time.time()
        _, _ = VisualSorting.mezcla_equilibrada_sort(datos_copy.copy())
        tiempo_equilibrada = time.time() - start
        
        # Mostrar resultados
        resultados = f"""
╔══════════════════════════════════════════════════════╗
║           COMPARACIÓN DE RENDIMIENTO                 ║
╠══════════════════════════════════════════════════════╣
║ Elementos: {len(self.datos_actuales):<46} ║
╠══════════════════════════════════════════════════════╣
║ Intercalación (O(n²)):      {tiempo_inter:.6f} segundos{' ' * (20 - len(f'{tiempo_inter:.6f}'))}║
║ Mezcla Directa (O(n²)):      {tiempo_directa:.6f} segundos{' ' * (20 - len(f'{tiempo_directa:.6f}'))}║
║ Mezcla Equilibrada (O(n log n)): {tiempo_equilibrada:.6f} segundos{' ' * (20 - len(f'{tiempo_equilibrada:.6f}'))}║
╚══════════════════════════════════════════════════════╝
"""
        
        messagebox.showinfo("Rendimiento", resultados)
        self.label_info.config(text="✓ Comparación de rendimiento completada")
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()

# Diálogo simple para entrada de números
class simpledialog:
    @staticmethod
    def askinteger(title, prompt, minvalue=None, maxvalue=None, initialvalue=None):
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.geometry("300x150")
        
        tk.Label(dialog, text=prompt).pack(pady=10)
        
        var = tk.IntVar()
        if initialvalue:
            var.set(initialvalue)
        
        entry = tk.Entry(dialog, textvariable=var)
        entry.pack(pady=5)
        
        resultado = None
        
        def aceptar():
            nonlocal resultado
            try:
                valor = var.get()
                if minvalue is not None and valor < minvalue:
                    messagebox.showerror("Error", f"El valor debe ser >= {minvalue}")
                    return
                if maxvalue is not None and valor > maxvalue:
                    messagebox.showerror("Error", f"El valor debe ser <= {maxvalue}")
                    return
                resultado = valor
                dialog.destroy()
            except:
                messagebox.showerror("Error", "Ingrese un número válido")
        
        tk.Button(dialog, text="Aceptar", command=aceptar).pack(pady=10)
        
        dialog.wait_window()
        return resultado

if __name__ == "__main__":
    app = OrdenamientoGUI()
    app.ejecutar()