import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from collections import deque
import threading
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Tarea:
    def __init__(self, id_tarea, prioridad, descripcion):
        self.id = id_tarea
        self.prioridad = prioridad
        self.descripcion = descripcion
        self.tiempo_ejecucion = random.uniform(0.5, 2.0)
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.estado = "Pendiente"
    
    def __str__(self):
        return f"T{self.id:03d}"

class SimuladorTareasProfesional:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Tareas Enterprise - Simulador de Colas Prioritarias")
        self.root.geometry("1400x900")
        
        # Configurar estilo profesional
        self.setup_styles()
        
        # Estructuras de datos
        self.cola_normal = deque()
        self.bicola_critica = deque()
        self.tareas_ejecutadas = []
        self.contador_tareas = 0
        self.ejecutando = False
        self.tiempo_inicio = None
        
        self.setup_ui()
        self.actualizar_tiempo()
        
    def setup_styles(self):
        """Configurar estilos profesionales"""
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Colores corporativos
        self.colors = {
            'primary': '#2c3e50',      # Azul oscuro corporativo
            'secondary': '#34495e',     # Azul grisáceo
            'accent': '#3498db',         # Azul brillante
            'success': '#27ae60',        # Verde éxito
            'warning': '#e74c3c',         # Rojo advertencia
            'info': '#f39c12',            # Naranja información
            'background': '#ecf0f1',      # Fondo claro
            'text': '#2c3e50',            # Texto oscuro
            'white': '#ffffff'             # Blanco
        }
        
        # Configurar estilos
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'),
                       foreground=self.colors['primary'])
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.colors['secondary'])
        
        style.configure('Stats.TLabel',
                       font=('Segoe UI', 11),
                       foreground=self.colors['text'])
        
        style.configure('Critical.TLabel',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['warning'])
        
        style.configure('Normal.TLabel',
                       font=('Segoe UI', 10),
                       foreground=self.colors['success'])
        
        style.configure('Corporate.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10,
                       background=self.colors['success'])
        
        style.configure('Warning.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10,
                       background=self.colors['warning'])
        
    def setup_ui(self):
        """Configurar interfaz de usuario profesional"""
        
        # Frame principal con padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header con logo corporativo
        self.setup_header(main_container)
        
        # Panel de control superior
        self.setup_control_panel(main_container)
        
        # Panel de métricas en tiempo real
        self.setup_metrics_panel(main_container)
        
        # Panel principal con colas
        self.setup_queues_panel(main_container)
        
        # Panel de gráficas
        self.setup_charts_panel(main_container)
        
        # Panel de log de ejecución
        self.setup_log_panel(main_container)
        
        # Barra de estado profesional
        self.setup_status_bar()
        
    def setup_header(self, parent):
        """Configurar header corporativo"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo y título
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT)
        
        ttk.Label(title_frame, 
                 text="🏢 GESTOR DE TAREAS ENTERPRISE",
                 style='Title.TLabel').pack(anchor=tk.W)
        
        ttk.Label(title_frame,
                 text="Sistema Avanzado de Colas Prioritarias v2.0",
                 font=('Segoe UI', 10),
                 foreground=self.colors['secondary']).pack(anchor=tk.W)
        
        # Reloj y fecha
        clock_frame = ttk.Frame(header_frame)
        clock_frame.pack(side=tk.RIGHT)
        
        self.time_label = ttk.Label(clock_frame,
                                    font=('Segoe UI', 24, 'bold'),
                                    foreground=self.colors['primary'])
        self.time_label.pack()
        
        self.date_label = ttk.Label(clock_frame,
                                   font=('Segoe UI', 10),
                                   foreground=self.colors['secondary'])
        self.date_label.pack()
        
    def setup_control_panel(self, parent):
        """Configurar panel de control profesional"""
        control_frame = ttk.LabelFrame(parent, 
                                       text="Panel de Control",
                                       padding="15")
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botones con iconos
        buttons = [
            ("➕ Agregar Tarea Normal", self.generar_tarea_normal, self.colors['success']),
            ("⚡ Agregar Tarea Crítica", self.generar_tarea_critica, self.colors['warning']),
            ("▶ Iniciar Simulación", self.iniciar_simulacion, self.colors['accent']),
            ("🎲 Generar 15 Tareas", self.generar_15_tareas, self.colors['info']),
            ("🔄 Reiniciar Sistema", self.limpiar_todo, self.colors['secondary']),
            ("⏹ Detener", self.detener_simulacion, self.colors['warning'])
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(control_frame,
                           text=text,
                           command=command,
                           bg=color,
                           fg='white',
                           font=('Segoe UI', 10, 'bold'),
                           padx=15,
                           pady=8,
                           relief=tk.FLAT,
                           cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['secondary']))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
            
    def setup_metrics_panel(self, parent):
        """Configurar panel de métricas en tiempo real"""
        metrics_frame = ttk.LabelFrame(parent, 
                                      text="Métricas en Tiempo Real",
                                      padding="15")
        metrics_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Grid de métricas
        metrics_grid = ttk.Frame(metrics_frame)
        metrics_grid.pack()
        
        # Métricas con diseño profesional
        metrics = [
            ("📊 Tareas Normales", "normal_count", self.colors['success']),
            ("⚠ Tareas Críticas", "critical_count", self.colors['warning']),
            ("✅ Completadas", "completed_count", self.colors['accent']),
            ("⏱ Tiempo Promedio", "avg_wait", self.colors['info']),
            ("⚙ Rendimiento", "throughput", self.colors['primary']),
            ("🎯 Utilización", "utilization", self.colors['secondary'])
        ]
        
        self.metric_labels = {}
        for i, (label, key, color) in enumerate(metrics):
            frame = tk.Frame(metrics_grid, bg=self.colors['white'], relief=tk.RAISED, bd=1)
            frame.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="nsew")
            
            ttk.Label(frame, text=label, style='Header.TLabel').pack(pady=(10, 5))
            
            self.metric_labels[key] = ttk.Label(frame, 
                                                text="0", 
                                                font=('Segoe UI', 20, 'bold'),
                                                foreground=color)
            self.metric_labels[key].pack(pady=(0, 10))
            
    def setup_queues_panel(self, parent):
        """Configurar panel de colas con diseño profesional"""
        queues_frame = ttk.Frame(parent)
        queues_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Cola Normal
        normal_frame = ttk.LabelFrame(queues_frame, 
                                     text="📋 COLA NORMAL (FIFO)",
                                     padding="10")
        normal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas con scrollbar para la cola normal
        self.setup_queue_display(normal_frame, "normal")
        
        # Bicola Crítica
        critical_frame = ttk.LabelFrame(queues_frame, 
                                       text="⚡ COLA CRÍTICA (Bicola - Prioritaria)",
                                       padding="10")
        critical_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas con scrollbar para la cola crítica
        self.setup_queue_display(critical_frame, "critical")
        
    def setup_queue_display(self, parent, queue_type):
        """Configurar display de cola con canvas y scrollbar"""
        # Canvas para scroll
        canvas = tk.Canvas(parent, bg=self.colors['white'], height=200)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        
        # Frame interior para los items
        inner_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configurar el canvas
        canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        # Bindings para el scroll
        def configure_inner_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        inner_frame.bind("<Configure>", configure_inner_frame)
        
        # Empaquetar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Guardar referencias
        if queue_type == "normal":
            self.normal_queue_frame = inner_frame
            self.normal_canvas = canvas
        else:
            self.critical_queue_frame = inner_frame
            self.critical_canvas = canvas
            
    def setup_charts_panel(self, parent):
        """Configurar panel de gráficas"""
        charts_frame = ttk.LabelFrame(parent, 
                                     text="Gráficas de Rendimiento",
                                     padding="10")
        charts_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Crear figura para gráficas
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 3))
        self.fig.patch.set_facecolor(self.colors['background'])
        
        # Configurar gráficas
        self.setup_charts()
        
        # Embed en tkinter
        self.canvas_chart = FigureCanvasTkAgg(self.fig, charts_frame)
        self.canvas_chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def setup_charts(self):
        """Configurar las gráficas"""
        # Gráfica de distribución
        self.ax1.set_title('Distribución de Tareas', fontweight='bold')
        self.ax1.set_facecolor(self.colors['white'])
        
        # Gráfica de rendimiento
        self.ax2.set_title('Rendimiento del Sistema', fontweight='bold')
        self.ax2.set_facecolor(self.colors['white'])
        self.ax2.set_xlabel('Tiempo')
        self.ax2.set_ylabel('Tareas Completadas')
        
        # Datos para gráfica de rendimiento
        self.performance_data = deque(maxlen=20)
        
    def setup_log_panel(self, parent):
        """Configurar panel de log profesional"""
        log_frame = ttk.LabelFrame(parent, 
                                  text="Registro de Ejecución",
                                  padding="10")
        log_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Text widget con scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(text_frame,
                                height=6,
                                font=('Consolas', 9),
                                bg=self.colors['white'],
                                fg=self.colors['text'],
                                wrap=tk.WORD)
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", 
                                 command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tags para colorear logs
        self.log_text.tag_config("info", foreground=self.colors['accent'])
        self.log_text.tag_config("success", foreground=self.colors['success'])
        self.log_text.tag_config("warning", foreground=self.colors['warning'])
        self.log_text.tag_config("critical", foreground=self.colors['warning'], font=('Consolas', 9, 'bold'))
        
    def setup_status_bar(self):
        """Configurar barra de estado profesional"""
        status_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(status_frame,
                                     text="✅ Sistema listo | Gestor de Tareas Enterprise v2.0",
                                     bg=self.colors['secondary'],
                                     fg='white',
                                     font=('Segoe UI', 9))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.system_status = tk.Label(status_frame,
                                      text="● EN LÍNEA",
                                      bg=self.colors['secondary'],
                                      fg=self.colors['success'],
                                      font=('Segoe UI', 9, 'bold'))
        self.system_status.pack(side=tk.RIGHT, padx=10)
        
    def actualizar_tiempo(self):
        """Actualizar reloj en tiempo real"""
        now = datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%A, %d de %B de %Y"))
        self.root.after(1000, self.actualizar_tiempo)
        
    def generar_tarea_normal(self):
        """Generar tarea normal"""
        self.contador_tareas += 1
        tarea = Tarea(self.contador_tareas, "Normal", f"Tarea Estándar #{self.contador_tareas}")
        self.cola_normal.append(tarea)
        self.actualizar_interfaz()
        self.agregar_log(f"📥 Tarea normal {tarea} agregada a la cola", "info")
        
    def generar_tarea_critica(self):
        """Generar tarea crítica"""
        self.contador_tareas += 1
        tarea = Tarea(self.contador_tareas, "Crítica", f"Tarea Crítica #{self.contador_tareas}")
        self.bicola_critica.appendleft(tarea)
        self.actualizar_interfaz()
        self.agregar_log(f"⚡ Tarea CRÍTICA {tarea} agregada a la cola prioritaria", "critical")
        
    def generar_15_tareas(self):
        """Generar 15 tareas automáticamente"""
        for i in range(15):
            self.contador_tareas += 1
            if random.random() < 0.3:
                tarea = Tarea(self.contador_tareas, "Crítica", f"Tarea Crítica #{self.contador_tareas}")
                self.bicola_critica.appendleft(tarea)
            else:
                tarea = Tarea(self.contador_tareas, "Normal", f"Tarea Estándar #{self.contador_tareas}")
                self.cola_normal.append(tarea)
        
        self.actualizar_interfaz()
        self.agregar_log("🎲 15 tareas generadas automáticamente", "success")
        
    def iniciar_simulacion(self):
        """Iniciar simulación"""
        if self.ejecutando:
            return
            
        if not self.cola_normal and not self.bicola_critica:
            self.agregar_log("⚠ No hay tareas para ejecutar", "warning")
            return
            
        self.ejecutando = True
        self.tiempo_inicio = time.time()
        self.system_status.config(text="● EJECUTANDO", fg=self.colors['warning'])
        self.agregar_log("▶ Simulación iniciada - Procesando tareas...", "info")
        
        thread = threading.Thread(target=self.ejecutar_tareas)
        thread.daemon = True
        thread.start()
        
    def ejecutar_tareas(self):
        """Ejecutar tareas en orden de prioridad"""
        while self.ejecutando and (self.bicola_critica or self.cola_normal):
            if self.bicola_critica:
                tarea = self.bicola_critica.popleft()
                self.root.after(0, lambda t=tarea: self.ejecutar_tarea(t, "critical"))
                time.sleep(tarea.tiempo_ejecucion)
            elif self.cola_normal:
                tarea = self.cola_normal.popleft()
                self.root.after(0, lambda t=tarea: self.ejecutar_tarea(t, "normal"))
                time.sleep(tarea.tiempo_ejecucion)
        
        if self.ejecutando:
            self.root.after(0, self.finalizar_simulacion)
            
    def ejecutar_tarea(self, tarea, tipo):
        """Ejecutar una tarea específica"""
        tarea.estado = "Completada"
        self.tareas_ejecutadas.append(tarea)
        
        # Actualizar gráfica de rendimiento
        self.performance_data.append(len(self.tareas_ejecutadas))
        self.actualizar_graficas()
        
        # Log de ejecución
        if tipo == "critical":
            self.agregar_log(f"⚡ EJECUTADA: {tarea} (Crítica) - Tiempo: {tarea.tiempo_ejecucion:.2f}s", "critical")
        else:
            self.agregar_log(f"✅ EJECUTADA: {tarea} (Normal) - Tiempo: {tarea.tiempo_ejecucion:.2f}s", "success")
        
        self.actualizar_interfaz()
        
    def finalizar_simulacion(self):
        """Finalizar simulación"""
        self.ejecutando = False
        tiempo_total = time.time() - self.tiempo_inicio if self.tiempo_inicio else 0
        self.system_status.config(text="● EN LÍNEA", fg=self.colors['success'])
        self.agregar_log(f"✅ Simulación completada - Tiempo total: {tiempo_total:.2f}s", "success")
        
    def detener_simulacion(self):
        """Detener simulación"""
        self.ejecutando = False
        self.system_status.config(text="● DETENIDO", fg=self.colors['warning'])
        self.agregar_log("⏹ Simulación detenida por el usuario", "warning")
        
    def limpiar_todo(self):
        """Limpiar todo el sistema"""
        self.cola_normal.clear()
        self.bicola_critica.clear()
        self.tareas_ejecutadas.clear()
        self.contador_tareas = 0
        self.ejecutando = False
        self.performance_data.clear()
        self.system_status.config(text="● EN LÍNEA", fg=self.colors['success'])
        self.actualizar_interfaz()
        self.log_text.delete(1.0, tk.END)
        self.actualizar_graficas()
        self.agregar_log("🔄 Sistema reiniciado correctamente", "info")
        
    def actualizar_interfaz(self):
        """Actualizar toda la interfaz"""
        self.actualizar_colas()
        self.actualizar_metricas()
        self.canvas_chart.draw_idle()
        
    def actualizar_colas(self):
        """Actualizar visualización de las colas"""
        # Limpiar frames
        for widget in self.normal_queue_frame.winfo_children():
            widget.destroy()
        for widget in self.critical_queue_frame.winfo_children():
            widget.destroy()
        
        # Mostrar tareas normales
        for i, tarea in enumerate(self.cola_normal):
            self.crear_tarea_widget(self.normal_queue_frame, tarea, i, "normal")
            
        # Mostrar tareas críticas
        for i, tarea in enumerate(self.bicola_critica):
            self.crear_tarea_widget(self.critical_queue_frame, tarea, i, "critical")
            
    def crear_tarea_widget(self, parent, tarea, index, tipo):
        """Crear widget para una tarea"""
        color = self.colors['warning'] if tipo == "critical" else self.colors['success']
        
        frame = tk.Frame(parent,
                        bg=self.colors['white'],
                        relief=tk.RAISED,
                        bd=1,
                        padx=10,
                        pady=5)
        frame.pack(fill=tk.X, pady=2)
        
        # Icono según tipo
        icon = "⚡" if tipo == "critical" else "📋"
        
        tk.Label(frame,
                text=f"{icon} {tarea}",
                bg=self.colors['white'],
                fg=color,
                font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        tk.Label(frame,
                text=f"[{tarea.tiempo_ejecucion:.1f}s]",
                bg=self.colors['white'],
                fg=self.colors['secondary'],
                font=('Segoe UI', 9)).pack(side=tk.RIGHT)
        
    def actualizar_metricas(self):
        """Actualizar métricas en tiempo real"""
        self.metric_labels['normal_count'].config(text=str(len(self.cola_normal)))
        self.metric_labels['critical_count'].config(text=str(len(self.bicola_critica)))
        self.metric_labels['completed_count'].config(text=str(len(self.tareas_ejecutadas)))
        
        # Calcular tiempo promedio de espera
        if self.tareas_ejecutadas:
            avg_wait = np.mean([t.tiempo_ejecucion for t in self.tareas_ejecutadas])
            self.metric_labels['avg_wait'].config(text=f"{avg_wait:.2f}s")
        
        # Calcular rendimiento (throughput)
        if self.tiempo_inicio and self.ejecutando:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            if tiempo_transcurrido > 0:
                throughput = len(self.tareas_ejecutadas) / tiempo_transcurrido
                self.metric_labels['throughput'].config(text=f"{throughput:.2f}/s")
        
        # Calcular utilización
        total_tasks = len(self.tareas_ejecutadas) + len(self.cola_normal) + len(self.bicola_critica)
        if total_tasks > 0:
            utilization = (len(self.tareas_ejecutadas) / total_tasks) * 100
            self.metric_labels['utilization'].config(text=f"{utilization:.1f}%")
            
    def actualizar_graficas(self):
        """Actualizar gráficas"""
        # Gráfica de distribución
        self.ax1.clear()
        labels = ['Normales', 'Críticas', 'Completadas']
        values = [len(self.cola_normal), len(self.bicola_critica), len(self.tareas_ejecutadas)]
        colors = [self.colors['success'], self.colors['warning'], self.colors['accent']]
        
        bars = self.ax1.bar(labels, values, color=colors)
        self.ax1.set_title('Distribución de Tareas', fontweight='bold', pad=10)
        
        # Añadir valores en las barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2., height,
                         f'{value}', ha='center', va='bottom')
        
        # Gráfica de rendimiento
        self.ax2.clear()
        if self.performance_data:
            self.ax2.plot(list(range(len(self.performance_data))), 
                         list(self.performance_data),
                         color=self.colors['accent'],
                         linewidth=2,
                         marker='o',
                         markersize=4)
        self.ax2.set_title('Rendimiento del Sistema', fontweight='bold', pad=10)
        self.ax2.set_xlabel('Tiempo')
        self.ax2.set_ylabel('Tareas Completadas')
        self.ax2.grid(True, alpha=0.3)
        
        self.fig.tight_layout()
        
    def agregar_log(self, mensaje, tipo="info"):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensaje}\n"
        
        self.log_text.insert(tk.END, log_entry, tipo)
        self.log_text.see(tk.END)
        
        # Actualizar barra de estado
        self.status_label.config(text=f"📌 {mensaje}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configurar icono de la aplicación (opcional)
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
    
    app = SimuladorTareasProfesional(root)
    
    # Manejar cierre de aplicación
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Desea salir del Gestor de Tareas Enterprise?"):
            app.detener_simulacion()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()