class Postre:
    def __init__(self, nombre, ingredientes):
        self.nombre = nombre
        self.ingredientes = ingredientes

POSTRES = []

def mostrar_menu():
    print("\n=== SISTEMA DE POSTRES ===")
    print("1. Ver ingredientes de un postre en especifico")
    print("2. Agregar ingrediente a un postre en especifico")
    print("3. Eliminar ingrediente a un postre en especifico")
    print("4. Modificar ingredientes a un postre en especifico")
    print("5. Dar de alta postre")
    print("6. Dar de baja postre")
    print("7. Eliminar repetidos")
    print("8. Mostrar todos los postres registrados")
    print("9. Salir")
    print("===========================")


def buscar_todos_postres(nombre):
    return [i for i, p in enumerate(POSTRES) if p.nombre.lower() == nombre.lower()]


def seleccionar_postre(indices, accion):
    if not indices:
        print("Error: El postre no existe")
        return -1
    if len(indices) == 1:
        return indices[0]
    print(f"\nSe encontraron {len(indices)} postres:")
    for i, idx in enumerate(indices):
        print(f"{i+1}. {POSTRES[idx].nombre} - {len(POSTRES[idx].ingredientes)} ingredientes")
    try:
        sel = int(input(f"Seleccione (1-{len(indices)}): ")) - 1
        return indices[sel] if 0 <= sel < len(indices) else -1
    except:
        print("Error: Número inválido")
        return -1


def ver_ingredientes():
    idx = seleccionar_postre(buscar_todos_postres(input("Nombre del postre: ")), "ver")
    if idx != -1:
        print(f"\nIngredientes de {POSTRES[idx].nombre}:")
        if not POSTRES[idx].ingredientes:
            print("  Sin ingredientes")
        else:
            for i, ing in enumerate(POSTRES[idx].ingredientes, 1):
                print(f"  {i}. {ing}")


def agregar_ingrediente():
    idx = seleccionar_postre(buscar_todos_postres(input("Nombre del postre: ")), "agregar")
    if idx != -1:
        ing = input("Nuevo ingrediente: ")
        if ing in POSTRES[idx].ingredientes:
            print("Error: El ingrediente ya existe")
        else:
            POSTRES[idx].ingredientes.append(ing)
            print(f"'{ing}' agregado")


def eliminar_ingrediente():
    idx = seleccionar_postre(buscar_todos_postres(input("Nombre del postre: ")), "eliminar")
    if idx != -1 and POSTRES[idx].ingredientes:
        print("Ingredientes:", ", ".join(f"{i+1}.{v}" for i,v in enumerate(POSTRES[idx].ingredientes)))
        ing = input("Ingrediente a eliminar (Nombre): ")
        if ing in POSTRES[idx].ingredientes:
            POSTRES[idx].ingredientes.remove(ing)
            print(f"'{ing}' eliminado")
        else:
            print("Error: No existe")


def modificar_ingredientes():
    idx = seleccionar_postre(buscar_todos_postres(input("Nombre del postre: ")), "modificar")
    if idx != -1:
        print("\n1. Reemplazar todo  2. Corregir uno")
        print("--- (Escoge un numero) ---")
        op = input("Opción: ")
        if op == "1":
            nuevos = []
            print("Nuevos ingredientes (vacío para terminar):")
            while True:
                ing = input("Ingrediente: ")
                if not ing: break
                if ing not in nuevos:
                    nuevos.append(ing)
            POSTRES[idx].ingredientes = nuevos
            print("Ingredientes reemplazados")
        elif op == "2" and POSTRES[idx].ingredientes:
            for i, ing in enumerate(POSTRES[idx].ingredientes, 1):
                print(f"{i}. {ing}")
            try:
                num = int(input("Número a corregir: ")) - 1
                if 0 <= num < len(POSTRES[idx].ingredientes):
                    POSTRES[idx].ingredientes[num] = input("Nuevo valor: ")
                    print("Corregido")
            except: print("Error")


def alta_postre():
    nombre = input("Nombre del nuevo postre: ")
    ingredientes = []
    print("Ingredientes (vacío para terminar):")
    while True:
        ing = input("Ingrediente: ")
        if not ing: break
        if ing not in ingredientes:
            ingredientes.append(ing)
    POSTRES.append(Postre(nombre, ingredientes))
    POSTRES.sort(key=lambda x: x.nombre)
    print(f"'{nombre}' agregado")


def baja_postre():
    idx = seleccionar_postre(buscar_todos_postres(input("Nombre del postre: ")), "eliminar")
    if idx != -1 and input(f"¿Eliminar '{POSTRES[idx].nombre}'? (s/n): ").lower() == 's':
        POSTRES.pop(idx)
        print("Postre eliminado")


def eliminar_repetidos():
    print("\n--- Eliminando repetidos ---")
    repetidos = False
    i = 0
    while i < len(POSTRES):
        j = i + 1
        while j < len(POSTRES):
            if POSTRES[i].nombre.lower() == POSTRES[j].nombre.lower():
                repetidos = True
                print(f"Repetido: '{POSTRES[i].nombre}'")
                print(f"  {i}: {POSTRES[i].ingredientes}")
                print(f"  {j}: {POSTRES[j].ingredientes}")
                print("1. Mantener 1°  2. Mantener 2°  3. Fusionar")
                op = input("Opción: ")
                if op == "1":
                    POSTRES.pop(j)
                elif op == "2":
                    POSTRES.pop(i)
                    i -= 1
                    break
                elif op == "3":
                    POSTRES[i].ingredientes = list(set(POSTRES[i].ingredientes + POSTRES[j].ingredientes))
                    POSTRES.pop(j)
                j = i + 1
            else:
                j += 1
        i += 1
    if not repetidos:
        print("No hay repetidos")
    else:
        print("\nConclusión: Al eliminar repetidos se pueden perder ingredientes si no se fusionan")
    mostrar_todos_postres()


def mostrar_todos_postres():
    if not POSTRES:
        print("No hay postres")
    else:
        print("--- Postres Registrados ---")
        for i, p in enumerate(POSTRES):
            print(f"{i+1}. {p.nombre} - {len(p.ingredientes)} ingredientes")


def main():

    # Datos de ejemplo
    POSTRES.extend([
        Postre("Pastel de Chocolate", ["harina", "huevos", "chocolate", "azucar"]),
        Postre("Flan", ["huevos", "leche", "azucar", "vainilla"]),
        Postre("Helado", ["leche", "azucar", "crema"])
    ])
    POSTRES.sort(key=lambda x: x.nombre)
    
    while True:
        mostrar_menu()
        op = input("Opción: ")
        if op == "1": ver_ingredientes()
        elif op == "2": agregar_ingrediente()
        elif op == "3": eliminar_ingrediente()
        elif op == "4": modificar_ingredientes()
        elif op == "5": alta_postre()
        elif op == "6": baja_postre()
        elif op == "7": eliminar_repetidos()
        elif op == "8": mostrar_todos_postres()
        elif op == "9": print("¡Adiós!"); break
        else: print("Opción inválida")

if __name__ == "__main__":
    main()