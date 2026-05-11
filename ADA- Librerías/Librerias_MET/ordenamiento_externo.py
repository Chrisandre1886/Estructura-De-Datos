"""
Librería de Métodos de Ordenamiento Externos
Implementa: Intercalación, Mezcla Directa, Mezcla Equilibrada
"""

class OrdenamientoExterno:
    """Clase que contiene los métodos de ordenamiento externo"""
    
    @staticmethod
    def intercalacion(arr, paso_callback=None):
        """
        Método de Intercalación (Equivalente a Insertion Sort en memoria)
        Complejidad: O(n²)
        """
        n = len(arr)
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
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
    def mezcla_directa(arr, paso_callback=None):
        """
        Método de Mezcla Directa (Bubble Sort)
        Complejidad: O(n²)
        """
        n = len(arr)
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
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
    def mezcla_equilibrada(arr, paso_callback=None):
        """
        Método de Mezcla Equilibrada (Merge Sort)
        Complejidad: O(n log n)
        """
        pasos = []
        arr_temp = arr.copy()
        
        pasos.append(arr_temp.copy())
        if paso_callback:
            paso_callback(arr_temp.copy())
        
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def merge_sort(arr_segment):
            if len(arr_segment) <= 1:
                return arr_segment
            
            mid = len(arr_segment) // 2
            left = merge_sort(arr_segment[:mid])
            right = merge_sort(arr_segment[mid:])
            
            merged = merge(left, right)
            paso = merged.copy()
            pasos.append(paso)
            if paso_callback:
                paso_callback(paso)
            return merged
        
        resultado = merge_sort(arr_temp)
        return pasos, resultado