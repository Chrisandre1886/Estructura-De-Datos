
ventas = [
    [0, 0, 0],  # Enero
    [0, 0, 0],  # Febrero
    [0, 0, 0],  # Marzo
    [0, 0, 0],  # Abril
    [0, 0, 0],  # Mayo
    [0, 0, 0],  # Junio
    [0, 0, 0],  # Julio
    [0, 0, 0],  # Agosto
    [0, 0, 0],  # Septiembre
    [0, 0, 0],  # Octubre
    [0, 0, 0],  # Noviembre
    [0, 0, 0]   # Diciembre
]

meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
departamentos = ["Ropa", "Deportes", "Juguetería"]


def insertar_venta(mes_idx, depto_idx, monto):
    """
    Inserta una venta en el arreglo
    mes_idx: índice del mes (0-11)
    depto_idx: índice del departamento (0-2)
    monto: cantidad de la venta
    """
    if 0 <= mes_idx < 12 and 0 <= depto_idx < 3:
        ventas[mes_idx][depto_idx] = monto
        print(f"✓ Venta registrada: {meses[mes_idx]} - {departamentos[depto_idx]}: ${monto}")
        return True
    else:
        print("✗ Error: Índices fuera de rango")
        return False


def buscar_venta(mes_idx, depto_idx):
    """
    Busca y retorna una venta específica
    mes_idx: índice del mes (0-11)
    depto_idx: índice del departamento (0-2)
    """
    if 0 <= mes_idx < 12 and 0 <= depto_idx < 3:
        monto = ventas[mes_idx][depto_idx]
        print(f"Venta encontrada: {meses[mes_idx]} - {departamentos[depto_idx]}: ${monto}")
        return monto
    else:
        print("✗ Error: Índices fuera de rango")
        return None


def eliminar_venta(mes_idx, depto_idx):
    """
    Elimina (pone en 0) una venta de un departamento específico
    mes_idx: índice del mes (0-11)
    depto_idx: índice del departamento (0-2)
    """
    if 0 <= mes_idx < 12 and 0 <= depto_idx < 3:
        monto_anterior = ventas[mes_idx][depto_idx]
        ventas[mes_idx][depto_idx] = 0
        print(f"✓ Venta eliminada: {meses[mes_idx]} - {departamentos[depto_idx]} (era ${monto_anterior})")
        return True
    else:
        print("✗ Error: Índices fuera de rango")
        return False


def mostrar_ventas():
    """Muestra todas las ventas en formato de tabla"""
    print("\n" + "="*60)
    print(f"{'Mes':<15} {'Ropa':<15} {'Deportes':<15} {'Juguetería':<15}")
    print("="*60)
    for i in range(12):
        print(f"{meses[i]:<15} ${ventas[i][0]:<14} ${ventas[i][1]:<14} ${ventas[i][2]:<14}")
    print("="*60 + "\n")


def main():
    print("="*60)
    print("SISTEMA DE GESTIÓN DE VENTAS MENSUALES")
    print("="*60)
    
    while True:
        print("\n--- MENÚ ---")
        print("1. Insertar venta")
        print("2. Buscar venta")
        print("3. Eliminar venta")
        print("4. Mostrar todas las ventas")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ")
        
        if opcion == "1":
            print("\nMeses disponibles:")
            for i, mes in enumerate(meses):
                print(f"{i}. {mes}")
            mes_idx = int(input("Selecciona el mes (0-11): "))
            
            print("\nDepartamentos disponibles:")
            for i, depto in enumerate(departamentos):
                print(f"{i}. {depto}")
            depto_idx = int(input("Selecciona el departamento (0-2): "))
            
            monto = float(input("Ingresa el monto de la venta: $"))
            insertar_venta(mes_idx, depto_idx, monto)
            
        elif opcion == "2":
            print("\nMeses disponibles:")
            for i, mes in enumerate(meses):
                print(f"{i}. {mes}")
            mes_idx = int(input("Selecciona el mes (0-11): "))
            
            print("\nDepartamentos disponibles:")
            for i, depto in enumerate(departamentos):
                print(f"{i}. {depto}")
            depto_idx = int(input("Selecciona el departamento (0-2): "))
            
            buscar_venta(mes_idx, depto_idx)
            
        elif opcion == "3":
            print("\nMeses disponibles:")
            for i, mes in enumerate(meses):
                print(f"{i}. {mes}")
            mes_idx = int(input("Selecciona el mes (0-11): "))
            
            print("\nDepartamentos disponibles:")
            for i, depto in enumerate(departamentos):
                print(f"{i}. {depto}")
            depto_idx = int(input("Selecciona el departamento (0-2): "))
            
            eliminar_venta(mes_idx, depto_idx)
            
        elif opcion == "4":
            mostrar_ventas()
            
        elif opcion == "5":
            print("\n¡Hasta luego!")
            break
            
        else:
            print("✗ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    main()