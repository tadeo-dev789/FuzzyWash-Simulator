def membresia_triangular(x , a , b , c):
    #Revisamos si la x está fuera de la base del triangulo, la cual corresponde [a,c]
    if x <= a or x>= c :
        return 0;
    #Luego, revisamos si x está en la pendiente de subida entre [a ,b]
    elif a < x <= b:
        return (x - a) / (b - a)
    # Ya al final, revisamos si x está en la pendiente de bajada  entre [b,c]
    elif b < x < c:
        return (c - x) / (c - b)
    
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


