
try:
    from motor_difuso.fuzzificacion import (
        fuzzify_grado_suciedad,
        fuzzify_tipo_suciedad,
        fuzzify_cantidad_ropa
    )
    from motor_difuso.inferencia import motor_de_inferencia
    from motor_difuso.defuzzificacion import defuzzify_centroide
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de que todos los archivos (fuzzificacion.py, inferencia.py, defuzzificacion.py) existen en 'motor_difuso'.")
    exit()

print("¡Importación exitosa de todos los módulos! ")

# --- CASO DE PRUEBA 1: (50, 50, 50) ---
# Este es el caso de prueba del artículo.
val_tipo = 50
val_grado = 50
val_cantidad = 50

print(f"\n--- Probando el sistema completo con el caso ({val_tipo}, {val_grado}, {val_cantidad}) ---")

# --- PASO 1: FUZZIFICACIÓN ---
fuzz_tipo = fuzzify_tipo_suciedad(val_tipo)
fuzz_grado = fuzzify_grado_suciedad(val_grado)
fuzz_cantidad = fuzzify_cantidad_ropa(val_cantidad)

valores_fuzzificados = {'tipo': fuzz_tipo, 'grado': fuzz_grado, 'cantidad': fuzz_cantidad}
print(f"1. Resultado Fuzzificación (parcial):")
print(f"   Tipo(50) -> {fuzz_tipo['Media']}")
print(f"   Grado(50) -> {fuzz_grado['Media']}")
print(f"   Cantidad(50) -> {fuzz_cantidad['Media']}")

# --- PASO 2: INFERENCIA ---
activacion_salidas = motor_de_inferencia(valores_fuzzificados)
print(f"\n2. Resultado Inferencia:")
print(f"   {activacion_salidas}")

# --- PASO 3: DEFUZZIFICACIÓN ---
tiempo_final = defuzzify_centroide(activacion_salidas)
print(f"\n3. Resultado Defuzzificación:")
print(f"   ¡Tiempo de lavado final: {tiempo_final:.2f} minutos!")
print("-" * 40)