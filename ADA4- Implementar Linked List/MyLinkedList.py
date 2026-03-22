"""
MyLinkedList 
"""

class Node:
    """Clase que representa un nodo de la lista enlazada"""
    def __init__(self, data):
        self.data = data    # Valor del nodo
        self.next = None    # Apuntador al siguiente nodo


class MyLinkedList:
    """Implementación de una lista enlazada simple"""
    
    def __init__(self):
        """Inicializa una lista vacía"""
        self.head = None    # Primer nodo de la lista
        self.size = 0       # Tamaño de la lista
    
    def append(self, data):
        """Agrega un elemento al final de la lista"""
        new_node = Node(data)
        
        if self.head is None:
            # Si la lista está vacía, el nuevo nodo es la cabeza
            self.head = new_node
        else:
            # Recorre hasta el último nodo
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, data):
        """Agrega un elemento al inicio de la lista"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert(self, index, data):
        """Inserta un elemento en una posición específica"""
        if index < 0 or index > self.size:
            raise IndexError("Índice fuera de rango")
        
        if index == 0:
            self.prepend(data)
            return
        
        if index == self.size:
            self.append(data)
            return
        
        new_node = Node(data)
        current = self.head
        # Llega al nodo anterior a la posición deseada
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def remove(self, data):
        """Elimina la primera ocurrencia del elemento especificado"""
        if self.head is None:
            return False
        
        # Si el elemento a eliminar está en la cabeza
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        
        # Busca el elemento en el resto de la lista
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def remove_at(self, index):
        """Elimina el elemento en la posición especificada"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        
        if index == 0:
            self.head = self.head.next
            self.size -= 1
            return
        
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        current.next = current.next.next
        self.size -= 1
    
    def get(self, index):
        """Obtiene el elemento en la posición especificada"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        
        current = self.head
        for _ in range(index):
            current = current.next
        
        return current.data
    
    def index_of(self, data):
        """Retorna el índice de la primera ocurrencia del elemento"""
        current = self.head
        idx = 0
        while current:
            if current.data == data:
                return idx
            current = current.next
            idx += 1
        return -1
    
    def contains(self, data):
        """Verifica si un elemento existe en la lista"""
        return self.index_of(data) != -1
    
    def is_empty(self):
        """Retorna True si la lista está vacía"""
        return self.size == 0
    
    def get_size(self):
        """Retorna el tamaño de la lista"""
        return self.size
    
    def clear(self):
        """Elimina todos los elementos de la lista"""
        self.head = None
        self.size = 0
    
    def __str__(self):
        """Representación en string de la lista"""
        if self.is_empty():
            return "[]"
        
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        
        return "[" + " -> ".join(elements) + "]"
    
    def __len__(self):
        """Permite usar len(lista)"""
        return self.size
    
    def __iter__(self):
        """Permite iterar sobre la lista"""
        current = self.head
        while current:
            yield current.data
            current = current.next


# ----- Código de prueba de funcionamiento -----
if __name__ == "__main__":
    print("=== PRUEBAS DE MyLinkedList ===\n")
    
    # Creacion de una nueva lista
    mi_lista = MyLinkedList()
    
    # Prueba de append
    print("1. Agregando elementos con append:")
    mi_lista.append(10)
    mi_lista.append(20)
    mi_lista.append(30)
    print(f"   Lista: {mi_lista}")
    print(f"   Tamaño: {len(mi_lista)}\n")
    
    # Prueba de prepend
    print("2. Agregando al inicio con prepend:")
    mi_lista.prepend(5)
    print(f"   Lista: {mi_lista}")
    print(f"   Tamaño: {len(mi_lista)}\n")
    
    # Prueba de insert
    print("3. Insertando en posición específica:")
    mi_lista.insert(2, 15)
    print(f"   Insertar 15 en índice 2: {mi_lista}")
    mi_lista.insert(0, 1)
    print(f"   Insertar 1 en índice 0: {mi_lista}")
    mi_lista.insert(6, 35)
    print(f"   Insertar 35 al final: {mi_lista}\n")
    
    # Prueba de get
    print("4. Obtener elementos por índice:")
    print(f"   Elemento en índice 0: {mi_lista.get(0)}")
    print(f"   Elemento en índice 3: {mi_lista.get(3)}")
    print(f"   Elemento en índice 5: {mi_lista.get(5)}\n")
    
    # Prueba de index_of y contains
    print("5. Búsqueda de elementos:")
    print(f"   ¿Contiene 15? {mi_lista.contains(15)}")
    print(f"   Índice de 15: {mi_lista.index_of(15)}")
    print(f"   ¿Contiene 100? {mi_lista.contains(100)}")
    print(f"   Índice de 100: {mi_lista.index_of(100)}\n")
    
    # Prueba de remove
    print("6. Eliminar elementos por valor:")
    mi_lista.remove(15)
    print(f"   Eliminar 15: {mi_lista}")
    mi_lista.remove(1)
    print(f"   Eliminar 1: {mi_lista}")
    resultado = mi_lista.remove(100)
    print(f"   Intentar eliminar 100: {'Eliminado' if resultado else 'No encontrado'}\n")
    
    # Prueba de remove_at
    print("7. Eliminar elementos por índice:")
    mi_lista.remove_at(0)
    print(f"   Eliminar índice 0: {mi_lista}")
    mi_lista.remove_at(2)
    print(f"   Eliminar índice 2: {mi_lista}\n")
    
    # Prueba de iteración
    print("8. Iterar sobre la lista:")
    for i, elemento in enumerate(mi_lista):
        print(f"   Elemento {i}: {elemento}")
    print()
    
    # Prueba de clear e is_empty
    print("9. Vaciar la lista:")
    print(f"   ¿Está vacía? {mi_lista.is_empty()}")
    mi_lista.clear()
    print(f"   Después de clear, ¿está vacía? {mi_lista.is_empty()}")
    print(f"   Lista vacía: {mi_lista}")