from .fuzzificacion import membresia_triangular

# Primeramente, definimos las funciones de memebresia para la salida
# para que la funcion de defuzzificación sepa cómo son las formas que debe equilibrar. 
SALIDA_MEMBRESIA = {
    'Muy Corto':    lambda x: membresia_triangular(x, 0, 8, 23),
    'Corto':        lambda x: membresia_triangular(x, 8, 23, 38),
    'Medio':        lambda x: membresia_triangular(x, 23, 38, 53),
    'Largo':        lambda x: membresia_triangular(x, 38, 53, 60),
    'Muy Largo':    lambda x: membresia_triangular(x, 53, 60, 60)
}

def defuzzify_centroide(activacion_salidas):
    numerador = 0.0
    denominador = 0.0
    
    paso = 0.5
    
    for x in range(int(60/paso) + 1):
        tiempo = x * paso
        
        grado_agregado = 0.0
        for  termino,fuerza in activacion_salidas.items():
            membresia_cortada  = min(fuerza, SALIDA_MEMBRESIA[termino](tiempo))
            
            grado_agregado = max(grado_agregado,membresia_cortada)
            
        numerador += tiempo * grado_agregado
        denominador += grado_agregado
    
    if denominador == 0:
        return 0.0
    
    return numerador / denominador;   

