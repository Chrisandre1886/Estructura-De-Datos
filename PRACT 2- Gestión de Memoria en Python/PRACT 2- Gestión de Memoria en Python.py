
#Codigo 1 Video
from tkinter import simpledialog
import tkinter as tk

root = tk.Tk()
root.withdraw()

calificaciones = [0] * 5

for i in range(5):
    calificaciones[i] = int(simpledialog.askstring("Entrada", "Ingresa la calificación"))
print (f"Codigo 1")

for i in range(5):
    print(f"La calificación {i+1} es: {calificaciones[i]}")


#Codigo 2 Video
print (f"  ")
print (f"Codigo 2")
Frutas = []
Frutas.append("Manzana")
Frutas.append("Pera")
Frutas.append("Uvas")
Frutas.append("Bananas")
print(Frutas)
Frutas.pop(1)
Frutas.pop(0)
Frutas.append("sandia")
print(Frutas)