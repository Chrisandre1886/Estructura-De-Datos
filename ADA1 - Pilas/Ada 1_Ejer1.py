def evaluar(expresion):
    """Evalúa automáticamente expresiones prefijas o posfijas"""
    tokens = expresion.split()
    pila = []
    operadores = {'+', '-', '*', '/', '^'}
    
    def es_operador(t): return t in operadores
    
    # Variable para guardar la notación detectada
    notacion = ""
    
    # Detectar notación
    if es_operador(tokens[0]):  # Es prefija
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
    else:  # Es posfija
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

# Programa principal
while True:
    print ("Ingresa los valores y los signos entre espacios")
    expr = input("\nExpresión ('salir' para terminar): ")
    if expr.lower() == 'salir':
        break
    try:
        resultado, tipo = evaluar(expr)
        print(f"Notación: {tipo} | Resultado: {resultado}")
    except:
        print("Error: Expresión inválida")