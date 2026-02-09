import random
import os

# Variables globales
NUM_ALUMNOS = 0
NUM_MATERIAS = 0
materias = []
calificaciones = []

# Listas para generar nombres de materias aleatorias
prefijos = ["Fundamentos de", "Introducción a", "Teoría de", "Práctica de", "Análisis de", 
            "Seminario de", "Taller de", "Laboratorio de", "Metodología de", "Historia de"]

temas = ["Programación", "Matemáticas", "Física", "Química", "Biología", "Economía", 
         "Administración", "Derecho", "Filosofía", "Psicología", "Sociología", "Estadística",
         "Electrónica", "Mecánica", "Arquitectura", "Diseño", "Literatura", "Arte",
         "Música", "Geografía", "Geología", "Astronomía", "Antropología", "Ingeniería",
         "Computación", "Redes", "Bases de Datos", "Inteligencia Artificial", "Robótica",
         "Contabilidad", "Finanzas", "Marketing", "Logística", "Producción"]

niveles = ["I", "II", "III", "IV", "V", "Avanzado", "Básico", "Intermedio"]

def inicializar_sistema():
    """Solicita al usuario la cantidad de alumnos y materias e inicializa el sistema"""
    global NUM_ALUMNOS, NUM_MATERIAS, materias, calificaciones
    
    print("\n" + "="*60)
    print("CONFIGURACIÓN INICIAL DEL SISTEMA")
    print("="*60)
    
    try:
        NUM_ALUMNOS = int(input("\nIngrese la cantidad de alumnos: "))
        NUM_MATERIAS = int(input("Ingrese la cantidad de materias: "))
        
        if NUM_ALUMNOS <= 0 or NUM_MATERIAS <= 0:
            print("❌ Error: Las cantidades deben ser mayores a cero.")
            return False
        
        # Generar materias únicas
        materias = []
        materias_generadas = set()
        
        print(f"\nGenerando {NUM_MATERIAS} materias...")
        
        while len(materias) < NUM_MATERIAS:
            prefijo = random.choice(prefijos)
            tema = random.choice(temas)
            nivel = random.choice(niveles)
            nombre_materia = f"{prefijo} {tema} {nivel}"
            
            if nombre_materia not in materias_generadas:
                materias.append(nombre_materia)
                materias_generadas.add(nombre_materia)
        
        # Generar calificaciones aleatorias (0-100)
        print(f"Generando calificaciones para {NUM_ALUMNOS} alumnos...")
        calificaciones = [[random.randint(0, 100) for _ in range(NUM_MATERIAS)] for _ in range(NUM_ALUMNOS)]
        
        print(f"\n✅ Sistema inicializado correctamente!")
        print(f"   - Alumnos: {NUM_ALUMNOS}")
        print(f"   - Materias: {NUM_MATERIAS}")
        
        return True
        
    except ValueError:
        print("❌ Error: Debe ingresar números válidos.")
        return False

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n" + "="*60)
    print("SISTEMA DE GESTIÓN DE CALIFICACIONES")
    print(f"Alumnos: {NUM_ALUMNOS} | Materias: {NUM_MATERIAS}")
    print("="*60)
    print("1. Buscar calificación de un alumno en una materia")
    print("2. Visualizar todas las calificaciones (tabla completa)")
    print("3. Salir")
    print("="*60)

def buscar_calificacion():
    try:
        alumno = int(input(f"\nIngrese el número de alumno (1-{NUM_ALUMNOS}): ")) - 1
        
        if alumno < 0 or alumno >= NUM_ALUMNOS:
            print(f"❌ Número de alumno inválido. Debe estar entre 1 y {NUM_ALUMNOS}.")
            return
        
        print("\n¿Cómo desea buscar la materia?")
        print("1. Por número de materia")
        print("2. Buscar por nombre/palabra clave")
        
        opcion = input("\nOpción: ")
        
        if opcion == "1":
            materia_num = int(input(f"\nIngrese el número de materia (1-{NUM_MATERIAS}): ")) - 1
            
            if materia_num < 0 or materia_num >= NUM_MATERIAS:
                print(f"❌ Número de materia inválido. Debe estar entre 1 y {NUM_MATERIAS}.")
                return
            
            calificacion = calificaciones[alumno][materia_num]
            print(f"\n✅ Alumno {alumno + 1} - {materias[materia_num]}: {calificacion}")
            
        elif opcion == "2":
            palabra = input("\nIngrese palabra clave para buscar materia: ").lower()
            resultados = [(i, m) for i, m in enumerate(materias) if palabra in m.lower()]
            
            if not resultados:
                print("❌ No se encontraron materias con esa palabra clave.")
                return
            
            print("\nMaterias encontradas:")
            for i, (idx, nombre) in enumerate(resultados[:20], 1):  # Limitar a 20 resultados
                print(f"{i}. [{idx+1}] {nombre}")
            
            if len(resultados) > 20:
                print(f"\n... y {len(resultados)-20} más")
            
            seleccion = int(input(f"\nSeleccione materia (1-{min(len(resultados), 20)}): ")) - 1
            
            if seleccion < 0 or seleccion >= len(resultados):
                print("❌ Selección inválida.")
                return
            
            materia_idx = resultados[seleccion][0]
            calificacion = calificaciones[alumno][materia_idx]
            print(f"\n✅ Alumno {alumno + 1} - {materias[materia_idx]}: {calificacion}")
        
    except ValueError:
        print("❌ Error: Debe ingresar un número válido.")

def visualizar_todas():
    print(f"\nADVERTENCIA: Hay {NUM_ALUMNOS} alumnos y {NUM_MATERIAS} materias.")
    print("\nSeleccione formato de visualización:")
    print("1. Primeros 10 alumnos y primeras 10 materias (vista rápida)")
    print("2. Rango personalizado de alumnos (todas las materias)")
    print("3. Rango personalizado de alumnos y materias")
    print("4. Estadísticas generales")
    
    opcion = input("\nOpción: ")
    
    if opcion == "1":
        max_alumnos = min(10, NUM_ALUMNOS)
        max_materias = min(10, NUM_MATERIAS)
        mostrar_tabla(0, max_alumnos, 0, max_materias)
    elif opcion == "2":
        try:
            inicio = int(input(f"Alumno inicial (1-{NUM_ALUMNOS}): ")) - 1
            fin = int(input(f"Alumno final (1-{NUM_ALUMNOS}): "))
            if inicio < 0 or fin > NUM_ALUMNOS or inicio >= fin:
                print("❌ Rango inválido.")
                return
            mostrar_tabla(inicio, fin, 0, NUM_MATERIAS)
        except ValueError:
            print("❌ Debe ingresar números válidos.")
    elif opcion == "3":
        try:
            inicio_al = int(input(f"Alumno inicial (1-{NUM_ALUMNOS}): ")) - 1
            fin_al = int(input(f"Alumno final (1-{NUM_ALUMNOS}): "))
            inicio_mat = int(input(f"Materia inicial (1-{NUM_MATERIAS}): ")) - 1
            fin_mat = int(input(f"Materia final (1-{NUM_MATERIAS}): "))
            
            if (inicio_al < 0 or fin_al > NUM_ALUMNOS or inicio_al >= fin_al or
                inicio_mat < 0 or fin_mat > NUM_MATERIAS or inicio_mat >= fin_mat):
                print("❌ Rango inválido.")
                return
            
            mostrar_tabla(inicio_al, fin_al, inicio_mat, fin_mat)
        except ValueError:
            print("❌ Debe ingresar números válidos.")
    elif opcion == "4":
        mostrar_estadisticas()
    else:
        print("❌ Opción inválida.")

def mostrar_tabla(inicio_al, fin_al, inicio_mat, fin_mat):
    # Limitar materias mostradas para no sobrecargar pantalla
    max_materias_mostrar = min(fin_mat - inicio_mat, 15)
    
    if fin_mat - inicio_mat > max_materias_mostrar:
        print(f"\n⚠️  Mostrando solo las primeras {max_materias_mostrar} materias del rango seleccionado")
        fin_mat = inicio_mat + max_materias_mostrar
    
    # Encabezado
    print(f"\n{'Alumno':<8}", end="")
    for j in range(inicio_mat, fin_mat):
        nombre_corto = materias[j][:12]
        print(f"{nombre_corto:<14}", end="")
    print(f"{'Prom.':<8}")
    print("="*(8 + 14*(fin_mat-inicio_mat) + 8))
    
    # Mostrar calificaciones
    for i in range(inicio_al, fin_al):
        print(f"{i+1:<8}", end="")
        suma = 0
        for j in range(inicio_mat, fin_mat):
            calif = calificaciones[i][j]
            suma += calif
            print(f"{calif:<14}", end="")
        promedio = sum(calificaciones[i]) / NUM_MATERIAS
        print(f"{promedio:<8.2f}")
    
    print("="*(8 + 14*(fin_mat-inicio_mat) + 8))

def mostrar_estadisticas():
    print("\n" + "="*60)
    print("ESTADÍSTICAS GENERALES DEL SISTEMA")
    print("="*60)
    
    # Calcular promedios
    suma_total = sum(sum(row) for row in calificaciones)
    promedio_general = suma_total / (NUM_ALUMNOS * NUM_MATERIAS)
    
    # Contar aprobados/reprobados (considerando 60 como mínima aprobatoria)
    aprobados = sum(1 for row in calificaciones for calif in row if calif >= 60)
    reprobados = (NUM_ALUMNOS * NUM_MATERIAS) - aprobados
    
    # Calificación más alta y más baja
    calif_max = max(max(row) for row in calificaciones)
    calif_min = min(min(row) for row in calificaciones)
    
    print(f"\nTotal de calificaciones: {NUM_ALUMNOS * NUM_MATERIAS:,}")
    print(f"Promedio general: {promedio_general:.2f}")
    print(f"Calificación más alta: {calif_max}")
    print(f"Calificación más baja: {calif_min}")
    print(f"\nAprobadas (≥60): {aprobados:,} ({aprobados*100/(NUM_ALUMNOS*NUM_MATERIAS):.2f}%)")
    print(f"Reprobadas (<60): {reprobados:,} ({reprobados*100/(NUM_ALUMNOS*NUM_MATERIAS):.2f}%)")
    
    # Top 5 alumnos
    promedios_alumnos = [(i+1, sum(calificaciones[i])/NUM_MATERIAS) for i in range(NUM_ALUMNOS)]
    promedios_alumnos.sort(key=lambda x: x[1], reverse=True)
    
    print("\n" + "-"*60)
    print(f"TOP {min(5, NUM_ALUMNOS)} ALUMNOS CON MEJOR PROMEDIO:")
    print("-"*60)
    for i, (alumno, promedio) in enumerate(promedios_alumnos[:5], 1):
        print(f"{i}. Alumno {alumno}: {promedio:.2f}")
    
    print("="*60)

# Programa principal
def main():
    # Inicializar el sistema al comenzar
    if not inicializar_sistema():
        print("\n❌ No se pudo inicializar el sistema. Saliendo...")
        return
    
    input("\nPresione Enter para continuar...")
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            buscar_calificacion()
        elif opcion == "2":
            visualizar_todas()
        elif opcion == "3":
            print("\n¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()