from .fuzzificacion import membresia_triangular

# Primero, definimos cómo son las "etiquetas" de salida (Muy Corto, Corto, etc.)
# Usamos la función del triángulo que ya teníamos para dibujar sus formas.
SALIDA_MEMBRESIA = {
    # Cada duración tiene su propia función lambda que llama a membresia_triangular
    # con los puntos específicos que definen su forma (triángulo o rampa) en el rango de 0 a 60 minutos.
    "Muy Corto": lambda x: membresia_triangular(
        x, 0, 8, 23
    ),  # Triángulo entre 0 y 23, pico en 8
    "Corto": lambda x: membresia_triangular(
        x, 8, 23, 38
    ),  # Triángulo entre 8 y 38, pico en 23
    "Medio": lambda x: membresia_triangular(
        x, 23, 38, 53
    ),  # Triángulo entre 23 y 53, pico en 38
    "Largo": lambda x: membresia_triangular(
        x, 38, 53, 60
    ),  # Triángulo entre 38 y 60, pico en 53
    "Muy Largo": lambda x: membresia_triangular(
        x, 53, 60, 60
    ),  # Rampa hacia arriba desde 53 hasta 60
}


def defuzzify_centroide(activacion_salidas):
    numerador = 0.0
    denominador = 0.0

    paso = 0.5

    for x in range(int(60 / paso) + 1):
        tiempo = x * paso

        grado_agregado = 0.0
        for termino, fuerza in activacion_salidas.items():
            membresia_cortada = min(fuerza, SALIDA_MEMBRESIA[termino](tiempo))

            grado_agregado = max(grado_agregado, membresia_cortada)

        numerador += tiempo * grado_agregado
        denominador += grado_agregado

    if denominador == 0:
        return 0.0

    return numerador / denominador


def defuzzify_centroide(activacion_salidas):
    """
    Toma las "fuerzas" de cada posible duración (el resultado del motor_de_inferencia)
    y las combina para calcular UN SOLO número final: el tiempo de lavado exacto.
    Usa el método del centroide (como encontrar el punto de equilibrio).
    """
    numerador = 0.0  # Parte de arriba de la fórmula del centroide
    denominador = 0.0  # Parte de abajo de la fórmula

    paso = 0.5  # Qué tan pequeños son los "saltitos" que damos al revisar el tiempo (0 a 60 min)

    # Revisamos cada posible valor de tiempo, desde 0 hasta 60, en saltitos de 'paso'
    for x in range(int(60 / paso) + 1):
        tiempo = (
            x * paso
        )  # El valor de tiempo actual que estamos revisando (ej. 0, 0.5, 1, 1.5 ... 60)

        # Calculamos la "altura combinada" de todas las formas de salida en este 'tiempo'
        grado_agregado = 0.0
        # Recorremos cada duración ("Muy Corto", "Corto", etc.) y su "fuerza" calculada antes
        for termino, fuerza in activacion_salidas.items():
            # 1. "Cortamos" la forma de la duración (ej. el triángulo de "Medio")
            #    a la altura máxima que nos dio la "fuerza" de esa regla.
            #    Usamos la función lambda que guardamos en SALIDA_MEMBRESIA.
            membresia_cortada = min(fuerza, SALIDA_MEMBRESIA[termino](tiempo))

            # 2. Combinamos las alturas cortadas. Si varias formas se solapan en este 'tiempo',
            #    nos quedamos con la más alta. Esto crea la forma final "agregada".
            grado_agregado = max(grado_agregado, membresia_cortada)

        # Acumulamos para la fórmula del centroide:
        # Sumamos (tiempo * altura_combinada)
        numerador += tiempo * grado_agregado
        # Sumamos (altura_combinada)
        denominador += grado_agregado

    # Si el denominador es 0 (ninguna regla se activó), devolvemos 0 para evitar errores.
    if denominador == 0:
        return 0.0

    # La fórmula final: divide la suma ponderada entre la suma de alturas.
    # Esto nos da el "centro de gravedad" de la forma combinada, que es nuestro tiempo final.
    return numerador / denominador
