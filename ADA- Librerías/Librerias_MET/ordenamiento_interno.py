"""
Librería de Métodos de Ordenamiento Internos
Implementa: Burbuja, Inserción, Selección, Shellsort, Quicksort, Heapsort, Radixsort
"""

class OrdenamientoInterno:
    """Clase que contiene los métodos de ordenamiento interno"""
    
    @staticmethod
    def burbuja(arr, paso_callback=None):
        """
        Método de Burbuja (Bubble Sort)
        Complejidad: O(n²)
        """
        n = len(arr)
        pasos = []
        arr_temp = arr.copy()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr_temp[j] > arr_temp[j + 1]:
                    arr_temp[j], arr_temp[j + 1] = arr_temp[j + 1], arr_temp[j]
                    paso = arr_temp.copy()
                    pasos.append(paso)
                    if paso_callback:
                        paso_callback(paso)
        
        return pasos, arr_temp
    
    @staticmethod
    def insercion(arr, paso_callback=None):
        """
        Método de Inserción (Insertion Sort)
        Complejidad: O(n²)
        """
        n = len(arr)
        pasos = []
        arr_temp = arr.copy()
        
        for i in range(1, n):
            key = arr_temp[i]
            j = i - 1
            while j >= 0 and arr_temp[j] > key:
                arr_temp[j + 1] = arr_temp[j]
                j -= 1
                paso = arr_temp.copy()
                pasos.append(paso)
                if paso_callback:
                    paso_callback(paso)
            arr_temp[j + 1] = key
            paso = arr_temp.copy()
            pasos.append(paso)
            if paso_callback:
                paso_callback(paso)
        
        return pasos, arr_temp
    
    @staticmethod
    def seleccion(arr, paso_callback=None):
        """
        Método de Selección (Selection Sort)
        Complejidad: O(n²)
        """
        n = len(arr)
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr_temp[j] < arr_temp[min_idx]:
                    min_idx = j
                paso = arr_temp.copy()
                pasos.append(paso)
                if paso_callback:
                    paso_callback(paso)
            
            if min_idx != i:
                arr_temp[i], arr_temp[min_idx] = arr_temp[min_idx], arr_temp[i]
                paso = arr_temp.copy()
                pasos.append(paso)
                if paso_callback:
                    paso_callback(paso)
        
        return pasos, arr_temp
    
    @staticmethod
    def shellsort(arr, paso_callback=None):
        """
        Método Shellsort
        Complejidad: O(n log n) en promedio
        """
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
        n = len(arr_temp)
        gap = n // 2
        
        while gap > 0:
            for i in range(gap, n):
                temp = arr_temp[i]
                j = i
                while j >= gap and arr_temp[j - gap] > temp:
                    arr_temp[j] = arr_temp[j - gap]
                    j -= gap
                arr_temp[j] = temp
                paso = arr_temp.copy()
                pasos.append(paso)
                if paso_callback:
                    paso_callback(paso)
            gap //= 2
        
        return pasos, arr_temp
    
    @staticmethod
    def quicksort(arr, paso_callback=None):
        """
        Método Quicksort
        Complejidad: O(n log n) en promedio
        """
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
        def _quicksort(arr, low, high):
            if low < high:
                pi = _partition(arr, low, high)
                _quicksort(arr, low, pi - 1)
                _quicksort(arr, pi + 1, high)
        
        def _partition(arr, low, high):
            pivote = arr[high]
            i = low - 1
            
            for j in range(low, high):
                if arr[j] <= pivote:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    paso = arr.copy()
                    pasos.append(paso)
                    if paso_callback:
                        paso_callback(paso)
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            paso = arr.copy()
            pasos.append(paso)
            if paso_callback:
                paso_callback(paso)
            
            return i + 1
        
        _quicksort(arr_temp, 0, len(arr_temp) - 1)
        return pasos, arr_temp
    
    @staticmethod
    def heapsort(arr, paso_callback=None):
        """
        Método Heapsort
        Complejidad: O(n log n)
        """
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
        def heapify(arr, n, i):
            mayor = i
            izq = 2 * i + 1
            der = 2 * i + 2
            
            if izq < n and arr[izq] > arr[mayor]:
                mayor = izq
            if der < n and arr[der] > arr[mayor]:
                mayor = der
            
            if mayor != i:
                arr[i], arr[mayor] = arr[mayor], arr[i]
                paso = arr.copy()
                pasos.append(paso)
                if paso_callback:
                    paso_callback(paso)
                heapify(arr, n, mayor)
        
        n = len(arr_temp)
        
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr_temp, n, i)
        
        for i in range(n - 1, 0, -1):
            arr_temp[0], arr_temp[i] = arr_temp[i], arr_temp[0]
            paso = arr_temp.copy()
            pasos.append(paso)
            if paso_callback:
                paso_callback(paso)
            heapify(arr_temp, i, 0)
        
        return pasos, arr_temp
    
    @staticmethod
    def radixsort(arr, paso_callback=None):
        """
        Método Radixsort
        Complejidad: O(n * k) donde k es el número de dígitos
        """
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
        if not arr_temp:
            return pasos, arr_temp
        
        def counting_sort(arr, exp):
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            
            for i in range(n):
                idx = (arr[i] // exp) % 10
                count[idx] += 1
            
            for i in range(1, 10):
                count[i] += count[i - 1]
            
            for i in range(n - 1, -1, -1):
                idx = (arr[i] // exp) % 10
                output[count[idx] - 1] = arr[i]
                count[idx] -= 1
            
            for i in range(n):
                arr[i] = output[i]
            
            paso = arr.copy()
            pasos.append(paso)
            if paso_callback:
                paso_callback(paso)
        
        max_val = max(arr_temp)
        exp = 1
        
        while max_val // exp > 0:
            counting_sort(arr_temp, exp)
            exp *= 10
        
        return pasos, arr_temp