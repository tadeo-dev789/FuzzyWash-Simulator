import unittest
import sys

from motor_difuso.fuzzificacion import (
    fuzzify_grado_suciedad,
    fuzzify_tipo_suciedad,
    fuzzify_cantidad_ropa
)

from motor_difuso.inferencia import motor_de_inferencia
from motor_difuso.defuzzificacion import defuzzify_centroide

class TestFuzzificacion(unittest.TestCase):
    
    # --- Pruebas para fuzzify_grado_suciedad ---

    def test_grado_suciedad_pico_media(self):
        """Prueba el valor (50), que debe ser 100% 'Media'."""
        valor_entrada = 50
        resultado_esperado = {'Poca': 0.0, 'Media': 1.0, 'Mucha': 0.0}
        resultado_real = fuzzify_grado_suciedad(valor_entrada)
        # self.assertEqual comprueba que los dos diccionarios son idénticos
        self.assertEqual(resultado_real, resultado_esperado)

    def test_grado_suciedad_cruce(self):
        """Prueba el valor (75), que debe ser 50% 'Media' y 50% 'Mucha'."""
        valor_entrada = 75
        resultado_esperado = {'Poca': 0.0, 'Media': 0.5, 'Mucha': 0.5}
        resultado_real = fuzzify_grado_suciedad(valor_entrada)
        self.assertEqual(resultado_real, resultado_esperado)

    def test_grado_suciedad_limite_inferior(self):
        """Prueba el valor (0), que debe ser 100% 'Poca'."""
        valor_entrada = 0
        resultado_esperado = {'Poca': 1.0, 'Media': 0.0, 'Mucha': 0.0}
        resultado_real = fuzzify_grado_suciedad(valor_entrada)
        self.assertEqual(resultado_real, resultado_esperado)

    # --- Pruebas para fuzzify_tipo_suciedad ---
    
    def test_tipo_suciedad_cruce_complejo(self):
        """Prueba el valor (30), que activa 'No Grasosa' y 'Media'."""
        valor_entrada = 30
        resultado_real = fuzzify_tipo_suciedad(valor_entrada)
        
        # Esperamos {'No Grasosa': 0.4, 'Media': 0.473..., 'Grasosa': 0.0}
        # Usamos self.assertAlmostEqual para comparar números decimales
        self.assertAlmostEqual(resultado_real['No Grasosa'], 0.4)
        self.assertAlmostEqual(resultado_real['Media'], 0.4736842105)
        self.assertAlmostEqual(resultado_real['Grasosa'], 0.0)

    # --- Pruebas para fuzzify_cantidad_ropa ---

    def test_cantidad_ropa_pico_media(self):
        """Prueba el valor (50), que debe ser 100% 'Media'."""
        valor_entrada = 50
        resultado_esperado = {'Ligera': 0.0, 'Media': 1.0, 'Pesada': 0.0}
        resultado_real = fuzzify_cantidad_ropa(valor_entrada)
        self.assertEqual(resultado_real, resultado_esperado)
        
        
    # --- PRUEBA DE INTEGRACIÓN ---
    
    def test_pipeline_completo_caso_50_50_50(self):
        """
        Prueba el pipeline completo (Fuzzify -> Inferir -> Defuzzify)
        con el caso de prueba (50, 50, 50) del artículo.
        """
        print("\n\n--- Ejecutando Prueba de Integración (50, 50, 50) ---")
        
        # --- Datos de Entrada ---
        val_tipo = 50
        val_grado = 50
        val_cantidad = 50
        
        # --- PASO 1: FUZZIFICACIÓN ---
        fuzz_tipo = fuzzify_tipo_suciedad(val_tipo)
        fuzz_grado = fuzzify_grado_suciedad(val_grado)
        fuzz_cantidad = fuzzify_cantidad_ropa(val_cantidad)
        
        valores_fuzzificados = {'tipo': fuzz_tipo, 'grado': fuzz_grado, 'cantidad': fuzz_cantidad}
        
        # --- PASO 2: INFERENCIA ---
        activacion_salidas = motor_de_inferencia(valores_fuzzificados)
        
        # Comprobación intermedia (opcional pero recomendada)
        resultado_inferencia_esperado = {'Muy Corto': 0.0, 'Corto': 0.0, 'Medio': 0.0, 'Largo': 1.0, 'Muy Largo': 0.0}
        self.assertEqual(activacion_salidas, resultado_inferencia_esperado)
        
        # --- PASO 3: DEFUZZIFICACIÓN ---
        tiempo_final = defuzzify_centroide(activacion_salidas)
        
        # Resultado esperado (como calculamos antes)
        resultado_final_esperado = 50.33333
        
        # --- VALIDACIÓN FINAL ---
        # Comparamos si el resultado real es "casi igual" al esperado
        # (usamos 2 decimales de precisión para la prueba)
        self.assertAlmostEqual(tiempo_final, resultado_final_esperado, places=2)
        print(f"¡Prueba de Integración Exitosa! Resultado final: {tiempo_final:.2f}")
        
        # ... (Aquí va tu prueba de integración test_pipeline_completo...)

    # --- PRUEBAS DE SANIDAD (COHERENCIA) ---
    
    def test_pipeline_peor_caso_posible(self):
        """
        Prueba de Sanidad: El peor caso (todo al 95%) debe dar un tiempo 'Muy Largo'.
        """
        print("\n--- Ejecutando Prueba de Sanidad (Peor Caso) ---")
        val_tipo = 95
        val_grado = 95
        val_cantidad = 95

        # 1. Fuzzificación
        fuzz_tipo = fuzzify_tipo_suciedad(val_tipo)
        fuzz_grado = fuzzify_grado_suciedad(val_grado)
        fuzz_cantidad = fuzzify_cantidad_ropa(val_cantidad)
        
        # (Esto dará {'Grasosa': 0.9, ...}, {'Mucha': 0.9, ...}, {'Pesada': 0.9, ...})
        valores_fuzzificados = {'tipo': fuzz_tipo, 'grado': fuzz_grado, 'cantidad': fuzz_cantidad}
        
        # 2. Inferencia
        # Esto debería activar fuertemente la Regla 27: (Grasosa, Mucha, Pesada) -> Muy Largo
        activacion_salidas = motor_de_inferencia(valores_fuzzificados)

        # 3. Defuzzificación
        tiempo_final = defuzzify_centroide(activacion_salidas)
        
        # VALIDACIÓN: Comprobamos que el tiempo es muy alto (ej. mayor a 55 minutos)
        print(f"Resultado 'Peor Caso': {tiempo_final:.2f} min")
        self.assertGreater(tiempo_final, 55, "El peor caso no dio un tiempo suficientemente largo.")

    def test_pipeline_mejor_caso_posible(self):
        """
        Prueba de Sanidad: El mejor caso (todo al 5%) debe dar un tiempo 'Muy Corto'.
        """
        print("\n--- Ejecutando Prueba de Sanidad (Mejor Caso) ---")
        val_tipo = 5
        val_grado = 5
        val_cantidad = 5

        # 1. Fuzzificación
        fuzz_tipo = fuzzify_tipo_suciedad(val_tipo)
        fuzz_grado = fuzzify_grado_suciedad(val_grado)
        fuzz_cantidad = fuzzify_cantidad_ropa(val_cantidad)
        
        # (Esto dará {'No Grasosa': 0.9, ...}, {'Poca': 0.9, ...}, {'Ligera': 0.9, ...})
        valores_fuzzificados = {'tipo': fuzz_tipo, 'grado': fuzz_grado, 'cantidad': fuzz_cantidad}
        
        # 2. Inferencia
        # Esto debería activar fuertemente la Regla 1: (No Grasosa, Poca, Ligera) -> Muy Corto
        activacion_salidas = motor_de_inferencia(valores_fuzzificados)

        # 3. Defuzzificación
        tiempo_final = defuzzify_centroide(activacion_salidas)
        
        # VALIDACIÓN: Comprobamos que el tiempo es muy bajo (ej. menor a 15 minutos)
        print(f"Resultado 'Mejor Caso': {tiempo_final:.2f} min")
        self.assertLess(tiempo_final, 20, "El mejor caso no dio un tiempo suficientemente corto.")


if __name__ == '__main__':
    unittest.main()