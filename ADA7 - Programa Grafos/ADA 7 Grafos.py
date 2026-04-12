import tkinter as tk
from itertools import permutations
import math

estados = [
    "CDMX",
    "Jalisco",
    "Nuevo Leon",
    "Yucatan",
    "Chiapas",
    "Veracruz",
    "Puebla"
]

conexiones = {
    ("CDMX", "Puebla"): 2,
    ("CDMX", "Veracruz"): 5,
    ("CDMX", "Jalisco"): 6,
    ("Jalisco", "Nuevo Leon"): 7,
    ("Jalisco", "Veracruz"): 9,
    ("Nuevo Leon", "Veracruz"): 10,
    ("Veracruz", "Puebla"): 3,
    ("Veracruz", "Chiapas"): 6,
    ("Veracruz", "Yucatan"): 8,
    ("Puebla", "Chiapas"): 7,
    ("Chiapas", "Yucatan"): 9
}


adyacencia = {estado: {} for estado in estados}
for (u, v), costo in conexiones.items():
    adyacencia[u][v] = costo
    adyacencia[v][u] = costo


def mostrar_relaciones():
    print("\n" + "="*60)
    print("ESTADOS Y SUS RELACIONES (COSTOS EN HORAS)")
    print("="*60)
    for estado in sorted(estados):
        print(f"\n{estado}:")
        for vecino, costo in sorted(adyacencia[estado].items()):
            print(f"  └─> {vecino}: {costo} horas")
    print("\n" + "="*60)


def recorrido_sin_repetir():
    mejor_ruta = None
    mejor_costo = float('inf')
    
    for perm in permutations(estados):
        valido = True
        costo_total = 0
        
        for i in range(len(perm)-1):
            if perm[i+1] not in adyacencia[perm[i]]:
                valido = False
                break
            costo_total += adyacencia[perm[i]][perm[i+1]]
        
        if valido and costo_total < mejor_costo:
            mejor_costo = costo_total
            mejor_ruta = perm
    
    return mejor_ruta, mejor_costo


def recorrido_con_repeticion():
    inicio = "CDMX"
    ruta = [inicio]
    costo_total = 0
    visitados_set = {inicio}
    
    while len(visitados_set) < len(estados):
        actual = ruta[-1]
        
        vecinos = sorted(adyacencia[actual].items(), key=lambda x: x[1])
        
        destino_encontrado = False
        for vecino, costo in vecinos:
            if vecino not in visitados_set:
                ruta.append(vecino)
                visitados_set.add(vecino)
                costo_total += costo
                destino_encontrado = True
                break
        
        if not destino_encontrado and vecinos:
            vecino, costo = vecinos[0]
            ruta.append(vecino)
            costo_total += costo
    
    return ruta, costo_total


class VisualizadorGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("Grafo de Estados de México")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        
        self.posiciones = self.calcular_posiciones()
        
        self.canvas = tk.Canvas(root, width=850, height=600, bg='white', highlightthickness=2, highlightbackground='gray')
        self.canvas.pack(pady=10)
        
        frame_botones = tk.Frame(root, bg='white')
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="Dibujar Grafo", command=self.dibujar_grafo, 
                 bg='lightblue', font=('Arial', 12), padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Mostrar Relaciones", command=self.mostrar_relaciones_ventana, 
                 bg='lightgreen', font=('Arial', 12), padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="Salir", command=root.quit, 
                 bg='lightcoral', font=('Arial', 12), padx=20, pady=5).pack(side=tk.LEFT, padx=10)
        
        self.info_label = tk.Label(root, text="Presiona 'Dibujar Grafo' para visualizar", 
                                   bg='white', font=('Arial', 11), fg='blue')
        self.info_label.pack(pady=5)
        
        self.dibujar_grafo()
    
    def calcular_posiciones(self):
        """Calcula posiciones en un círculo para los 7 estados"""
        centro_x, centro_y = 425, 300
        radio = 200
        angulos = [i * (2 * math.pi / len(estados)) for i in range(len(estados))]
        
        posiciones = {}
        for i, estado in enumerate(estados):
            x = centro_x + radio * math.cos(angulos[i])
            y = centro_y + radio * math.sin(angulos[i])
            posiciones[estado] = (x, y)
        
        posiciones["Yucatan"] = (600, 150)
        posiciones["Chiapas"] = (550, 400)
        posiciones["CDMX"] = (425, 300)
        posiciones["Jalisco"] = (250, 250)
        posiciones["Nuevo Leon"] = (200, 400)
        posiciones["Veracruz"] = (500, 300)
        posiciones["Puebla"] = (450, 200)
        
        return posiciones
    
    def dibujar_grafo(self):
        """Dibuja el grafo completo con nodos, aristas y costos"""
        self.canvas.delete("all")
        
        for (u, v), costo in conexiones.items():
            x1, y1 = self.posiciones[u]
            x2, y2 = self.posiciones[v]
            
            self.canvas.create_line(x1, y1, x2, y2, width=2, fill='gray', tags=('arista',))
            
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            # Desplazar ligeramente para mejor visibilidad
            angle = math.atan2(y2 - y1, x2 - x1)
            offset_x = 10 * math.sin(angle)
            offset_y = -10 * math.cos(angle)
            
            self.canvas.create_text(mid_x + offset_x, mid_y + offset_y, 
                                   text=str(costo), fill='red', font=('Arial', 10, 'bold'),
                                   tags=('costo',))
        
        for estado, (x, y) in self.posiciones.items():
            self.canvas.create_oval(x-30, y-30, x+30, y+30, fill='lightblue', 
                                   outline='darkblue', width=2, tags=('nodo',))
            
            if " " in estado:
                palabras = estado.split()
                texto = f"{palabras[0]}\n{palabras[1]}"
            else:
                texto = estado
            
            self.canvas.create_text(x, y, text=texto, font=('Arial', 9, 'bold'), 
                                   fill='darkblue', tags=('texto',))
        
        self.info_label.config(text="Grafo dibujado correctamente - " + 
                              f"{len(conexiones)} conexiones mostradas", fg='green')
    
    def mostrar_relaciones_ventana(self):
        """Muestra las relaciones en una ventana emergente"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Relaciones entre Estados")
        ventana.geometry("400x500")
        ventana.configure(bg='white')
        
        tk.Label(ventana, text="CONEXIONES Y COSTOS", font=('Arial', 14, 'bold'), 
                bg='white', fg='darkblue').pack(pady=10)
        
        texto = tk.Text(ventana, wrap=tk.WORD, width=45, height=25, font=('Courier', 10))
        texto.pack(padx=20, pady=10)
        
        for (u, v), costo in sorted(conexiones.items()):
            texto.insert(tk.END, f"{u:15} ↔ {v:15} : {costo:3} horas\n")
        
        texto.config(state=tk.DISABLED)
        
        tk.Button(ventana, text="Cerrar", command=ventana.destroy, 
                 bg='lightcoral', font=('Arial', 10)).pack(pady=10)


def mostrar_ruta(ruta, costo, titulo):
    print(f"\n{titulo}")
    print("─" * 50)
    print("Ruta:")
    for i in range(len(ruta)-1):
        print(f"  {ruta[i]} → {ruta[i+1]} ({adyacencia[ruta[i]][ruta[i+1]]} hrs)")
    print(f"\n✓ Costo total: {costo} horas")
    print(f"✓ Estados visitados: {len(set(ruta))} diferentes")
    print(f"✓ Longitud de ruta: {len(ruta)} pasos")


if __name__ == "__main__":
    mostrar_relaciones()
    
    ruta_sin, costo_sin = recorrido_sin_repetir()
    mostrar_ruta(ruta_sin, costo_sin, "INCISO A: RECORRIDO SIN REPETIR ESTADOS")
    
    ruta_con, costo_con = recorrido_con_repeticion()
    mostrar_ruta(ruta_con, costo_con, "INCISO B: RECORRIDO REPITIENDO AL MENOS UN ESTADO")
    
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"Recorrido sin repetición: {costo_sin} horas")
    print(f"Recorrido con repetición: {costo_con} horas")
    print(f"Diferencia: {abs(costo_con - costo_sin):.1f} horas")
    print("="*60)
    
    print("\nAbriendo ventana visual del grafo...")
    root = tk.Tk()
    app = VisualizadorGrafo(root)
    root.mainloop()