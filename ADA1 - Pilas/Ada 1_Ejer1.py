def evaluar(expresion):
    """Evalúa automáticamente expresiones prefijas o posfijas"""
    tokens = expresion.split()
    pila = []
    operadores = {'+', '-', '*', '/', '^'}
    
    def es_operador(t): return t in operadores
    
    notacion = ""
    
    if es_operador(tokens[0]):  
        notacion = "prefija"
        for token in reversed(tokens):
            if es_operador(token):
                a, b = pila.pop(), pila.pop()
                if token == '+': pila.append(a + b)
                elif token == '-': pila.append(a - b)
                elif token == '*': pila.append(a * b)
                elif token == '/': pila.append(a / b)
                elif token == '^': pila.append(a ** b)
            else:
                pila.append(float(token))
    else:  
        notacion = "posfija"
        for token in tokens:
            if es_operador(token):
                b, a = pila.pop(), pila.pop()
                if token == '+': pila.append(a + b)
                elif token == '-': pila.append(a - b)
                elif token == '*': pila.append(a * b)
                elif token == '/': pila.append(a / b)
                elif token == '^': pila.append(a ** b)
            else:
                pila.append(float(token))
    
    return pila[0], notacion

while True:
    print (" ")
    print ("Ingresa los valores y los signos entre espacios")
    expr = input("\nExpresión ('salir' para terminar): ")
    if expr.lower() == 'salir':
        break
    try:
        resultado, tipo = evaluar(expr)
        print(f"Notación: {tipo} | Resultado: {resultado}")
    except:
        print("Error: Expresión inválida")