import sys
import time
import numpy as np

sys.setrecursionlimit(5000) 

def multiplicacion_tradicional(matriz_a, matriz_b):
    """
    Calcula la multiplicación de matrices usando el método O(n^3).
    """
    dimension = matriz_a.shape[0]
    
    # Inicializar la matriz de resultado con ceros
    matriz_resultado = np.zeros((dimension, dimension), dtype=int)
    
    # Iterar sobre filas
    for fila in range(dimension):
        # Iterar sobre columnas
        for columna in range(dimension):
            suma_parcial = 0
            for indice_interno in range(dimension):
                suma_parcial += matriz_a[fila, indice_interno] * matriz_b[indice_interno, columna]
            matriz_resultado[fila, columna] = suma_parcial
    return matriz_resultado

def multiplicacion_dr1(matriz_a, matriz_b):
    """
    Multiplicación recursiva basada en la Propiedad 1 (8 multiplicaciones).
    """
    dimension = matriz_a.shape[0]
    
    # Caso base de la recursión (matriz 1x1)
    if dimension == 1:
        return matriz_a * matriz_b

    # Dividir la matriz en 4 sub-problemas
    punto_medio = dimension // 2
    
    # Generar submatrices de A
    submatriz_a11 = matriz_a[:punto_medio, :punto_medio]
    submatriz_a12 = matriz_a[:punto_medio, punto_medio:]
    submatriz_a21 = matriz_a[punto_medio:, :punto_medio]
    submatriz_a22 = matriz_a[punto_medio:, punto_medio:]
    
    # Generar submatrices de B
    submatriz_b11 = matriz_b[:punto_medio, :punto_medio]
    submatriz_b12 = matriz_b[:punto_medio, punto_medio:]
    submatriz_b21 = matriz_b[punto_medio:, :punto_medio]
    submatriz_b22 = matriz_b[punto_medio:, punto_medio:]
    
    # Calcular submatrices C con 8 llamadas recursivas
    submatriz_c11 = multiplicacion_dr1(submatriz_a11, submatriz_b11) + multiplicacion_dr1(submatriz_a12, submatriz_b21)
    submatriz_c12 = multiplicacion_dr1(submatriz_a11, submatriz_b12) + multiplicacion_dr1(submatriz_a12, submatriz_b22)
    submatriz_c21 = multiplicacion_dr1(submatriz_a21, submatriz_b11) + multiplicacion_dr1(submatriz_a22, submatriz_b21)
    submatriz_c22 = multiplicacion_dr1(submatriz_a21, submatriz_b12) + multiplicacion_dr1(submatriz_a22, submatriz_b22)
    
    # Combinar resultados en una sola matriz
    fila_superior = np.hstack((submatriz_c11, submatriz_c12))
    fila_inferior = np.hstack((submatriz_c21, submatriz_c22))
    matriz_resultado = np.vstack((fila_superior, fila_inferior))
    
    return matriz_resultado

def multiplicacion_dr2_strassen(matriz_a, matriz_b):
    """
    Multiplicación recursiva basada en la Propiedad 2 (Strassen, 7 multiplicaciones)
    """
    dimension = matriz_a.shape[0]
    
    # Caso base
    if dimension == 1:
        return matriz_a * matriz_b

    punto_medio = dimension // 2
    
    # 1. Definir submatrices
    a11 = matriz_a[:punto_medio, :punto_medio]
    a12 = matriz_a[:punto_medio, punto_medio:]
    a21 = matriz_a[punto_medio:, :punto_medio]
    a22 = matriz_a[punto_medio:, punto_medio:]
    
    b11 = matriz_b[:punto_medio, :punto_medio]
    b12 = matriz_b[:punto_medio, punto_medio:]
    b21 = matriz_b[punto_medio:, :punto_medio]
    b22 = matriz_b[punto_medio:, punto_medio:]
    
    # Calcular los 7 productos de Strassen
    
    p1 = multiplicacion_dr2_strassen(a11 + a22, b11 + b22)
    
    p2 = multiplicacion_dr2_strassen(a11, b12 - b22)
    
    p3 = multiplicacion_dr2_strassen(a21 + a22, b11)
    
    p4 = multiplicacion_dr2_strassen(a22, b21 - b11)
    
    p5 = multiplicacion_dr2_strassen(a11 + a12, b22)
    
    p6 = multiplicacion_dr2_strassen(a21 - a11, b11 + b12)
    
    p7 = multiplicacion_dr2_strassen(a12 - a22, b21 + b22)
    
    # Calcular las submatrices del resultado 
    
    submatriz_c11 = p1 + p4 - p5 + p7
    
    submatriz_c12 = p2 + p5
    
    submatriz_c21 = p3 + p4

    submatriz_c22 = p1 + p2 - p3 + p6
    
    # Combinar
    fila_superior = np.hstack((submatriz_c11, submatriz_c12))
    fila_inferior = np.hstack((submatriz_c21, submatriz_c22))
    matriz_resultado = np.vstack((fila_superior, fila_inferior))
    
    return matriz_resultado

# --- Pruebas ---

# Lista de tamaños n a probar
lista_tamanos = [64, 128, 256, 512, 1024, 2048, 4096]

# Imprimir tabla
print("--- Iniciando Experimentos ---")
print("Tiempos de ejecución en segundos.\n")
print(f"{'n':<8} | {'Tradicional':<15} | {'DR1':<15} | {'DR2':<15}")
print("-" * 59)

# Guardar los resultados
tiempos_ejecucion = {
    "Tradicional": [],
    "DR1": [],
    "DR2": []
}

# Límite de tiempo en segundos
TIEMPO_MAXIMO_SEGUNDOS = 7200 
omitir_tradicional = False
omitir_dr1 = False
omitir_dr2 = False

for tamano in lista_tamanos:
    print(f"{tamano:<8} | ", end="", flush=True)
    
    # Generar nuevas matrices aleatorias para cada n
    try:
        
        matriz_a_exp = np.random.randint(10, size=(tamano, tamano))
        matriz_b_exp = np.random.randint(10, size=(tamano, tamano))
    except MemoryError:
        print(f"Error de memoria al crear matrices de {tamano}x{tamano}. Deteniendo.")
        break
        
    # Prueba Algoritmo Tradicional
    tiempo_alg_tradicional = -1
    if not omitir_tradicional:
        try:
            tiempo_inicio = time.perf_counter()
            multiplicacion_tradicional(matriz_a_exp, matriz_b_exp)
            tiempo_fin = time.perf_counter()
            tiempo_alg_tradicional = tiempo_fin - tiempo_inicio
            print(f"{tiempo_alg_tradicional:<15.6f} | ", end="", flush=True)
            if tiempo_alg_tradicional > TIEMPO_MAXIMO_SEGUNDOS:
                print("\n(Tradicional superó el límite de tiempo, omitiendo pruebas mayores)")
                omitir_tradicional = True
        except Exception as e:
            print(f"{'Error':<15} | ", end="", flush=True)
            print(e)
            omitir_tradicional = True
    else:
        print(f"{'Omitido':<15} | ", end="", flush=True)
        
    tiempos_ejecucion["Tradicional"].append(tiempo_alg_tradicional)

    # Prueba algoritmo DR1
    tiempo_alg_dr1 = -1
    if not omitir_dr1:
        try:
            tiempo_inicio = time.perf_counter()
            multiplicacion_dr1(matriz_a_exp, matriz_b_exp)
            tiempo_fin = time.perf_counter()
            tiempo_alg_dr1 = tiempo_fin - tiempo_inicio
            print(f"{tiempo_alg_dr1:<15.6f} | ", end="", flush=True)
            if tiempo_alg_dr1 > TIEMPO_MAXIMO_SEGUNDOS:
                print("\n(DR1 superó el límite de tiempo, omitiendo pruebas mayores)")
                omitir_dr1 = True
        except Exception as e:
            print(f"{'Error':<15} | ", end="", flush=True)
            print(e)
            omitir_dr1 = True
    else:
        print(f"{'Omitido':<15} | ", end="", flush=True)
        
    tiempos_ejecucion["DR1"].append(tiempo_alg_dr1)

    # Prueba algoritmo DR2 
    tiempo_alg_dr2 = -1
    if not omitir_dr2:
        try:
            tiempo_inicio = time.perf_counter()
            multiplicacion_dr2_strassen(matriz_a_exp, matriz_b_exp)
            tiempo_fin = time.perf_counter()
            tiempo_alg_dr2 = tiempo_fin - tiempo_inicio
            print(f"{tiempo_alg_dr2:<15.6f}", flush=True) # print final de la línea
            if tiempo_alg_dr2 > TIEMPO_MAXIMO_SEGUNDOS:
                print("\n(DR2 superó el límite de tiempo, omitiendo pruebas mayores)")
                omitir_dr2 = True
        except Exception as e:
            print(f"{'Error':<15}", flush=True)
            print(e)
            omitir_dr2 = True
    else:
        print(f"{'Omitido':<15}", flush=True)
        
    tiempos_ejecucion["DR2"].append(tiempo_alg_dr2)

print("-" * 59)
print("--- Experimentos Finalizados ---")

print("\nResultados para copiar en el documento:")
print("\nN\tTradicional\tDR1\tDR2")
for indice, tamano in enumerate(lista_tamanos):
    texto_trad = f"{tiempos_ejecucion['Tradicional'][indice]:.6f}" if tiempos_ejecucion['Tradicional'][indice] != -1 else "Error/Omitido"
    texto_dr1 = f"{tiempos_ejecucion['DR1'][indice]:.6f}" if tiempos_ejecucion['DR1'][indice] != -1 else "Error/Omitido"
    texto_dr2 = f"{tiempos_ejecucion['DR2'][indice]:.6f}" if tiempos_ejecucion['DR2'][indice] != -1 else "Error/Omitido"
    
    
    if texto_trad == "Error/Omitido" and texto_dr1 == "Error/Omitido" and texto_dr2 == "Error/Omitido":
        print(f"{tamano}\tError de memoria.")
        break
    
    print(f"{tamano}\t{texto_trad}\t{texto_dr1}\t{texto_dr2}")