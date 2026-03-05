import tkinter as tk
from tkinter import messagebox, ttk
import random

class PilaVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Pila (Stack)")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Configuración de la pila
        self.pila = []
        self.capacidad_maxima = 8
        self.colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
                       '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="Visualización de Pila (Stack)", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Frame para controles
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Entrada de valor
        ttk.Label(control_frame, text="Valor:").grid(row=0, column=0, padx=5)
        self.valor_entry = ttk.Entry(control_frame, width=15)
        self.valor_entry.grid(row=0, column=1, padx=5)
        self.valor_entry.bind('<Return>', lambda e: self.push())
        
        # Botones
        ttk.Button(control_frame, text="Push (Agregar)", 
                  command=self.push).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Pop (Quitar)", 
                  command=self.pop).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Peek (Ver tope)", 
                  command=self.peek).grid(row=0, column=4, padx=5)
        ttk.Button(control_frame, text="Vaciar Pila", 
                  command=self.vaciar).grid(row=0, column=5, padx=5)
        ttk.Button(control_frame, text="Ejemplo Auto", 
                  command=self.ejemplo_auto).grid(row=0, column=6, padx=5)
        
        # Información de la pila
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.info_label = ttk.Label(info_frame, text="Tamaño: 0 | Capacidad: 8", 
                                    font=('Arial', 10))
        self.info_label.grid(row=0, column=0, padx=10)
        
        self.tope_label = ttk.Label(info_frame, text="Tope: Vacío", 
                                    font=('Arial', 10))
        self.tope_label.grid(row=0, column=1, padx=10)
        
        # Canvas para dibujar la pila
        canvas_frame = ttk.LabelFrame(main_frame, text="Visualización de la Pila", padding="10")
        canvas_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, width=600, height=350, bg='white', 
                               highlightthickness=1, highlightbackground='gray')
        self.canvas.grid(row=0, column=0)
        
        # Etiqueta de instrucciones
        instrucciones = ttk.Label(main_frame, 
                                 text="LIFO (Last In, First Out) - El último en entrar es el primero en salir",
                                 font=('Arial', 9, 'italic'))
        instrucciones.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Dibujar estructura inicial
        self.dibujar_pila()
        
    def dibujar_pila(self):
        self.canvas.delete("all")
        
        # Dibujar el contenedor de la pila (estructura fija)
        x_inicio = 250
        y_inicio = 50
        ancho = 120
        alto_elemento = 30
        
        # Dibujar el marco de la pila
        self.canvas.create_rectangle(x_inicio-10, y_inicio-10, 
                                     x_inicio+ancho+10, y_inicio+self.capacidad_maxima*alto_elemento+10,
                                     outline='#333', width=2, dash=(2, 2))
        
        # Dibujar las líneas divisorias de capacidad
        for i in range(self.capacidad_maxima + 1):
            y = y_inicio + i * alto_elemento
            self.canvas.create_line(x_inicio-5, y, x_inicio+ancho+5, y, 
                                   fill='#ddd', width=1, dash=(1, 3))
        
        # Dibujar los elementos de la pila
        for i, valor in enumerate(self.pila):
            y_pos = y_inicio + (self.capacidad_maxima - 1 - i) * alto_elemento
            color = self.colores[i % len(self.colores)]
            
            # Rectángulo del elemento
            self.canvas.create_rectangle(x_inicio, y_pos, 
                                        x_inicio+ancho, y_pos+alto_elemento,
                                        fill=color, outline='#333', width=2)
            
            # Texto del valor
            self.canvas.create_text(x_inicio + ancho/2, y_pos + alto_elemento/2,
                                   text=str(valor), font=('Arial', 11, 'bold'))
            
            # Indicador de posición
            if i == len(self.pila) - 1:  # Tope
                self.canvas.create_text(x_inicio + ancho + 30, y_pos + alto_elemento/2,
                                       text="← TOPE", font=('Arial', 10, 'bold'), 
                                       fill='#FF6B6B', anchor='w')
        
        # Dibujar indicador de fondo (base)
        self.canvas.create_text(x_inicio + ancho/2, y_inicio + self.capacidad_maxima*alto_elemento + 20,
                               text="BASE", font=('Arial', 9), fill='#666')
        
        # Actualizar información
        self.actualizar_info()
        
    def actualizar_info(self):
        self.info_label.config(text=f"Tamaño: {len(self.pila)} | Capacidad: {self.capacidad_maxima}")
        if self.pila:
            self.tope_label.config(text=f"Tope: {self.pila[-1]}")
        else:
            self.tope_label.config(text="Tope: Vacío")
            
    def push(self):
        valor = self.valor_entry.get().strip()
        
        if not valor:
            messagebox.showwarning("Advertencia", "Por favor ingresa un valor")
            return
            
        if len(self.pila) >= self.capacidad_maxima:
            messagebox.showerror("Error", "La pila está llena (Stack Overflow)")
            return
            
        self.pila.append(valor)
        self.valor_entry.delete(0, tk.END)
        self.dibujar_pila()
        
        # Animación simple
        self.root.update()
        
    def pop(self):
        if not self.pila:
            messagebox.showwarning("Advertencia", "La pila está vacía (Stack Underflow)")
            return
            
        valor = self.pila.pop()
        messagebox.showinfo("Pop", f"Se eliminó el elemento: {valor}")
        self.dibujar_pila()
        
    def peek(self):
        if not self.pila:
            messagebox.showinfo("Peek", "La pila está vacía")
        else:
            messagebox.showinfo("Peek", f"El elemento en el tope es: {self.pila[-1]}")
            
    def vaciar(self):
        if not self.pila:
            messagebox.showinfo("Info", "La pila ya está vacía")
            return
            
        if messagebox.askyesno("Confirmar", "¿Estás seguro de vaciar la pila?"):
            self.pila.clear()
            self.dibujar_pila()
            messagebox.showinfo("Info", "Pila vaciada exitosamente")
            
    def ejemplo_auto(self):
        """Agrega elementos de ejemplo automáticamente"""
        elementos_ejemplo = ["A", "B", "C", "D", "E"]
        for elem in elementos_ejemplo:
            if len(self.pila) < self.capacidad_maxima:
                self.pila.append(elem)
            else:
                break
        self.dibujar_pila()
        messagebox.showinfo("Ejemplo", "Se agregaron elementos de ejemplo")

class PilaApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # Configurar estilo
        self.setup_style()
        
        # Crear aplicación
        self.app = PilaVisual(self.root)
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)
        
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('TButton', padding=6, relief="flat", background="#4CAF50")
        style.configure('TLabel', padding=3)
        style.configure('TLabelframe', padding=5)
        
    def cerrar(self):
        if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.destroy()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PilaApp()
    app.run()