from motor_difuso.inferencia import motor_de_inferencia

valores_fuzzificados_simulados = {
    'tipo': {
        'No Grasosa': 1.0,  # 100% No Grasosa
        'Media': 0.0,
        'Grasosa': 0.0
    },
    'grado': {
        'Poca': 0.5,       # 50% Poca
        'Media': 0.5,      # 50% Media
        'Mucha': 0.0
    },
    'cantidad': {
        'Ligera': 0.0,
        'Media': 1.0,      # 100% Media
        'Pesada': 0.0
    }
}

# 2. Llamamos al motor de inferencia con los datos simulados
print("Probando el motor de inferencia...")
resultado_inferencia = motor_de_inferencia(valores_fuzzificados_simulados)

# 3. Imprimimos el resultado
print("Resultado de la inferencia (activación de salidas):")
print(resultado_inferencia)