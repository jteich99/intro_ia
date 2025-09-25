# notas de ejercicio de N reinas - intro ia
**estado**: lista donde cada posición es una columna y el valor es la fila en la que está la reina que se encuentra en columna
**vecino**: mover la reina de una columna de fila -> modificar un valor en la lista de ubicaciones de reinas
- se tienen 56 vecinos para cada estado
**costo**: cantidad de pares de reinas que se atacan entre sí (que comparten fila, columna o diagonal)
- columna no pueden compartir por como armamos el ejercicio