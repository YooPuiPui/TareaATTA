# Tarea 1 - Multiplicación de Matrices (Análisis de Algoritmos)

Este script implementa y compara el rendimiento de tres algoritmos para la multiplicación de matrices cuadradas.

Los algoritmos implementados son:
1.  **Algoritmo Tradicional** (Iterativo, $O(n^3)$)
2.  [cite_start]**Algoritmo DR1** (Recursivo, 8 multiplicaciones)
3.  [cite_start]**Algoritmo DR2** (Recursivo de Strassen, 7 multiplicaciones)

## Requisitos

Para ejecutar este programa, necesitarás:
* Python (versión 3.6 o superior)
* La biblioteca NumPy

## Instalación

1.  **Python:** Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/).
2.  **NumPy:** Una vez instalado Python, abre una terminal o símbolo del sistema y ejecuta el siguiente comando para instalar NumPy:
    ```bash
    pip install numpy o python -m pip install numpy
    ```

## Ejecución

1.  Guarda el código principal en un archivo llamado `matrices.py` (o el nombre que prefieras).
2.  Abre una terminal y navega hasta la carpeta donde guardaste el archivo.
3.  Ejecuta el script con el siguiente comando:

    ```bash
    python matrices.py
    ```

### ⚠️ Advertencia de Tiempo

El script comenzará a tomar los tiempos para todos los tamaños de matrices, desde $n=64$ hasta $n=4096$.

**La ejecución será muy larga**, especialmente para $n=1024$ y superiores. [cite_start]Es normal que el programa tarde varios minutos o incluso horas en completarse, tal como se advierte en el enunciado de la tarea [cite: 34-35]. Los resultados se irán imprimiendo en la terminal fila por fila a medida que se completen.