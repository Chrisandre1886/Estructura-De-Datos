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
    
    def dequeue(self):
        """Elimina y retorna el primer elemento. Retorna None si está vacía."""
        if self.isEmpty():
            return None
        
        info = self.front_node.info
        self.front_node = self.front_node.next
        self.count -= 1
        
        # Si la cola quedó vacía, rear_node también debe ser None
        if self.isEmpty():
            self.rear_node = None
            
        return info
    
    def printInfo(self):
        """Presenta información de la cola y sus elementos."""
        print(f"Número de elementos: {self.size()}")
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


class TestQueue:
    """Clase para probar la implementación de Queue."""
    
    @staticmethod
    def main():
        print("=== Test de Queue basada en lista enlazada ===\n")
        
        queue = Queue()
        
        print("1. Cola recién creada:")
        queue.printInfo()
        print(f"isEmpty: {queue.isEmpty()}")
        print(f"front: {queue.front()}")
        print(f"dequeue: {queue.dequeue()}\n")
        
        print("2. Agregando 3 órdenes...")
        queue.enqueue(Order(101, "Cliente A"))
        queue.enqueue(Order(102, "Cliente B"))
        queue.enqueue(Order(103, "Cliente C"))
        queue.printInfo()
        print(f"size: {queue.size()}\n")
        
        print("3. Ver frente sin eliminar:")
        front_order = queue.front()
        print("front:", end=" ")
        if front_order:
            front_order.print()
        else:
            print("None")
        print(f"size después de front: {queue.size()}\n")
        
        print("4. Eliminando dos elementos:")
        removed1 = queue.dequeue()
        print("dequeue 1:", end=" ")
        if removed1:
            removed1.print()
        else:
            print("None")
            
        removed2 = queue.dequeue()
        print("dequeue 2:", end=" ")
        if removed2:
            removed2.print()
        else:
            print("None")
            
        print("\nCola después de dos dequeue:")
        queue.printInfo()
        print(f"size: {queue.size()}\n")
        
        print("5. Agregando dos órdenes más...")
        queue.enqueue(Order(104, "Cliente D"))
        queue.enqueue(Order(105, "Cliente E"))
        queue.printInfo()
        print(f"size: {queue.size()}\n")
        
        print("6. Vaciando cola completamente:")
        while not queue.isEmpty():
            removed = queue.dequeue()
            print("Eliminado:", end=" ")
            if removed:
                removed.print()
        
        print("\nCola final:")
        queue.printInfo()
        print(f"isEmpty: {queue.isEmpty()}")


if __name__ == "__main__":
    TestQueue.main()