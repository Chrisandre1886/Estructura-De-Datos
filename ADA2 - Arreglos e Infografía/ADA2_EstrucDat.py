import random
import os


NUM_ALUMNOS = NUM_MATERIAS = 0
materias = []
calificaciones = []


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
        
        print(f"\nGenerando {NUM_MATERIAS} materias...")
        materias_set = set()
        while len(materias) < NUM_MATERIAS:
            nombre = f"{random.choice(prefijos)} {random.choice(temas)} {random.choice(niveles)}"
            if nombre not in materias_set:
                materias.append(nombre)
                materias_set.add(nombre)
        
        print(f"Generando calificaciones para {NUM_ALUMNOS} alumnos...")
        calificaciones = [[random.randint(0, 100) for _ in range(NUM_MATERIAS)] for _ in range(NUM_ALUMNOS)]
        
        print(f"\n✅ Sistema inicializado - Alumnos: {NUM_ALUMNOS} | Materias: {NUM_MATERIAS}")
        return True
    except ValueError:
        print("❌ Error: Debe ingresar números válidos.")
        return False

def mostrar_menu():
    print(f"\n{'='*60}\nSISTEMA DE GESTIÓN DE CALIFICACIONES")
    print(f"Alumnos: {NUM_ALUMNOS} | Materias: {NUM_MATERIAS}")
    
    print(f"{'='*60}\n1. Buscar calificación de un alumno en una materia")
    print("2. Visualizar todas las calificaciones (tabla completa)")
    print(f"3. Salir\n{'='*60}")

def buscar_calificacion():
    try:
        alumno = int(input(f"\nIngrese el número de alumno (1-{NUM_ALUMNOS}): ")) - 1
        if not (0 <= alumno < NUM_ALUMNOS):
            print(f"❌ Número inválido. Debe estar entre 1 y {NUM_ALUMNOS}.")
            return
        
        print("\n¿Cómo desea buscar?\n1. Por número de materia\n2. Por nombre/palabra clave")
        opcion = input("\nOpción: ")
        
        if opcion == "1":
            materia_num = int(input(f"\nIngrese el número de materia (1-{NUM_MATERIAS}): ")) - 1
            if not (0 <= materia_num < NUM_MATERIAS):
                print(f"❌ Número inválido. Debe estar entre 1 y {NUM_MATERIAS}.")
                return
            print(f"\n✅ Alumno {alumno + 1} - {materias[materia_num]}: {calificaciones[alumno][materia_num]}")
            
        elif opcion == "2":
            palabra = input("\nIngrese palabra clave: ").lower()
            resultados = [(i, m) for i, m in enumerate(materias) if palabra in m.lower()]
            
            if not resultados:
                print("❌ No se encontraron materias.")
                return
            
            print("\nMaterias encontradas:")
            for i, (idx, nombre) in enumerate(resultados[:20], 1):
                print(f"{i}. [{idx+1}] {nombre}")
            if len(resultados) > 20:
                print(f"\n... y {len(resultados)-20} más")
            
            seleccion = int(input(f"\nSeleccione materia (1-{min(len(resultados), 20)}): ")) - 1
            if not (0 <= seleccion < len(resultados)):
                print("❌ Selección inválida.")
                return
            
            materia_idx = resultados[seleccion][0]
            print(f"\n✅ Alumno {alumno + 1} - {materias[materia_idx]}: {calificaciones[alumno][materia_idx]}")
    except ValueError:
        print("❌ Error: Debe ingresar un número válido.")

def visualizar_todas():
    print(f"\nADVERTENCIA: {NUM_ALUMNOS} alumnos y {NUM_MATERIAS} materias.")
    print("\nSeleccione orientación de la tabla:")
    print("1. Alumnos en filas, Materias en columnas (tradicional)")
    print("2. Materias en filas, Alumnos en columnas (transpuesta)")
    
    orientacion = input("\nOrientación: ")
    
    if orientacion not in ["1", "2"]:
        print("❌ Opción inválida.")
        return
    
    print("\nSeleccione formato de visualización:")
    print("1. Vista rápida (10x10)\n2. Rango de alumnos (todas las materias)" if orientacion == "1" 
          else "1. Vista rápida (10x10)\n2. Rango de materias (todos los alumnos)")
    print("3. Rango personalizado\n4. Estadísticas generales")
    
    opcion = input("\nOpción: ")
    
    if opcion == "1":
        if orientacion == "1":
            mostrar_tabla_alumnos_filas(0, min(10, NUM_ALUMNOS), 0, min(10, NUM_MATERIAS))
        else:
            mostrar_tabla_materias_filas(0, min(10, NUM_MATERIAS), 0, min(10, NUM_ALUMNOS))
    elif opcion == "2":
        try:
            if orientacion == "1":
                inicio = int(input(f"Alumno inicial (1-{NUM_ALUMNOS}): ")) - 1
                fin = int(input(f"Alumno final (1-{NUM_ALUMNOS}): "))
                if 0 <= inicio < fin <= NUM_ALUMNOS:
                    mostrar_tabla_alumnos_filas(inicio, fin, 0, NUM_MATERIAS)
                else:
                    print("❌ Rango inválido.")
            else:
                inicio = int(input(f"Materia inicial (1-{NUM_MATERIAS}): ")) - 1
                fin = int(input(f"Materia final (1-{NUM_MATERIAS}): "))
                if 0 <= inicio < fin <= NUM_MATERIAS:
                    mostrar_tabla_materias_filas(inicio, fin, 0, NUM_ALUMNOS)
                else:
                    print("❌ Rango inválido.")
        except ValueError:
            print("❌ Debe ingresar números válidos.")
    elif opcion == "3":
        try:
            if orientacion == "1":
                inicio_al = int(input(f"Alumno inicial (1-{NUM_ALUMNOS}): ")) - 1
                fin_al = int(input(f"Alumno final (1-{NUM_ALUMNOS}): "))
                inicio_mat = int(input(f"Materia inicial (1-{NUM_MATERIAS}): ")) - 1
                fin_mat = int(input(f"Materia final (1-{NUM_MATERIAS}): "))
                
                if (0 <= inicio_al < fin_al <= NUM_ALUMNOS and 0 <= inicio_mat < fin_mat <= NUM_MATERIAS):
                    mostrar_tabla_alumnos_filas(inicio_al, fin_al, inicio_mat, fin_mat)
                else:
                    print("❌ Rango inválido.")
            else:
                inicio_mat = int(input(f"Materia inicial (1-{NUM_MATERIAS}): ")) - 1
                fin_mat = int(input(f"Materia final (1-{NUM_MATERIAS}): "))
                inicio_al = int(input(f"Alumno inicial (1-{NUM_ALUMNOS}): ")) - 1
                fin_al = int(input(f"Alumno final (1-{NUM_ALUMNOS}): "))
                
                if (0 <= inicio_mat < fin_mat <= NUM_MATERIAS and 0 <= inicio_al < fin_al <= NUM_ALUMNOS):
                    mostrar_tabla_materias_filas(inicio_mat, fin_mat, inicio_al, fin_al)
                else:
                    print("❌ Rango inválido.")
        except ValueError:
            print("❌ Debe ingresar números válidos.")
    elif opcion == "4":
        mostrar_estadisticas()
    else:
        print("❌ Opción inválida.")

def mostrar_tabla_alumnos_filas(inicio_al, fin_al, inicio_mat, fin_mat):
    """Tabla tradicional: Alumnos en filas, Materias en columnas"""
    max_mat = min(fin_mat - inicio_mat, 15)
    if fin_mat - inicio_mat > max_mat:
        print(f"\n⚠️  Mostrando solo {max_mat} materias")
        fin_mat = inicio_mat + max_mat
    
    print(f"\n{'Alumno':<8}", end="")
    for j in range(inicio_mat, fin_mat):
        print(f"{materias[j][:12]:<14}", end="")
    print(f"{'Prom.':<8}\n{'='*(8 + 14*(fin_mat-inicio_mat) + 8)}")
    
    for i in range(inicio_al, fin_al):
        print(f"{i+1:<8}", end="")
        for j in range(inicio_mat, fin_mat):
            print(f"{calificaciones[i][j]:<14}", end="")
        print(f"{sum(calificaciones[i])/NUM_MATERIAS:<8.2f}")
    
    print("="*(8 + 14*(fin_mat-inicio_mat) + 8))

def mostrar_tabla_materias_filas(inicio_mat, fin_mat, inicio_al, fin_al):
    """Tabla transpuesta: Materias en filas, Alumnos en columnas"""
    max_al = min(fin_al - inicio_al, 15)
    if fin_al - inicio_al > max_al:
        print(f"\n⚠️  Mostrando solo {max_al} alumnos")
        fin_al = inicio_al + max_al
    
    print(f"\n{'Materia':<35}", end="")
    for i in range(inicio_al, fin_al):
        print(f"Al{i+1:<4}", end="  ")
    print(f"{'Prom.':<8}\n{'='*(35 + 6*(fin_al-inicio_al) + 8)}")
    
    for j in range(inicio_mat, fin_mat):
        print(f"{materias[j][:33]:<35}", end="")
        suma_materia = 0
        for i in range(inicio_al, fin_al):
            calif = calificaciones[i][j]
            suma_materia += calif
            print(f"{calif:<6}", end="")
        promedio_materia = sum(calificaciones[i][j] for i in range(NUM_ALUMNOS)) / NUM_ALUMNOS
        print(f"{promedio_materia:<8.2f}")
    
    print("="*(35 + 6*(fin_al-inicio_al) + 8))
    
    print(f"{'PROMEDIO POR ALUMNO':<35}", end="")
    for i in range(inicio_al, fin_al):
        promedio_alumno = sum(calificaciones[i]) / NUM_MATERIAS
        print(f"{promedio_alumno:<6.2f}", end="")
    print()
    print("="*(35 + 6*(fin_al-inicio_al) + 8))

def mostrar_estadisticas():
    suma_total = sum(sum(row) for row in calificaciones)
    total_calif = NUM_ALUMNOS * NUM_MATERIAS
    promedio_general = suma_total / total_calif
    aprobados = sum(1 for row in calificaciones for c in row if c >= 60)
    
    print(f"\n{'='*60}\nESTADÍSTICAS GENERALES\n{'='*60}")
    print(f"\nTotal de calificaciones: {total_calif:,}")
    print(f"Promedio general: {promedio_general:.2f}")
    print(f"Calificación máxima: {max(max(row) for row in calificaciones)}")
    print(f"Calificación mínima: {min(min(row) for row in calificaciones)}")
    print(f"\nAprobadas (≥60): {aprobados:,} ({aprobados*100/total_calif:.2f}%)")
    print(f"Reprobadas (<60): {total_calif-aprobados:,} ({(total_calif-aprobados)*100/total_calif:.2f}%)")
    
    promedios = sorted([(i+1, sum(calificaciones[i])/NUM_MATERIAS) for i in range(NUM_ALUMNOS)], 
                       key=lambda x: x[1], reverse=True)
    
    print(f"\n{'-'*60}\nTOP {min(5, NUM_ALUMNOS)} ALUMNOS:\n{'-'*60}")
    for i, (alumno, prom) in enumerate(promedios[:5], 1):
        print(f"{i}. Alumno {alumno}: {prom:.2f}")
    print("="*60)

def main():
    if not inicializar_sistema():
        print("\n❌ No se pudo inicializar el sistema.")
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
            print("❌ Opción inválida.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()