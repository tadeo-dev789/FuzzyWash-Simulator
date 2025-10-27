# Este archivo contiene las reglas de inferencia del proyecto.

REGLAS = [
    # Reglas para 'No Grasosa'
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Muy Corto",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Media",
        },
        "then": "Corto",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Media",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Media",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "No Grasosa",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Largo",
    },
    # Reglas para 'Media'
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Corto",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Media",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Media",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Corto",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Media",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Media",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Largo",
    },
    # Reglas para 'Grasosa'
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Corto",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Media",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Poca",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Media",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Media",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Muy Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Ligera",
        },
        "then": "Medio",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Media",
        },
        "then": "Largo",
    },
    {
        "if": {
            "Tipo de Suciedad": "Grasosa",
            "Grado de Suciedad": "Mucha",
            "Cantidad de Ropa": "Pesada",
        },
        "then": "Muy Largo",
    },
]


def motor_de_inferencia(valores_fuzzificados):
    # Inicializa un diccionario para guardar cada posible duración (salida)
    activacion_salidas = {
        "Muy Corto": 0.0,
        "Corto": 0.0,
        "Medio": 0.0,
        "Largo": 0.0,
        "Muy Largo": 0.0,
    }

    # Revisa cada regla una por una
    for regla in REGLAS:
        # Calcula qué tan bien se cumple la condición "if" de la regla
        fuerza = min(
            valores_fuzzificados["tipo"][regla["if"]["Tipo de Suciedad"]],
            valores_fuzzificados["grado"][regla["if"]["Grado de Suciedad"]],
            valores_fuzzificados["cantidad"][regla["if"]["Cantidad de Ropa"]],
        )

        # Obtiene la duración recomendada por la regla "then"
        termino_salida = regla["then"]

        # Actualiza el marcador para esa duración:
        # Se queda con el valor más alto encontrado hasta ahora para esa duración.
        activacion_salidas[termino_salida] = max(
            activacion_salidas[termino_salida], fuerza
        )

    # Devuelve el marcador final con la "fuerza" de cada posible duración
    return activacion_salidas
