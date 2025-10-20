import math

# --- Función de Membresía (Dependencia) ---
def membresia_triangular(x, a, b, c):
    """Calcula la membresía para una función triangular [a, b, c]."""
    
    # Caso 1: Pico es el punto inicial (rampa de bajada, como "Poca")
    if a == b:
        if x <= a: return 1.0
        if x >= c: return 0.0
        return (c - x) / (c - a) if (c - a) != 0 else 0.0
        
    # Caso 2: Pico es el punto final (rampa de subida, como "Mucha" o "Muy Largo")
    if b == c:
        if x >= c: return 1.0
        if x <= a: return 0.0
        return (x - a) / (c - a) if (c - a) != 0 else 0.0
        
    # Caso 3: Triángulo normal (como "Media")
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a) if (b - a) != 0 else 0.0
    if b < x < c:
        return (c - x) / (c - b) if (c - b) != 0 else 0.0
    
    return 0.0 

# --- Definición de la Salida (Dependencia) ---
SALIDA_MEMBRESIA = {
    'Muy Corto': lambda x: membresia_triangular(x, 0, 8, 23),
    'Corto':     lambda x: membresia_triangular(x, 8, 23, 38),
    'Medio':     lambda x: membresia_triangular(x, 23, 38, 53),
    'Largo':     lambda x: membresia_triangular(x, 38, 53, 60),
    'Muy Largo': lambda x: membresia_triangular(x, 53, 60, 60)
}

# --- Función a Probar ---
def defuzzify_centroide(activacion_salidas):
    """Calcula el valor crisp de salida usando el método del centroide."""
    numerador = 0.0
    denominador = 0.0
    
    paso = 0.5 # Pequeño incremento para muestrear
    for x in range(int(60 / paso) + 1):
        tiempo = x * paso
        
        grado_agregado = 0.0
        for termino, fuerza in activacion_salidas.items():
            # "Recorta" la función de membresía a la altura de la 'fuerza'
            membresia_cortada = min(fuerza, SALIDA_MEMBRESIA[termino](tiempo))
            # La agregación es el MÁXIMO de todas las formas recortadas
            grado_agregado = max(grado_agregado, membresia_cortada)
        
        numerador += tiempo * grado_agregado
        denominador += grado_agregado
        
    if denominador == 0:
        return 0.0
        
    return numerador / denominador



# 1. Simulamos la salida del motor de inferencia
salida_simulada = {
    'Muy Corto': 0.0,
    'Corto': 0.0,
    'Medio': 0.0,
    'Largo': 0.2,      # 20% activado
    'Muy Largo': 0.5   # 50% activado
}

# 2. Llamamos a nuestra función de defuzzificación
tiempo_final = defuzzify_centroide(salida_simulada)

# 3. Imprimimos el resultado
print(f"El tiempo de lavado calculado es: {tiempo_final:.2f} minutos")