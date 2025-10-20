REGLAS = [
    # Reglas para 'No Grasosa'
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Muy Corto'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Media'}, 'then': 'Corto'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Media'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Media'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'No Grasosa', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Largo'},
    # Reglas para 'Media'
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Corto'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Media'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Media'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Corto'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Media'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'Media', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Largo'},
    # Reglas para 'Grasosa'
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Corto'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Media'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Poca', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Media'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Media', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Muy Largo'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Ligera'}, 'then': 'Medio'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Media'}, 'then': 'Largo'},
    {'if': {'Tipo de Suciedad': 'Grasosa', 'Grado de Suciedad': 'Mucha', 'Cantidad de Ropa': 'Pesada'}, 'then': 'Muy Largo'},

]

def motor_de_inferencia(valores_fuzzificados):
    activacion_salidas = {
        'Muy Corto':0.0, 'Corto':0.0, 'Medio':0.0,'Largo':0.0,'Muy Largo':0.0    
    }
    
    for regla in REGLAS:
        
        fuerza = min(
            valores_fuzzificados['tipo'][regla['if']['Tipo de Suciedad']],     # Número 1
            valores_fuzzificados['grado'][regla['if']['Grado de Suciedad']],    # Número 2
            valores_fuzzificados['cantidad'][regla['if']['Cantidad de Ropa']]  # Número 3
        )
        
        termino_salida = regla['then']
        activacion_salidas[termino_salida] = max(activacion_salidas[termino_salida],fuerza)
        
        
    return activacion_salidas