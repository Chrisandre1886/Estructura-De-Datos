import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from collections import deque
import threading
from datetime import datetime

class Tarea:
    def __init__(self, id_tarea, prioridad, descripcion):
        self.id = id_tarea
        self.prioridad = prioridad
        self.descripcion = descripcion
        # Tiempos fijos: 2s para normales, 1s para críticas
        self.tiempo_ejecucion = 2.0 if prioridad == "Normal" else 1.0
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.estado = "Pendiente"
        self.hora_fin = None
        self.posicion_original = None
        self.hilo_ejecucion = None  # Para seguimiento del hilo
    
    def __str__(self):
        return f"T{self.id:03d}"

class SimuladorTareasProfesional:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Tareas Enterprise - Simulador de Colas Prioritarias con Procesamiento Paralelo")
        self.root.geometry("1600x900")  # Ajustado para mejor visualización sin gráficas
        
        # Límites para evitar lentitud
        self.max_tareas_visibles = 50  # Límite de tareas visibles en colas
        self.max_log_lines = 100  # Límite de líneas en el log
        self.max_completadas_visibles = 100  # Límite de tareas completadas visibles
        
        # Configurar estilo profesional
        self.setup_styles()
        
        # Estructuras de datos
        self.cola_normal = deque()
        self.bicola_critica = deque()
        self.tareas_ejecutadas = []
        self.tareas_en_ejecucion = []  # Lista de tareas siendo ejecutadas
        self.orden_ejecucion = []  # Lista para almacenar el orden de ejecución
        self.contador_tareas = 0
        self.ejecutando = False
        self.tiempo_inicio = None
        
        # Lock para sincronización de hilos
        self.lock = threading.Lock()
        
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
            'white': '#ffffff',             # Blanco
            'completed_bg': '#f0f9f0',      # Fondo para completadas
            'completed_fg': '#2e7d32',       # Texto para completadas
            'next_up': '#fff3e0',            # Color para "próximas tareas"
            'next_up_fg': '#e65100',           # Texto para "próximas tareas"
            'executing': '#ffd54f',          # Color para tareas en ejecución
            'parallel': '#7e57c2'            # Color para procesamiento paralelo
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
        
        style.configure('NextUp.TLabel',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['next_up_fg'])
        
        style.configure('Parallel.TLabel',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['parallel'])
        
    def setup_ui(self):
        """Configurar interfaz de usuario profesional"""
        
        # Frame principal con padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configurar pesos para que todo se expanda proporcionalmente
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(0, weight=0)  # Header
        main_container.rowconfigure(1, weight=0)  # Control panel
        main_container.rowconfigure(2, weight=0)  # Metrics panel
        main_container.rowconfigure(3, weight=1)  # Content (queues, order, completed)
        main_container.rowconfigure(4, weight=0)  # Log
        main_container.rowconfigure(5, weight=0)  # Status bar
        
        # Header con logo corporativo
        self.setup_header(main_container)
        
        # Panel de control superior
        self.setup_control_panel(main_container)
        
        # Panel de métricas en tiempo real
        self.setup_metrics_panel(main_container)
        
        # Frame para colas, orden de ejecución y tareas completadas (3 columnas)
        content_frame = ttk.Frame(main_container)
        content_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)  # Colas izquierda
        content_frame.columnconfigure(1, weight=1)  # Orden ejecución
        content_frame.columnconfigure(2, weight=1)  # Completadas
        content_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo: Colas (ahora una sola columna con ambas colas)
        queues_frame = ttk.Frame(content_frame)
        queues_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        queues_frame.rowconfigure(0, weight=1)
        queues_frame.rowconfigure(1, weight=1)
        queues_frame.columnconfigure(0, weight=1)
        
        # Cola Normal
        normal_frame = ttk.LabelFrame(queues_frame, 
                                     text="📋 COLA NORMAL (FIFO) - T: 2s",
                                     padding="5")
        normal_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        normal_frame.rowconfigure(0, weight=1)
        normal_frame.columnconfigure(0, weight=1)
        
        # Canvas con scrollbar para la cola normal
        self.setup_queue_display(normal_frame, "normal")
        
        # Bicola Crítica
        critical_frame = ttk.LabelFrame(queues_frame, 
                                       text="⚡ COLA CRÍTICA (Prioritaria) - T: 1s",
                                       padding="5")
        critical_frame.grid(row=1, column=0, sticky="nsew")
        critical_frame.rowconfigure(0, weight=1)
        critical_frame.columnconfigure(0, weight=1)
        
        # Canvas con scrollbar para la cola crítica
        self.setup_queue_display(critical_frame, "critical")
        
        # Panel central: Orden de Ejecución y Tareas en Ejecución
        self.setup_execution_order_panel(content_frame)
        
        # Panel derecho: Tareas Completadas
        self.setup_completed_tasks_panel(content_frame)
        
        # Panel de log de ejecución
        self.setup_log_panel(main_container)
        
        # Barra de estado profesional
        self.setup_status_bar()
        
    def setup_header(self, parent):
        """Configurar header corporativo"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=0)
        
        # Logo y título
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        ttk.Label(title_frame, 
                 text="🏢 GESTOR DE TAREAS ENTERPRISE",
                 style='Title.TLabel').pack(anchor=tk.W)
        
        ttk.Label(title_frame,
                 text="Sistema Avanzado de Colas Prioritarias con Procesamiento Paralelo v4.0",
                 font=('Segoe UI', 10),
                 foreground=self.colors['secondary']).pack(anchor=tk.W)
        
        # Reloj y fecha
        clock_frame = ttk.Frame(header_frame)
        clock_frame.grid(row=0, column=1, sticky="e")
        
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
                                       padding="10")
        control_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # Frame para botones con grid para mejor distribución
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X, expand=True)
        
        # Configurar grid para 6 botones en una fila
        for i in range(6):
            buttons_frame.columnconfigure(i, weight=1)
        
        # Botones con iconos
        buttons = [
            ("➕ Agregar Tarea Normal (2s)", self.generar_tarea_normal, self.colors['success']),
            ("⚡ Agregar Tarea Crítica (1s)", self.generar_tarea_critica, self.colors['warning']),
            ("▶ Iniciar Simulación Paralela", self.iniciar_simulacion, self.colors['accent']),
            ("🎲 Generar 15 Tareas", self.generar_15_tareas, self.colors['info']),
            ("🔄 Reiniciar Sistema", self.limpiar_todo, self.colors['secondary']),
            ("⏹ Detener", self.detener_simulacion, self.colors['warning'])
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(buttons_frame,
                           text=text,
                           command=command,
                           bg=color,
                           fg='white',
                           font=('Segoe UI', 10, 'bold'),
                           padx=10,
                           pady=8,
                           relief=tk.FLAT,
                           cursor='hand2',
                           wraplength=150)  # Wrap text to fit
            btn.grid(row=0, column=i, padx=3, sticky="ew")
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['secondary']))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))
    
    def setup_execution_order_panel(self, parent):
        """Configurar panel de orden de ejecución y tareas en ejecución"""
        # Frame principal para orden y ejecución
        main_order_frame = ttk.Frame(parent)
        main_order_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        main_order_frame.rowconfigure(0, weight=0)  # Tareas en ejecución
        main_order_frame.rowconfigure(1, weight=1)  # Orden de ejecución
        main_order_frame.columnconfigure(0, weight=1)
        
        # Panel de tareas en ejecución
        executing_frame = ttk.LabelFrame(main_order_frame, 
                                        text="⚙ TAREAS EN EJECUCIÓN (Paralelo)",
                                        padding="5")
        executing_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        executing_frame.columnconfigure(0, weight=1)
        
        # Frame para mostrar tareas ejecutándose
        self.executing_container = ttk.Frame(executing_frame)
        self.executing_container.pack(fill=tk.X, expand=True)
        
        self.executing_labels = []
        self.update_executing_display()
        
        # Panel de orden de ejecución
        order_frame = ttk.LabelFrame(main_order_frame, 
                                     text="⏳ ORDEN DE EJECUCIÓN (Próximas Tareas)",
                                     padding="5")
        order_frame.grid(row=1, column=0, sticky="nsew")
        order_frame.rowconfigure(0, weight=1)
        order_frame.columnconfigure(0, weight=1)
        
        # Treeview para mostrar orden de ejecución
        columns = ('Posición', 'ID', 'Prioridad', 'Descripción', 'Tiempo')
        self.order_tree = ttk.Treeview(order_frame, columns=columns, 
                                       show='headings', height=15)
        
        # Configurar columnas
        self.order_tree.heading('Posición', text='#')
        self.order_tree.heading('ID', text='ID')
        self.order_tree.heading('Prioridad', text='Prioridad')
        self.order_tree.heading('Descripción', text='Descripción')
        self.order_tree.heading('Tiempo', text='Tiempo (s)')
        
        # Configurar anchos de columna
        self.order_tree.column('Posición', width=50, anchor='center', minwidth=40)
        self.order_tree.column('ID', width=70, anchor='center', minwidth=60)
        self.order_tree.column('Prioridad', width=90, anchor='center', minwidth=80)
        self.order_tree.column('Descripción', width=200, minwidth=150)
        self.order_tree.column('Tiempo', width=80, anchor='center', minwidth=70)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(order_frame, orient=tk.VERTICAL, 
                                  command=self.order_tree.yview)
        self.order_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar con grid
        self.order_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Etiqueta de información
        self.order_info = ttk.Label(order_frame, 
                                     text="Próxima tarea: -",
                                     font=('Segoe UI', 10, 'bold'),
                                     foreground=self.colors['next_up_fg'])
        self.order_info.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Configurar tags de color
        self.order_tree.tag_configure('critical', background='#ffebee', foreground='#c62828')
        self.order_tree.tag_configure('normal', background='#e8f5e9', foreground='#2e7d32')
        self.order_tree.tag_configure('next', background='#fff3e0', foreground='#e65100', font=('Segoe UI', 10, 'bold'))
        
    def setup_completed_tasks_panel(self, parent):
        """Configurar panel de tareas completadas con límite de visibilidad"""
        completed_frame = ttk.LabelFrame(parent, 
                                        text="✅ TAREAS COMPLETADAS",
                                        padding="5")
        completed_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        completed_frame.rowconfigure(0, weight=1)
        completed_frame.columnconfigure(0, weight=1)
        
        # Treeview para mostrar tareas completadas
        columns = ('ID', 'Prioridad', 'Descripción', 'Tiempo', 'Fin')
        self.completed_tree = ttk.Treeview(completed_frame, columns=columns, 
                                           show='headings', height=20)
        
        # Configurar columnas
        self.completed_tree.heading('ID', text='ID')
        self.completed_tree.heading('Prioridad', text='Prioridad')
        self.completed_tree.heading('Descripción', text='Descripción')
        self.completed_tree.heading('Tiempo', text='Tiempo (s)')
        self.completed_tree.heading('Fin', text='Hora Fin')
        
        # Configurar anchos
        self.completed_tree.column('ID', width=70, anchor='center', minwidth=60)
        self.completed_tree.column('Prioridad', width=90, anchor='center', minwidth=80)
        self.completed_tree.column('Descripción', width=200, minwidth=150)
        self.completed_tree.column('Tiempo', width=80, anchor='center', minwidth=70)
        self.completed_tree.column('Fin', width=90, anchor='center', minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(completed_frame, orient=tk.VERTICAL, 
                                  command=self.completed_tree.yview)
        self.completed_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar con grid
        self.completed_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Etiqueta de resumen con límite
        self.completed_summary = ttk.Label(completed_frame, 
                                           text="Total: 0 tareas | Mostrando: 0",
                                           font=('Segoe UI', 10, 'bold'),
                                           foreground=self.colors['primary'])
        self.completed_summary.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Configurar tags de color
        self.completed_tree.tag_configure('critical', background='#ffebee', foreground='#c62828')
        self.completed_tree.tag_configure('normal', background='#e8f5e9', foreground='#2e7d32')
        
    def setup_queue_display(self, parent, queue_type):
        """Configurar display de cola con canvas y scrollbar y límite de visibilidad"""
        # Frame para contener canvas y scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        
        # Canvas para scroll
        canvas = tk.Canvas(container, bg=self.colors['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
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
        
        # Empaquetar con grid
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Guardar referencias
        if queue_type == "normal":
            self.normal_queue_frame = inner_frame
            self.normal_canvas = canvas
        else:
            self.critical_queue_frame = inner_frame
            self.critical_canvas = canvas
    
    def setup_log_panel(self, parent):
        """Configurar panel de log profesional con límite de líneas"""
        log_frame = ttk.LabelFrame(parent, 
                                  text="Registro de Ejecución",
                                  padding="5")
        log_frame.grid(row=4, column=0, sticky="ew", pady=(0, 5))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Text widget con scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.grid(row=0, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(text_frame,
                                height=5,
                                font=('Consolas', 9),
                                bg=self.colors['white'],
                                fg=self.colors['text'],
                                wrap=tk.WORD)
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", 
                                 command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Tags para colorear logs
        self.log_text.tag_config("info", foreground=self.colors['accent'])
        self.log_text.tag_config("success", foreground=self.colors['success'])
        self.log_text.tag_config("warning", foreground=self.colors['warning'])
        self.log_text.tag_config("critical", foreground=self.colors['warning'], font=('Consolas', 9, 'bold'))
        self.log_text.tag_config("parallel", foreground=self.colors['parallel'], font=('Consolas', 9, 'bold'))
        
    def setup_status_bar(self):
        """Configurar barra de estado profesional"""
        status_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        # Configurar grid para mejor distribución
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=0)
        status_frame.columnconfigure(2, weight=0)
        status_frame.columnconfigure(3, weight=0)
        
        self.status_label = tk.Label(status_frame,
                                     text="✅ Sistema listo | Modo: Procesamiento Paralelo",
                                     bg=self.colors['secondary'],
                                     fg='white',
                                     font=('Segoe UI', 9),
                                     anchor='w')
        self.status_label.grid(row=0, column=0, padx=10, sticky="w")
        
        self.task_counter = tk.Label(status_frame,
                                     text="Tareas: 0",
                                     bg=self.colors['secondary'],
                                     fg='white',
                                     font=('Segoe UI', 9))
        self.task_counter.grid(row=0, column=1, padx=10)
        
        self.parallel_indicator = tk.Label(status_frame,
                                          text="⚡ PARALELO",
                                          bg=self.colors['parallel'],
                                          fg='white',
                                          font=('Segoe UI', 9, 'bold'),
                                          padx=10)
        self.parallel_indicator.grid(row=0, column=2, padx=5)
        
        self.system_status = tk.Label(status_frame,
                                      text="● EN LÍNEA",
                                      bg=self.colors['secondary'],
                                      fg=self.colors['success'],
                                      font=('Segoe UI', 9, 'bold'))
        self.system_status.grid(row=0, column=3, padx=10)
        
    def setup_metrics_panel(self, parent):
        """Configurar panel de métricas en tiempo real"""
        metrics_frame = ttk.LabelFrame(parent, 
                                      text="Métricas en Tiempo Real",
                                      padding="10")
        metrics_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        metrics_frame.columnconfigure(0, weight=1)
        
        # Grid de métricas con 7 items en una fila
        metrics_grid = ttk.Frame(metrics_frame)
        metrics_grid.pack(fill=tk.X, expand=True)
        
        for i in range(7):
            metrics_grid.columnconfigure(i, weight=1)
        
        # Métricas con diseño profesional
        metrics = [
            ("📊 Tareas Normales", "normal_count", self.colors['success']),
            ("⚠ Tareas Críticas", "critical_count", self.colors['warning']),
            ("⚙ En Ejecución", "executing_count", self.colors['parallel']),
            ("✅ Completadas", "completed_count", self.colors['accent']),
            ("⏱ Tiempo Promedio", "avg_wait", self.colors['info']),
            ("⚙ Rendimiento", "throughput", self.colors['primary']),
            ("🎯 Utilización", "utilization", self.colors['secondary'])
        ]
        
        self.metric_labels = {}
        for i, (label, key, color) in enumerate(metrics):
            frame = tk.Frame(metrics_grid, bg=self.colors['white'], relief=tk.RAISED, bd=1)
            frame.grid(row=0, column=i, padx=5, pady=2, sticky="nsew")
            
            ttk.Label(frame, text=label, style='Header.TLabel').pack(pady=(5, 2))
            
            self.metric_labels[key] = ttk.Label(frame, 
                                                text="0", 
                                                font=('Segoe UI', 16, 'bold'),
                                                foreground=color)
            self.metric_labels[key].pack(pady=(0, 5))
    
    def update_executing_display(self):
        """Actualizar display de tareas en ejecución con colores correctos según prioridad"""
        # Limpiar container
        for widget in self.executing_container.winfo_children():
            widget.destroy()
        
        self.executing_labels = []
        
        if self.tareas_en_ejecucion:
            # Frame para contener las tareas en horizontal
            tasks_frame = ttk.Frame(self.executing_container)
            tasks_frame.pack(fill=tk.X, expand=True)
            
            # Mostrar tareas en ejecución con sus colores correctos
            for tarea in self.tareas_en_ejecucion:
                # Determinar color basado en la prioridad real de la tarea
                if tarea.prioridad == "Crítica":
                    bg_color = self.colors['warning']  # Rojo para críticas
                    icon = "⚡"
                    tiempo_text = f"Tiempo: 1s"
                else:
                    bg_color = self.colors['success']  # Verde para normales
                    icon = "📋"
                    tiempo_text = f"Tiempo: 2s"
                
                # Crear frame para cada tarea
                frame = tk.Frame(tasks_frame,
                               bg=bg_color,
                               relief=tk.RAISED,
                               bd=2,
                               padx=10,
                               pady=5)
                frame.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.BOTH)
                
                # Mostrar icono y ID según prioridad real
                tk.Label(frame,
                        text=f"{icon} {tarea}",
                        bg=frame['bg'],
                        fg='white',
                        font=('Segoe UI', 12, 'bold')).pack()
                
                tk.Label(frame,
                        text=f"{tarea.descripcion[:20]}..." if len(tarea.descripcion) > 20 else tarea.descripcion,
                        bg=frame['bg'],
                        fg='white',
                        font=('Segoe UI', 9)).pack()
                
                # Mostrar tiempo según prioridad real
                tk.Label(frame,
                        text=tiempo_text,
                        bg=frame['bg'],
                        fg='white',
                        font=('Segoe UI', 9, 'bold')).pack()
                
                # Barra de progreso simulada
                progress_frame = tk.Frame(frame, bg=frame['bg'], height=6)
                progress_frame.pack(fill=tk.X, pady=(5, 0))
                
                progress = tk.Frame(progress_frame, bg='white', height=6, width=80)
                progress.pack(side=tk.LEFT)
                
                # Animación de progreso
                self.animate_progress(progress, tarea)
            
            # Indicador de procesamiento paralelo si hay más de una tarea
            if len(self.tareas_en_ejecucion) > 1:
                parallel_frame = tk.Frame(tasks_frame,
                                         bg=self.colors['parallel'],
                                         relief=tk.RAISED,
                                         bd=2,
                                         padx=10,
                                         pady=5)
                parallel_frame.pack(side=tk.RIGHT, padx=2, fill=tk.Y)
                
                tk.Label(parallel_frame,
                        text="⚡ PARALELO",
                        bg=self.colors['parallel'],
                        fg='white',
                        font=('Segoe UI', 10, 'bold')).pack()
                
                # Mostrar qué tareas se están ejecutando en paralelo
                tipos = [t.prioridad for t in self.tareas_en_ejecucion]
                if "Crítica" in tipos and "Normal" in tipos:
                    info_text = "Crítica (1s)\n+ Normal (2s)"
                elif all(t.prioridad == "Crítica" for t in self.tareas_en_ejecucion):
                    info_text = "2 Críticas\n(1s c/u)"
                else:
                    info_text = "2 Normales\n(2s c/u)"
                
                tk.Label(parallel_frame,
                        text=info_text,
                        bg=self.colors['parallel'],
                        fg='white',
                        font=('Segoe UI', 8),
                        justify=tk.CENTER).pack()
        else:
            # No hay tareas en ejecución
            label = tk.Label(self.executing_container,
                           text="⏸ No hay tareas en ejecución",
                           bg=self.colors['background'],
                           fg=self.colors['secondary'],
                           font=('Segoe UI', 11, 'italic'),
                           padx=20,
                           pady=15)
            label.pack(fill=tk.BOTH, expand=True)
    
    def animate_progress(self, progress_bar, tarea):
        """Animar barra de progreso"""
        def update_width(width=0):
            if tarea in self.tareas_en_ejecucion and width < 100:
                try:
                    progress_bar.config(width=width)
                    self.root.after(int(tarea.tiempo_ejecucion * 10), update_width, width + 1)
                except:
                    pass
            else:
                try:
                    progress_bar.config(width=100)
                except:
                    pass
        
        update_width()
    
    def actualizar_tiempo(self):
        """Actualizar reloj en tiempo real"""
        now = datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%A, %d de %B de %Y"))
        self.root.after(1000, self.actualizar_tiempo)
    
    def generar_tarea_normal(self):
        """Generar tarea normal con límite de visibilidad"""
        if len(self.cola_normal) + len(self.bicola_critica) >= self.max_tareas_visibles * 2:
            self.agregar_log("⚠ Límite de tareas alcanzado", "warning")
            return
            
        self.contador_tareas += 1
        tarea = Tarea(self.contador_tareas, "Normal", f"Tarea Estándar #{self.contador_tareas}")
        self.cola_normal.append(tarea)
        self.actualizar_orden_ejecucion()
        self.actualizar_interfaz()
        self.agregar_log(f"📥 Tarea normal {tarea} (2s) agregada a la cola", "info")
        
    def generar_tarea_critica(self):
        """Generar tarea crítica con límite de visibilidad"""
        if len(self.cola_normal) + len(self.bicola_critica) >= self.max_tareas_visibles * 2:
            self.agregar_log("⚠ Límite de tareas alcanzado", "warning")
            return
            
        self.contador_tareas += 1
        tarea = Tarea(self.contador_tareas, "Crítica", f"Tarea Crítica #{self.contador_tareas}")
        self.bicola_critica.appendleft(tarea)
        self.actualizar_orden_ejecucion()
        self.actualizar_interfaz()
        self.agregar_log(f"⚡ Tarea CRÍTICA {tarea} (1s) agregada a la cola prioritaria", "critical")
        
    def generar_15_tareas(self):
        """Generar 15 tareas automáticamente con límite"""
        for i in range(15):
            if len(self.cola_normal) + len(self.bicola_critica) >= self.max_tareas_visibles * 2:
                self.agregar_log("⚠ Límite de tareas alcanzado", "warning")
                break
                
            self.contador_tareas += 1
            if random.random() < 0.3:
                tarea = Tarea(self.contador_tareas, "Crítica", f"Tarea Crítica #{self.contador_tareas}")
                self.bicola_critica.appendleft(tarea)
            else:
                tarea = Tarea(self.contador_tareas, "Normal", f"Tarea Estándar #{self.contador_tareas}")
                self.cola_normal.append(tarea)
        
        self.actualizar_orden_ejecucion()
        self.actualizar_interfaz()
        self.agregar_log("🎲 15 tareas generadas automáticamente", "success")
        
    def actualizar_orden_ejecucion(self):
        """Actualizar la lista de orden de ejecución"""
        # Limpiar treeview
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        # Construir lista de orden de ejecución
        orden = []
        posicion = 1
        
        # Primero las tareas críticas (en orden) que no están en ejecución
        for tarea in self.bicola_critica:
            if tarea not in self.tareas_en_ejecucion:
                orden.append((posicion, tarea, "critical"))
                posicion += 1
        
        # Luego las tareas normales que no están en ejecución
        for tarea in self.cola_normal:
            if tarea not in self.tareas_en_ejecucion:
                orden.append((posicion, tarea, "normal"))
                posicion += 1
        
        # Mostrar en el treeview (con límite de visibilidad)
        for i, (pos, tarea, tipo) in enumerate(orden[:self.max_tareas_visibles]):
            tag = 'next' if i == 0 else tipo
            self.order_tree.insert('', 'end', values=(
                f"#{pos}",
                f"T{tarea.id:03d}",
                tarea.prioridad,
                tarea.descripcion[:30] + "..." if len(tarea.descripcion) > 30 else tarea.descripcion,
                f"{tarea.tiempo_ejecucion:.2f}"
            ), tags=(tag,))
        
        # Actualizar información de próxima tarea
        if orden:
            next_tarea = orden[0][1]
            self.order_info.config(
                text=f"➡ Próxima: {next_tarea} ({next_tarea.prioridad}) - {next_tarea.tiempo_ejecucion:.2f}s"
            )
        else:
            self.order_info.config(text="Próxima tarea: -")
        
    def iniciar_simulacion(self):
        """Iniciar simulación con procesamiento paralelo"""
        if self.ejecutando:
            return
            
        if not self.cola_normal and not self.bicola_critica:
            self.agregar_log("⚠ No hay tareas para ejecutar", "warning")
            return
            
        self.ejecutando = True
        self.tiempo_inicio = time.time()
        self.system_status.config(text="● EJECUTANDO (PARALELO)", fg=self.colors['parallel'])
        self.agregar_log("▶ Simulación iniciada - Modo PARALELO activado", "parallel")
        
        # Iniciar el procesamiento continuo
        self.procesar_siguiente_lote()
        
    def procesar_siguiente_lote(self):
        """Procesar el siguiente lote de tareas en paralelo (priorizando crítica + normal)"""
        if not self.ejecutando:
            return
            
        # Verificar si hay espacio para nuevas tareas (máximo 2 en paralelo)
        with self.lock:
            espacio_paralelo = 2 - len(self.tareas_en_ejecucion)
        
        if espacio_paralelo > 0:
            tareas_a_ejecutar = []
            
            with self.lock:
                # PRIMERO: Intentar tomar una tarea crítica
                tarea_critica = None
                if self.bicola_critica and espacio_paralelo > 0:
                    tarea_critica = self.bicola_critica.popleft()
                    tareas_a_ejecutar.append(tarea_critica)
                    self.tareas_en_ejecucion.append(tarea_critica)
                    espacio_paralelo -= 1
                    self.agregar_log(f"⚡ Preparando tarea CRÍTICA {tarea_critica} (1s) para ejecución", "critical")
                
                # SEGUNDO: Intentar tomar una tarea normal para ejecutar en paralelo
                tarea_normal = None
                if self.cola_normal and espacio_paralelo > 0:
                    tarea_normal = self.cola_normal.popleft()
                    tareas_a_ejecutar.append(tarea_normal)
                    self.tareas_en_ejecucion.append(tarea_normal)
                    espacio_paralelo -= 1
                    self.agregar_log(f"📋 Preparando tarea NORMAL {tarea_normal} (2s) para ejecución", "info")
                
                # Si todavía hay espacio y no hay normal, tomar otra crítica
                if espacio_paralelo > 0 and self.bicola_critica:
                    tarea_critica2 = self.bicola_critica.popleft()
                    tareas_a_ejecutar.append(tarea_critica2)
                    self.tareas_en_ejecucion.append(tarea_critica2)
                    self.agregar_log(f"⚡ Preparando segunda tarea CRÍTICA {tarea_critica2} (1s)", "critical")
            
            # Registrar qué tipo de ejecución vamos a hacer
            if len(tareas_a_ejecutar) == 2:
                tipos = [t.prioridad for t in tareas_a_ejecutar]
                if "Crítica" in tipos and "Normal" in tipos:
                    self.agregar_log("✨ EJECUTANDO EN PARALELO: Una crítica (1s) y una normal (2s)", "parallel")
                elif all(t.prioridad == "Crítica" for t in tareas_a_ejecutar):
                    self.agregar_log("⚡ EJECUTANDO EN PARALELO: Dos tareas críticas (1s cada una)", "critical")
                else:
                    self.agregar_log("📋 EJECUTANDO EN PARALELO: Dos tareas normales (2s cada una)", "info")
            elif len(tareas_a_ejecutar) == 1:
                if tareas_a_ejecutar[0].prioridad == "Crítica":
                    self.agregar_log("⚡ EJECUTANDO: Una tarea crítica (1s)", "critical")
                else:
                    self.agregar_log("📋 EJECUTANDO: Una tarea normal (2s)", "info")
            
            # Ejecutar tareas en paralelo
            for tarea in tareas_a_ejecutar:
                thread = threading.Thread(target=self.ejecutar_tarea_thread, args=(tarea,))
                thread.daemon = True
                thread.start()
        
        # Programar siguiente verificación
        if self.ejecutando and (self.cola_normal or self.bicola_critica or self.tareas_en_ejecucion):
            self.root.after(100, self.procesar_siguiente_lote)
        elif not self.tareas_en_ejecucion:
            self.finalizar_simulacion()
    
    def ejecutar_tarea_thread(self, tarea):
        """Ejecutar una tarea en un hilo separado"""
        try:
            # Determinar el tipo de log según la prioridad
            log_tipo = "critical" if tarea.prioridad == "Crítica" else "info"
            
            # Actualizar UI en el hilo principal
            self.root.after(0, lambda: self.actualizar_interfaz())
            
            # Simular tiempo de ejecución
            time.sleep(tarea.tiempo_ejecucion)
            
            # Marcar como completada
            with self.lock:
                if tarea in self.tareas_en_ejecucion:
                    self.tareas_en_ejecucion.remove(tarea)
                
                tarea.estado = "Completada"
                tarea.hora_fin = datetime.now().strftime("%H:%M:%S")
                self.tareas_ejecutadas.append(tarea)
            
            # Actualizar UI en el hilo principal
            self.root.after(0, lambda: self.tarea_completada(tarea))
            
        except Exception as e:
            self.root.after(0, lambda: self.agregar_log(f"❌ Error en tarea {tarea}: {e}", "warning"))
    
    def tarea_completada(self, tarea):
        """Manejar finalización de tarea"""
        # Actualizar orden de ejecución
        self.actualizar_orden_ejecucion()
        
        # Actualizar lista de completadas
        self.actualizar_lista_completadas()
        
        # Log de finalización
        if tarea.prioridad == "Crítica":
            self.agregar_log(f"✅ COMPLETADA: {tarea} (Crítica) - Tiempo: 1s", "success")
        else:
            self.agregar_log(f"✅ COMPLETADA: {tarea} (Normal) - Tiempo: 2s", "success")
        
        # Actualizar toda la interfaz
        self.actualizar_interfaz()
        
        # Verificar si debemos continuar procesando
        if self.ejecutando and (self.cola_normal or self.bicola_critica):
            self.procesar_siguiente_lote()
        
    def actualizar_lista_completadas(self):
        """Actualizar la lista de tareas completadas con límite"""
        # Limpiar treeview
        for item in self.completed_tree.get_children():
            self.completed_tree.delete(item)
        
        # Mostrar solo las últimas max_completadas_visibles tareas
        tareas_mostrar = self.tareas_ejecutadas[-self.max_completadas_visibles:]
        
        for tarea in reversed(tareas_mostrar):
            tag = 'critical' if tarea.prioridad == "Crítica" else 'normal'
            
            self.completed_tree.insert('', '0', values=(
                f"T{tarea.id:03d}",
                tarea.prioridad,
                tarea.descripcion[:30] + "..." if len(tarea.descripcion) > 30 else tarea.descripcion,
                f"{tarea.tiempo_ejecucion:.2f}",
                tarea.hora_fin if tarea.hora_fin else "-"
            ), tags=(tag,))
        
        # Actualizar resumen
        total = len(self.tareas_ejecutadas)
        mostrando = min(total, self.max_completadas_visibles)
        self.completed_summary.config(
            text=f"Total: {total} tareas | Mostrando: {mostrando}"
        )
        
    def actualizar_interfaz(self):
        """Actualizar toda la interfaz"""
        self.actualizar_colas()
        self.actualizar_metricas()
        self.update_executing_display()
        
        # Actualizar contador de tareas en barra de estado
        total_tareas = len(self.cola_normal) + len(self.bicola_critica) + len(self.tareas_ejecutadas) + len(self.tareas_en_ejecucion)
        self.task_counter.config(text=f"Tareas: {total_tareas}")
        
        # Actualizar indicador de modo paralelo
        if len(self.tareas_en_ejecucion) > 1:
            self.parallel_indicator.config(text="⚡ PARALELO ACTIVO", bg=self.colors['parallel'])
        elif len(self.tareas_en_ejecucion) == 1:
            self.parallel_indicator.config(text="▶ EJECUCIÓN SIMPLE", bg=self.colors['accent'])
        else:
            self.parallel_indicator.config(text="⏸ EN ESPERA", bg=self.colors['secondary'])
        
    def actualizar_colas(self):
        """Actualizar visualización de las colas con límite de visibilidad"""
        # Limpiar frames
        for widget in self.normal_queue_frame.winfo_children():
            widget.destroy()
        for widget in self.critical_queue_frame.winfo_children():
            widget.destroy()
        
        # Mostrar tareas normales (con límite) - excluir las que están en ejecución
        tareas_normal = [t for t in self.cola_normal if t not in self.tareas_en_ejecucion]
        tareas_normal = tareas_normal[:self.max_tareas_visibles]
        
        for i, tarea in enumerate(tareas_normal):
            self.crear_tarea_widget(self.normal_queue_frame, tarea, i, "normal")
        
        # Mostrar indicador si hay más tareas
        if len(self.cola_normal) > self.max_tareas_visibles:
            self.crear_mensaje_limite(self.normal_queue_frame, 
                                      len(self.cola_normal) - self.max_tareas_visibles)
        
        # Mostrar tareas críticas (con límite) - excluir las que están en ejecución
        tareas_criticas = [t for t in self.bicola_critica if t not in self.tareas_en_ejecucion]
        tareas_criticas = tareas_criticas[:self.max_tareas_visibles]
        
        for i, tarea in enumerate(tareas_criticas):
            self.crear_tarea_widget(self.critical_queue_frame, tarea, i, "critical")
        
        # Mostrar indicador si hay más tareas
        if len(self.bicola_critica) > self.max_tareas_visibles:
            self.crear_mensaje_limite(self.critical_queue_frame,
                                      len(self.bicola_critica) - self.max_tareas_visibles)
            
    def crear_mensaje_limite(self, parent, cantidad_extra):
        """Crear mensaje de límite de visualización"""
        frame = tk.Frame(parent,
                        bg=self.colors['secondary'],
                        relief=tk.RAISED,
                        bd=1,
                        padx=8,
                        pady=4)
        frame.pack(fill=tk.X, pady=2)
        
        tk.Label(frame,
                text=f"... y {cantidad_extra} tareas más",
                bg=self.colors['secondary'],
                fg='white',
                font=('Segoe UI', 8, 'italic')).pack()
            
    def crear_tarea_widget(self, parent, tarea, index, tipo):
        """Crear widget para una tarea"""
        color = self.colors['warning'] if tipo == "critical" else self.colors['success']
        
        frame = tk.Frame(parent,
                        bg=self.colors['white'],
                        relief=tk.RAISED,
                        bd=1,
                        padx=8,
                        pady=3)
        frame.pack(fill=tk.X, pady=1)
        
        # Icono según tipo
        icon = "⚡" if tipo == "critical" else "📋"
        
        # Información de la tarea
        info_frame = tk.Frame(frame, bg=self.colors['white'])
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(info_frame,
                text=f"{icon} {tarea}",
                bg=self.colors['white'],
                fg=color,
                font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)
        
        # Acortar descripción si es muy larga
        descripcion = tarea.descripcion
        if len(descripcion) > 20:
            descripcion = descripcion[:20] + "..."
        
        tk.Label(info_frame,
                text=f" - {descripcion}",
                bg=self.colors['white'],
                fg=self.colors['secondary'],
                font=('Segoe UI', 8)).pack(side=tk.LEFT, padx=(3,0))
        
        # Tiempo de ejecución fijo
        tiempo_text = f"[{tarea.tiempo_ejecucion:.0f}s]"
        tk.Label(frame,
                text=tiempo_text,
                bg=self.colors['white'],
                fg=color,
                font=('Segoe UI', 8, 'bold')).pack(side=tk.RIGHT)
        
    def actualizar_metricas(self):
        """Actualizar métricas en tiempo real"""
        self.metric_labels['normal_count'].config(text=str(len([t for t in self.cola_normal if t not in self.tareas_en_ejecucion])))
        self.metric_labels['critical_count'].config(text=str(len([t for t in self.bicola_critica if t not in self.tareas_en_ejecucion])))
        self.metric_labels['completed_count'].config(text=str(len(self.tareas_ejecutadas)))
        self.metric_labels['executing_count'].config(text=str(len(self.tareas_en_ejecucion)))
        
        # Calcular tiempo promedio de espera
        if self.tareas_ejecutadas:
            tiempos = [t.tiempo_ejecucion for t in self.tareas_ejecutadas[-50:]]  # Últimas 50
            avg_wait = sum(tiempos) / len(tiempos)
            self.metric_labels['avg_wait'].config(text=f"{avg_wait:.2f}s")
        else:
            self.metric_labels['avg_wait'].config(text="0.00s")
        
        # Calcular rendimiento (throughput) promedio
        if self.tiempo_inicio and self.ejecutando:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            if tiempo_transcurrido > 0:
                throughput = len(self.tareas_ejecutadas) / tiempo_transcurrido
                self.metric_labels['throughput'].config(text=f"{throughput:.2f}/s")
        else:
            self.metric_labels['throughput'].config(text="0.00/s")
        
        # Calcular utilización
        total_tasks = len(self.tareas_ejecutadas) + len(self.cola_normal) + len(self.bicola_critica) + len(self.tareas_en_ejecucion)
        if total_tasks > 0:
            utilization = (len(self.tareas_ejecutadas) / total_tasks) * 100
            self.metric_labels['utilization'].config(text=f"{utilization:.1f}%")
        else:
            self.metric_labels['utilization'].config(text="0%")
    
    def finalizar_simulacion(self):
        """Finalizar simulación"""
        self.ejecutando = False
        tiempo_total = time.time() - self.tiempo_inicio if self.tiempo_inicio else 0
        self.system_status.config(text="● EN LÍNEA", fg=self.colors['success'])
        self.parallel_indicator.config(text="⚡ PARALELO", bg=self.colors['parallel'])
        self.agregar_log(f"✅ Simulación completada - Tiempo total: {tiempo_total:.2f}s - Tareas: {len(self.tareas_ejecutadas)}", "success")
        
        # Estadísticas finales
        tareas_normales = sum(1 for t in self.tareas_ejecutadas if t.prioridad == "Normal")
        tareas_criticas = sum(1 for t in self.tareas_ejecutadas if t.prioridad == "Crítica")
        self.agregar_log(f"📊 Estadísticas: {tareas_normales} normales, {tareas_criticas} críticas", "info")
        
    def detener_simulacion(self):
        """Detener simulación"""
        self.ejecutando = False
        self.system_status.config(text="● DETENIDO", fg=self.colors['warning'])
        self.parallel_indicator.config(text="⏸ DETENIDO", bg=self.colors['warning'])
        self.agregar_log("⏹ Simulación detenida por el usuario", "warning")
        
    def limpiar_todo(self):
        """Limpiar todo el sistema"""
        self.ejecutando = False
        time.sleep(0.1)  # Pequeña pausa para permitir que los hilos terminen
        
        with self.lock:
            self.cola_normal.clear()
            self.bicola_critica.clear()
            self.tareas_ejecutadas.clear()
            self.tareas_en_ejecucion.clear()
            self.orden_ejecucion.clear()
            self.contador_tareas = 0
        
        self.system_status.config(text="● EN LÍNEA", fg=self.colors['success'])
        self.parallel_indicator.config(text="⚡ PARALELO", bg=self.colors['parallel'])
        
        # Limpiar listas
        for item in self.completed_tree.get_children():
            self.completed_tree.delete(item)
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        self.actualizar_interfaz()
        self.log_text.delete(1.0, tk.END)
        self.completed_summary.config(text="Total: 0 tareas | Mostrando: 0")
        self.order_info.config(text="Próxima tarea: -")
        self.update_executing_display()
        self.agregar_log("🔄 Sistema reiniciado correctamente", "info")
        
    def agregar_log(self, mensaje, tipo="info"):
        """Agregar mensaje al log con límite de líneas"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensaje}\n"
        
        self.log_text.insert(tk.END, log_entry, tipo)
        
        # Limitar número de líneas en el log
        line_count = int(self.log_text.index('end-1c').split('.')[0])
        if line_count > self.max_log_lines:
            self.log_text.delete(1.0, f"{line_count - self.max_log_lines}.0")
        
        self.log_text.see(tk.END)
        
        # Actualizar barra de estado
        self.status_label.config(text=f"📌 {mensaje}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configurar para que la ventana sea redimensionable
    root.minsize(1200, 700)
    
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
            time.sleep(0.2)  # Pequeña pausa para limpiar hilos
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()