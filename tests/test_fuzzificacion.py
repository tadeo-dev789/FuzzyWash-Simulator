
try:
    from motor_difuso.fuzzificacion import (
        fuzzify_grado_suciedad,
        fuzzify_tipo_suciedad,
        fuzzify_cantidad_ropa
    )
except ImportError:
    print("Error: No se encontró la carpeta 'motor_difuso' o el archivo 'fuzzificacion.py'.")
    print("Asegúrate de que este script esté en la carpeta raíz del proyecto.")
    exit()

print("¡Importación exitosa! Comenzando pruebas...\n")

# --- PRUEBA 1: Grado de Suciedad ---
# Probamos con 75. Esperamos que esté 50% "Media" y 50% "Mucha".
test_valor_grado = 75
resultado_grado = fuzzify_grado_suciedad(test_valor_grado)
print(f"--- Probando Grado de Suciedad con valor: {test_valor_grado} ---")
print(resultado_grado)
print("-" * 40)

# --- PRUEBA 2: Tipo de Suciedad ---
# Probamos con 30. Debería estar un poco "No Grasosa" y un poco "Media".
test_valor_tipo = 30
resultado_tipo = fuzzify_tipo_suciedad(test_valor_tipo)
print(f"--- Probando Tipo de Suciedad con valor: {test_valor_tipo} ---")
print(resultado_tipo)
print("-" * 40)

# --- PRUEBA 3: Cantidad de Ropa ---
# Probamos con 50. Debería ser 100% "Media" y 0% en las otras.
test_valor_cantidad = 50
resultado_cantidad = fuzzify_cantidad_ropa(test_valor_cantidad)
print(f"--- Probando Cantidad de Ropa con valor: {test_valor_cantidad} ---")
print(resultado_cantidad)
print("-" * 40)

# --- PRUEBA 4: Caso de Prueba del Artículo ---
# Probamos con 50, 50, 50
print("--- Probando Caso del Artículo (50, 50, 50) ---")
print("Grado (50):", fuzzify_grado_suciedad(50))
print("Tipo (50):", fuzzify_tipo_suciedad(50))
print("Cantidad (50):", fuzzify_cantidad_ropa(50))
print("-" * 40)