class Cola:
    
    def __init__(self):
        self.items = []
    
    def encolar(self, item):
        self.items.append(item)
    
    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def tamano(self):
        return len(self.items)
    
    def ver_primero(self):
        if not self.esta_vacia():
            return self.items[0]
        return None
    
    def __str__(self):
        return str(self.items)


class SistemaColasSeguros:
    
    def __init__(self):
        self.colas = {}
        self.contadores = {}
        self.numero_servicios = 5  
        
        for i in range(1, self.numero_servicios + 1):
            self.colas[i] = Cola()
            self.contadores[i] = 0
    
    def generar_numero_atencion(self, servicio):
        self.contadores[servicio] += 1
        return f"{servicio}-{self.contadores[servicio]:03d}"
    
    def llegada_cliente(self, servicio):
        
        try:
            servicio = int(servicio)
            if servicio < 1 or servicio > self.numero_servicios:
                print(f"Error: Servicio debe estar entre 1 y {self.numero_servicios}")
                return
            
            numero_atencion = self.generar_numero_atencion(servicio)
            
            self.colas[servicio].encolar(numero_atencion)
            
            print(f"Cliente agregado a la cola de servicio {servicio}")
            print(f"Número de atención asignado: {numero_atencion}")
            print(f"Clientes en espera para servicio {servicio}: {self.colas[servicio].tamano()}")
            
        except ValueError:
            print("Error: El número de servicio debe ser un valor numérico")
    
    def atender_cliente(self, servicio):
        
        try:
            servicio = int(servicio)
            if servicio < 1 or servicio > self.numero_servicios:
                print(f"Error: Servicio debe estar entre 1 y {self.numero_servicios}")
                return
            
            if self.colas[servicio].esta_vacia():
                print(f"No hay clientes en espera para el servicio {servicio}")
                return
            
            cliente_atendido = self.colas[servicio].desencolar()
            
            print(f"Llamando a cliente: {cliente_atendido}")
            print(f"Clientes restantes en servicio {servicio}: {self.colas[servicio].tamano()}")
            
        except ValueError:
            print("Error: El número de servicio debe ser un valor numérico")
    
    def mostrar_estado(self):
        print("\n" + "="*50)
        print("ESTADO ACTUAL DE LAS COLAS")
        print("="*50)
        
        for servicio in range(1, self.numero_servicios + 1):
            tamano = self.colas[servicio].tamano()
            print(f"Servicio {servicio}: {tamano} cliente(s) en espera")
            if not self.colas[servicio].esta_vacia():
                print(f"  - Siguiente: {self.colas[servicio].ver_primero()}")
        
        print("="*50)


def main():
    sistema = SistemaColasSeguros()
    
    print("\n" + "="*50)
    print("SISTEMA DE COLAS - COMPAÑÍA DE SEGUROS")
    print("="*50)
    print("Comandos disponibles:")
    print("  C [n]  - Llegada de cliente para servicio n (1-5)")
    print("  A [n]  - Atender cliente de servicio n (1-5)")
    print("  E      - Mostrar estado de todas las colas")
    print("  Q      - Salir del sistema")
    print("="*50)
    
    while True:
        try:
            comando = input("\nIngrese comando: ").strip().upper()
            
            if not comando:
                continue
            
            if comando == 'Q':
                print("Saliendo del sistema...")
                break
            
            elif comando == 'E':
                sistema.mostrar_estado()
            
            elif len(comando) >= 3 and comando[0] in ['C', 'A'] and comando[1] == ' ':
                tipo = comando[0]
                parametro = comando[2:].strip()
                
                if tipo == 'C':
                    sistema.llegada_cliente(parametro)
                elif tipo == 'A':
                    sistema.atender_cliente(parametro)
            
            else:
                print("Comando no válido. Use C, A, E o Q.")
                
        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")


if __name__ == "__main__":

    main()

