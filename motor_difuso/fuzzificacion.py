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
    
def fuzzify_grado_suciedad(valor_entrada):
    
    # Llama a membresia_triangular para 'Poca'
    # (Pico en 0, base de 0 a 50)
    poca = membresia_triangular(valor_entrada,0,0,50)
    
    # Llama a membresia_triangular para 'Media'
    # (Pico en 50, base de 0 a 100)
    media = membresia_triangular(valor_entrada,0,50,100)
    
    # Llama a membresia_triangular para 'Mucha'
    # (Pico en 100, base de 50 a 100)
    mucha  = membresia_triangular(valor_entrada,50,100,100)
    
    #Devuelve los tres resultados en un diccionario
    return {'poca':poca,'media':media,'mucha':mucha}

print(fuzzify_grado_suciedad(75))


