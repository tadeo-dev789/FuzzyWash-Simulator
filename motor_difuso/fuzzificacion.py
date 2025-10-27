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


def fuzzify_grado_suciedad(valor_entrada):
    # Llama a membresia_triangular para 'Poca'
    # (Pico en 0, base de 0 a 50)
    poca = membresia_triangular(valor_entrada, 0, 0, 50)

    # Llama a membresia_triangular para 'Media'
    # (Pico en 50, base de 0 a 100)
    media = membresia_triangular(valor_entrada, 0, 50, 100)

    # Llama a membresia_triangular para 'Mucha'
    # (Pico en 100, base de 50 a 100)
    mucha = membresia_triangular(valor_entrada, 50, 100, 100)

    # Devuelve los tres resultados en un diccionario con claves que coincidan
    return {"Poca": poca, "Media": media, "Mucha": mucha}


def fuzzify_tipo_suciedad(valor):
    noGrasosa = membresia_triangular(valor, 0, 0, 50)
    media = membresia_triangular(valor, 12, 50, 90)
    grasosa = membresia_triangular(valor, 50, 100, 100)

    return {"No Grasosa": noGrasosa, "Media": media, "Grasosa": grasosa}


def fuzzify_cantidad_ropa(valor):
    ligera = membresia_triangular(valor, 0, 0, 50)
    media = membresia_triangular(valor, 0, 50, 90)
    pesada = membresia_triangular(valor, 50, 100, 100)

    return {"Ligera": ligera, "Media": media, "Pesada": pesada}
