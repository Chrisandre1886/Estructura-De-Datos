class Node:
    """Representa un nodo de la lista enlazada para la cola."""
    
    def __init__(self, info):
        self.info = info      
        self.next = None      


class Queue:
    """Implementación de una cola basada en lista enlazada."""
    
    def __init__(self):
        self.front_node = None   
        self.rear_node = None    
        self.count = 0           
    
    def size(self):
        """Retorna el número de elementos en la cola."""
        return self.count
    
    def isEmpty(self):
        """Verifica si la cola está vacía."""
        return self.count == 0
    
    def front(self):
        """Retorna el primer elemento sin eliminarlo. Retorna None si está vacía."""
        if self.isEmpty():
            return None
        return self.front_node.info
    
    def enqueue(self, info):
        """Agrega un nuevo elemento al final de la cola."""
        new_node = Node(info)
        
        if self.isEmpty():
            self.front_node = new_node
            self.rear_node = new_node
        else:
            self.rear_node.next = new_node
            self.rear_node = new_node
        
        self.count += 1
        print(f"Insertado al final: {info}")
    
    def dequeue(self):
        """Elimina y retorna el primer elemento. Retorna None si está vacía."""
        if self.isEmpty():
            print("La cola está vacía, no se puede eliminar")
            return None
        
        info = self.front_node.info
        self.front_node = self.front_node.next
        self.count -= 1
        
        # Si la cola quedó vacía, rear_node también debe ser None
        if self.isEmpty():
            self.rear_node = None
            
        print(f"Eliminado del frente: {info}")
        return info
    
    def insertAtPosition(self, pos, info):
        """
        Inserta un elemento en una posición específica.
        Posiciones válidas: 0 a size()
        """
        if pos < 0 or pos > self.count:
            print(f"Error: Posición {pos} fuera de rango. Debe ser entre 0 y {self.count}")
            return False
        
        new_node = Node(info)
        
        # Insertar al frente (posición 0)
        if pos == 0:
            new_node.next = self.front_node
            self.front_node = new_node
            if self.isEmpty():
                self.rear_node = new_node
            self.count += 1
            print(f"Insertado en posición {pos}: {info}")
            return True
        
        # Insertar al final (posición == count)
        if pos == self.count:
            self.enqueue(info)
            return True
        
        # Insertar en medio
        current = self.front_node
        for i in range(pos - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.count += 1
        print(f"Insertado en posición {pos}: {info}")
        return True
    
    def insertMultiple(self, n, data_type="order"):
        """
        Inserta N cantidad de nodos.
        Args:
            n: Número de nodos a insertar
            data_type: Tipo de datos a insertar ("order" o "simple")
        """
        if n <= 0:
            print("Error: La cantidad debe ser mayor a 0")
            return False
        
        print(f"\n--- Insertando {n} elementos ---")
        for i in range(n):
            if data_type == "order":
                order_id = 200 + i + 1
                description = input(f"  Descripción para Order {order_id}: ")
                self.enqueue(Order(order_id, description))
            else:
                value = input(f"  Valor {i+1}: ")
                self.enqueue(value)
        
        print(f"✅ {n} elementos insertados correctamente")
        return True
    
    def insertMultipleAtPosition(self, n, pos, data_type="order"):
        """
        Inserta N cantidad de nodos en una posición específica.
        Args:
            n: Número de nodos a insertar
            pos: Posición inicial donde insertar
            data_type: Tipo de datos a insertar
        """
        if n <= 0:
            print("Error: La cantidad debe ser mayor a 0")
            return False
        
        if pos < 0 or pos > self.count:
            print(f"Error: Posición {pos} fuera de rango. Debe ser entre 0 y {self.count}")
            return False
        
        print(f"\n--- Insertando {n} elementos en posición {pos} ---")
        current_pos = pos
        for i in range(n):
            if data_type == "order":
                order_id = 300 + i + 1
                description = input(f"  Descripción para Order {order_id}: ")
                self.insertAtPosition(current_pos, Order(order_id, description))
            else:
                value = input(f"  Valor {i+1}: ")
                self.insertAtPosition(current_pos, value)
            current_pos += 1
        
        print(f"✅ {n} elementos insertados en posición {pos} correctamente")
        return True
    
    def deleteAtPosition(self, pos):
        """
        Elimina un elemento en una posición específica.
        Posiciones válidas: 0 a size()-1
        """
        if self.isEmpty():
            print("Error: La cola está vacía")
            return None
        
        if pos < 0 or pos >= self.count:
            print(f"Error: Posición {pos} fuera de rango. Debe ser entre 0 y {self.count-1}")
            return None
        
        # Eliminar del frente (posición 0)
        if pos == 0:
            return self.dequeue()
        
        # Eliminar de otra posición
        current = self.front_node
        for i in range(pos - 1):
            current = current.next
        
        info_eliminado = current.next.info
        current.next = current.next.next
        self.count -= 1
        
        # Si eliminamos el último, actualizar rear_node
        if current.next is None:
            self.rear_node = current
        
        print(f"Eliminado de posición {pos}: {info_eliminado}")
        return info_eliminado
    
    def deleteMultiple(self, n, desde_frente=True):
        """
        Elimina N cantidad de nodos.
        Args:
            n: Número de nodos a eliminar
            desde_frente: True para eliminar desde el frente, False para eliminar desde el final
        """
        if n <= 0:
            print("Error: La cantidad debe ser mayor a 0")
            return 0
        
        if self.isEmpty():
            print("Error: La cola está vacía")
            return 0
        
        if n > self.count:
            print(f"⚠️ Solo hay {self.count} elementos. Se eliminarán todos.")
            n = self.count
        
        eliminados = 0
        print(f"\n--- Eliminando {n} elementos {'desde el frente' if desde_frente else 'desde el final'} ---")
        
        if desde_frente:
            for i in range(n):
                self.dequeue()
                eliminados += 1
        else:
            # Eliminar desde el final requiere eliminar posiciones específicas
            for i in range(n):
                if not self.isEmpty():
                    self.deleteAtPosition(self.count - 1)
                    eliminados += 1
        
        print(f"✅ {eliminados} elementos eliminados correctamente")
        return eliminados
    
    def deleteMultipleByPosition(self, n, start_pos):
        """
        Elimina N cantidad de nodos desde una posición inicial.
        Args:
            n: Número de nodos a eliminar
            start_pos: Posición inicial para comenzar a eliminar
        """
        if n <= 0:
            print("Error: La cantidad debe ser mayor a 0")
            return 0
        
        if self.isEmpty():
            print("Error: La cola está vacía")
            return 0
        
        if start_pos < 0 or start_pos >= self.count:
            print(f"Error: Posición {start_pos} fuera de rango. Debe ser entre 0 y {self.count-1}")
            return 0
        
        if start_pos + n > self.count:
            n = self.count - start_pos
            print(f"⚠️ Ajustando a {n} elementos (desde posición {start_pos} hasta el final)")
        
        eliminados = 0
        print(f"\n--- Eliminando {n} elementos desde posición {start_pos} ---")
        
        # Eliminar desde start_pos hacia adelante (las posiciones cambian)
        pos_actual = start_pos
        for i in range(n):
            self.deleteAtPosition(pos_actual)  # Siempre eliminamos en la misma posición
            eliminados += 1
        
        print(f"✅ {eliminados} elementos eliminados desde posición {start_pos}")
        return eliminados
    
    def deleteByValue(self, info):
        """
        Elimina la primera ocurrencia de un valor específico.
        Retorna True si se eliminó, False si no se encontró.
        """
        if self.isEmpty():
            print("La cola está vacía")
            return False
        
        # Si el valor está en el frente
        if self.front_node.info == info:
            self.dequeue()
            return True
        
        # Buscar en el resto de la cola
        current = self.front_node
        while current.next and current.next.info != info:
            current = current.next
        
        if current.next:
            # Encontramos el valor
            current.next = current.next.next
            self.count -= 1
            
            # Si eliminamos el último, actualizar rear_node
            if current.next is None:
                self.rear_node = current
            
            print(f"Eliminado por valor: {info}")
            return True
        else:
            print(f"Valor {info} no encontrado en la cola")
            return False
    
    def insertAfterValue(self, target_info, new_info):
        """
        Inserta un nuevo valor después de la primera ocurrencia de target_info.
        Retorna True si se insertó, False si no se encontró target_info.
        """
        if self.isEmpty():
            print("La cola está vacía")
            return False
        
        current = self.front_node
        while current and current.info != target_info:
            current = current.next
        
        if current:
            new_node = Node(new_info)
            new_node.next = current.next
            current.next = new_node
            self.count += 1
            
            # Si insertamos después del último, actualizar rear_node
            if new_node.next is None:
                self.rear_node = new_node
            
            print(f"Insertado {new_info} después de {target_info}")
            return True
        else:
            print(f"Valor {target_info} no encontrado en la cola")
            return False
    
    def printInfo(self):
        """Presenta información de la cola y sus elementos."""
        print(f"\n=== Información de la Cola ===")
        print(f"Número de elementos: {self.size()}")
        print(f"¿Está vacía?: {self.isEmpty()}")
        print("Contenido de la cola:")
        
        if self.isEmpty():
            print("  (cola vacía)")
        else:
            current = self.front_node
            position = 0
            while current:
                print(f"  Posición {position}: ", end="")
                if hasattr(current.info, 'print'):
                    current.info.print()
                else:
                    print(current.info)
                current = current.next
                position += 1
            print(f"  Frente: {self.front_node.info}")
            print(f"  Final: {self.rear_node.info}")
        print("============================\n")


class Order:
    """Clase de ejemplo para probar la cola con objetos."""
    
    def __init__(self, order_id, description):
        self.order_id = order_id
        self.description = description
    
    def print(self):
        """Método print requerido por Queue.printInfo()"""
        print(f"Order[ID={self.order_id}, Desc='{self.description}']")
    
    def __str__(self):
        return f"Order({self.order_id})"
    
    def __eq__(self, other):
        """Para poder comparar órdenes por ID"""
        if isinstance(other, Order):
            return self.order_id == other.order_id
        return False


class MenuQueue:
    """Clase con menú interactivo para el usuario."""
    
    def __init__(self):
        self.queue = Queue()
        self.ejecutando = True
    
    def mostrar_menu(self):
        """Muestra el menú principal."""
        print("\n" + "="*50)
        print("          MENÚ DE OPERACIONES CON COLA")
        print("="*50)
        print("1. Insertar un elemento (enqueue)")
        print("2. Insertar múltiples elementos (N nodos)")
        print("3. Insertar en posición específica")
        print("4. Insertar múltiples en posición específica")
        print("5. Eliminar un elemento (dequeue)")
        print("6. Eliminar múltiples elementos (N nodos)")
        print("7. Eliminar múltiples desde posición específica")
        print("8. Eliminar por valor")
        print("9. Insertar después de un valor")
        print("10. Ver frente de la cola")
        print("11. Mostrar toda la cola")
        print("12. Tamaño de la cola")
        print("13. Vaciar toda la cola")
        print("14. Ejecutar pruebas predefinidas")
        print("0. Salir")
        print("="*50)
    
    def obtener_n(self, accion="insertar"):
        """Obtiene un número válido del usuario."""
        while True:
            try:
                n = int(input(f"¿Cuántos elementos desea {accion}? "))
                if n > 0:
                    return n
                else:
                    print("Error: Debe ingresar un número positivo.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")
    
    def obtener_posicion(self, mensaje="Ingrese la posición: "):
        """Obtiene una posición válida del usuario."""
        while True:
            try:
                pos = int(input(mensaje))
                return pos
            except ValueError:
                print("Error: Debe ingresar un número válido.")
    
    def obtener_tipo_dato(self):
        """Pregunta al usuario qué tipo de dato desea insertar."""
        print("Tipo de dato a insertar:")
        print("1. Order (objeto con ID y descripción)")
        print("2. Valor simple (string)")
        opcion = input("Seleccione opción (1 o 2): ")
        return "order" if opcion == "1" else "simple"
    
    def ejecutar(self):
        """Ejecuta el menú interactivo."""
        print("=== SISTEMA DE GESTIÓN DE COLA ===\n")
        
        while self.ejecutando:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                # Insertar un elemento
                tipo = self.obtener_tipo_dato()
                if tipo == "order":
                    order_id = int(input("ID de la orden: "))
                    desc = input("Descripción: ")
                    self.queue.enqueue(Order(order_id, desc))
                else:
                    valor = input("Valor a insertar: ")
                    self.queue.enqueue(valor)
            
            elif opcion == "2":
                # Insertar múltiples elementos
                n = self.obtener_n()
                tipo = self.obtener_tipo_dato()
                self.queue.insertMultiple(n, tipo)
            
            elif opcion == "3":
                # Insertar en posición específica
                pos = self.obtener_posicion()
                tipo = self.obtener_tipo_dato()
                if tipo == "order":
                    order_id = int(input("ID de la orden: "))
                    desc = input("Descripción: ")
                    self.queue.insertAtPosition(pos, Order(order_id, desc))
                else:
                    valor = input("Valor a insertar: ")
                    self.queue.insertAtPosition(pos, valor)
            
            elif opcion == "4":
                # Insertar múltiples en posición específica
                pos = self.obtener_posicion("Posición inicial para insertar: ")
                n = self.obtener_n()
                tipo = self.obtener_tipo_dato()
                self.queue.insertMultipleAtPosition(n, pos, tipo)
            
            elif opcion == "5":
                # Eliminar un elemento
                self.queue.dequeue()
            
            elif opcion == "6":
                # Eliminar múltiples elementos
                n = self.obtener_n("eliminar")
                print("¿Desde dónde desea eliminar?")
                print("1. Desde el frente")
                print("2. Desde el final")
                subop = input("Seleccione: ")
                desde_frente = subop == "1"
                self.queue.deleteMultiple(n, desde_frente)
            
            elif opcion == "7":
                # Eliminar múltiples desde posición específica
                n = self.obtener_n("eliminar")
                pos = self.obtener_posicion("Posición inicial para eliminar: ")
                self.queue.deleteMultipleByPosition(n, pos)
            
            elif opcion == "8":
                # Eliminar por valor
                if not self.queue.isEmpty():
                    print("Valor a eliminar:")
                    tipo = self.obtener_tipo_dato()
                    if tipo == "order":
                        order_id = int(input("ID de la orden a eliminar: "))
                        self.queue.deleteByValue(Order(order_id, ""))
                    else:
                        valor = input("Valor a eliminar: ")
                        self.queue.deleteByValue(valor)
                else:
                    print("La cola está vacía")
            
            elif opcion == "9":
                # Insertar después de un valor
                if not self.queue.isEmpty():
                    print("Valor de referencia:")
                    tipo = self.obtener_tipo_dato()
                    if tipo == "order":
                        target_id = int(input("ID de la orden de referencia: "))
                        target = Order(target_id, "")
                        print("Nuevo valor:")
                        new_id = int(input("ID de la nueva orden: "))
                        new_desc = input("Descripción: ")
                        self.queue.insertAfterValue(target, Order(new_id, new_desc))
                    else:
                        target = input("Valor de referencia: ")
                        new_valor = input("Nuevo valor a insertar: ")
                        self.queue.insertAfterValue(target, new_valor)
                else:
                    print("La cola está vacía")
            
            elif opcion == "10":
                # Ver frente de la cola
                frente = self.queue.front()
                if frente:
                    print(f"Frente de la cola: {frente}")
                else:
                    print("La cola está vacía")
            
            elif opcion == "11":
                # Mostrar toda la cola
                self.queue.printInfo()
            
            elif opcion == "12":
                # Tamaño de la cola
                print(f"Tamaño de la cola: {self.queue.size()}")
            
            elif opcion == "13":
                # Vaciar toda la cola
                confirm = input("¿Está seguro de vaciar toda la cola? (s/n): ")
                if confirm.lower() == 's':
                    while not self.queue.isEmpty():
                        self.queue.dequeue()
                    print("Cola vaciada completamente")
            
            elif opcion == "14":
                # Ejecutar pruebas predefinidas
                print("\n--- Ejecutando pruebas predefinidas ---")
                TestQueue.main_static(self.queue)
            
            elif opcion == "0":
                confirm = input("¿Está seguro que desea salir? (s/n): ")
                if confirm.lower() == 's':
                    print("¡Hasta luego!")
                    self.ejecutando = False
            
            else:
                print("Opción no válida. Intente nuevamente.")
            
            if self.ejecutando and opcion != "0":
                input("\nPresione Enter para continuar...")


class TestQueue:
    """Clase para probar la implementación de Queue con inserciones y eliminaciones."""
    
    @staticmethod
    def main():
        print("=== Test de Queue con operaciones avanzadas ===\n")
        
        # Crear cola
        queue = Queue()
        TestQueue.main_static(queue)
    
    @staticmethod
    def main_static(queue):
        """Versión estática para usar desde el menú."""
        
        # 1. Pruebas básicas
        print("--- 1. Pruebas básicas ---")
        print("Cola recién creada:")
        queue.printInfo()
        
        # 2. Insertar elementos
        print("\n--- 2. Insertando elementos (enqueue) ---")
        queue.enqueue(Order(101, "Cliente A"))
        queue.enqueue(Order(102, "Cliente B"))
        queue.enqueue(Order(103, "Cliente C"))
        queue.printInfo()
        
        # 3. Insertar en posiciones específicas
        print("\n--- 3. Insertando en posiciones específicas ---")
        queue.insertAtPosition(1, Order(104, "Cliente D (insertado en pos 1)"))
        queue.insertAtPosition(0, Order(105, "Cliente E (insertado al frente)"))
        queue.insertAtPosition(queue.size(), Order(106, "Cliente F (insertado al final)"))
        queue.printInfo()
        
        # 4. Insertar después de un valor
        print("\n--- 4. Insertando después de un valor específico ---")
        target = Order(101, "Cliente A")
        queue.insertAfterValue(target, Order(107, "Cliente G (después de 101)"))
        queue.printInfo()
        
        # 5. Eliminar por posición
        print("\n--- 5. Eliminando por posición ---")
        queue.deleteAtPosition(2)  # Eliminar posición 2
        queue.deleteAtPosition(0)  # Eliminar frente
        queue.deleteAtPosition(queue.size() - 1)  # Eliminar último
        queue.printInfo()
        
        # 6. Eliminar por valor
        print("\n--- 6. Eliminando por valor ---")
        queue.deleteByValue(Order(104, "Cliente D (insertado en pos 1)"))
        queue.deleteByValue(Order(999, "No existe"))  # Intento de eliminar no existente
        queue.printInfo()
        
        # 7. Prueba de operaciones básicas
        print("\n--- 7. Probando operaciones básicas ---")
        print(f"Front: {queue.front()}")
        print(f"Size: {queue.size()}")
        print(f"isEmpty: {queue.isEmpty()}")
        
        # 8. Vaciar cola completamente
        print("\n--- 8. Vaciando cola completamente ---")
        while not queue.isEmpty():
            queue.dequeue()
        queue.printInfo()
        
        # 9. Prueba de errores
        print("\n--- 9. Prueba de manejo de errores ---")
        queue.deleteAtPosition(0)  # Intentar eliminar de cola vacía
        queue.insertAtPosition(5, Order(999, "Error"))  # Posición inválida


if __name__ == "__main__":
    # Preguntar al usuario cómo desea ejecutar
    print("¿Cómo desea ejecutar el programa?")
    print("1. Modo interactivo (menú)")
    print("2. Pruebas automáticas")
    opcion = input("Seleccione una opción (1 o 2): ")
    
    if opcion == "1":
        menu = MenuQueue()
        menu.ejecutar()
    else:
        TestQueue.main()