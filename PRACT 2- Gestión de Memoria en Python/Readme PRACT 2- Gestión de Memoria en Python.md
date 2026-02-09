Despues de ver el video que se adjunto en la tarea sobre Memoria estatica y Memoria Dinamica, al igual que analice los dos codigos que se presentaron.
Continue con la tarea que consiste en analizar los dos codigos del video (Java) y pasarlos a Python.

Codigo 1
El codigo 1 le pide al usuario 5 calificaciones mediante una ventana emergente, guarda esas calificaciones en una lista y despues imprime cada calificacion en la consola.

Cambios de Java a Python (Despues de investigar un poco):

1) JOptionPane.showInputDialog() → simpledialog.askstring() (para los cuadros de diálogo)
2) int[] calificaciones = new int[5] → calificaciones = [0] * 5 (arreglo a lista)
3) for(int i = 0; i < 5; i++) → for i in range(5): (sintaxis del bucle)
4) System.out.println() → print() (para imprimir)

Codigo 2
El codigo 2 crea una lista de frutas y agrega 4 elementos, despues elimina "Pera" y "Manzana", agrega la fruta "Sandia" y despues imprime la lista al inicio y al final.

Cambios de Java a Python (Despues de investigar un poco):

1) ArrayList<String> → lista simple [] (Python no necesita declarar tipos)
2) .add() → .append() (agregar elementos)
3) .remove(índice) → .pop(índice) (eliminar por posición)
4) System.out.println() → print() (imprimir)
