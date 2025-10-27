# Función de membresia para saber los grados de membresía.


def membresia_triangular(x: int, a: int, b: int, c: int) -> float:
    """
    Calcula los grados de membresia membresía para una función triangular [a, b, c].

    Parameters:
    --------
    x : Valor de la variable de entrada.
    a : Limite inferior de la función triangular.
    b : Altura máxima de la función triangular.
    c : Limite superior de la función triangular.
    """

    # Caso 1: Pico es el punto inicial (rampa de bajada, como "Poca")
    if a == b:
        if x <= a:
            return 1.0
        if x >= c:
            return 0.0
        return (c - x) / (c - a) if (c - a) != 0 else 0.0

    # Caso 2: Pico es el punto final (rampa de subida, como "Mucha" o "Muy Largo")
    if b == c:
        if x >= c:
            return 1.0
        if x <= a:
            return 0.0
        return (x - a) / (c - a) if (c - a) != 0 else 0.0

    # Caso 3: Triángulo normal (como "Media")
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a) if (b - a) != 0 else 0.0
    if b < x < c:
        return (c - x) / (c - b) if (c - b) != 0 else 0.0

    return 0.0


# def y(x, x0, x1):
#     return (x - x0) / (x1 - x0)


# --- Fuzzificar el GRADO de Suciedad ---
def fuzzify_grado_suciedad(valor_entrada):
    """
    Toma un número (0-100) que dice qué tan sucia está la ropa
    y calcula qué tanto es "Poca", "Media" o "Mucha" suciedad.
    """
    # Llama a la función del triángulo para cada categoría:
    # "Poca": Máxima en 0, baja hasta 50.
    poca = membresia_triangular(valor_entrada, 0, 0, 50)
    # "Media": Sube de 0 a 50, baja de 50 a 100.
    media = membresia_triangular(valor_entrada, 0, 50, 100)
    # "Mucha": Sube desde 50, máxima en 100.
    mucha = membresia_triangular(valor_entrada, 50, 100, 100)

    # Devuelve un diccionario diciendo qué tanto pertenece a cada una.
    return {"Poca": poca, "Media": media, "Mucha": mucha}


# --- Fuzzificar el TIPO de Suciedad ---
def fuzzify_tipo_suciedad(valor):
    """
    Toma un número (0-100) que representa qué tan grasosa es la suciedad
    y calcula qué tanto es "No Grasosa", "Media" o "Grasosa".
    """
    # Llama a la función del triángulo para cada categoría:
    noGrasosa = membresia_triangular(valor, 0, 0, 50)  # Rampa abajo 0-50
    media = membresia_triangular(
        valor, 12, 50, 90
    )  # Triángulo 12-50-90 (¡se traslapa!)
    grasosa = membresia_triangular(valor, 50, 100, 100)  # Rampa arriba 50-100

    # Devuelve el "grado de pertenencia" a cada tipo de suciedad.
    return {"No Grasosa": noGrasosa, "Media": media, "Grasosa": grasosa}


# --- Fuzzificar la CANTIDAD de Ropa ---
def fuzzify_cantidad_ropa(valor):
    """
    Toma un número (0-100) que representa cuánta ropa hay (ej. peso)
    y calcula qué tanto es "Ligera", "Media" o "Pesada".
    """
    # Llama a la función del triángulo para cada categoría:
    ligera = membresia_triangular(valor, 0, 0, 50)  # Rampa abajo 0-50
    media = membresia_triangular(valor, 0, 50, 90)  # Triángulo 0-50-90 (¡se traslapa!)
    pesada = membresia_triangular(valor, 50, 100, 100)  # Rampa arriba 50-100

    # Devuelve el "grado de pertenencia" a cada cantidad de ropa.
    return {"Ligera": ligera, "Media": media, "Pesada": pesada}
