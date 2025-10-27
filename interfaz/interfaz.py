import tkinter as tk
from .components.tambor_lavadora import TamborLavadora
from .components.agua_burbujas import AguaBurbujas
from .components.perilla_area_indicador import PerillaAreaIndicador
from .components.boton import BotonNeumorphism
from .components.display_digital import DisplayDigital
import sys
from os.path import expanduser

# Add config directory to Python path
sys.path.append(expanduser("~/.config/qtile"))

try:
    from motor_difuso.fuzzificacion import (
        fuzzify_tipo_suciedad,
        fuzzify_grado_suciedad,
        fuzzify_cantidad_ropa,
        membresia_triangular,  # Import membresia_triangular if needed here
    )
    from motor_difuso.inferencia import (
        motor_de_inferencia,
        REGLAS,
    )  # Import REGLAS if needed here
    from motor_difuso.defuzzificacion import (
        defuzzify_centroide,
        SALIDA_MEMBRESIA,
    )  # Import SALIDA_MEMBRESIA if needed here
except ImportError:
    print(
        "Error: No se encontraron los archivos del 'motor_difuso'. Usando valores por defecto."
    )

    # Fallback functions if fuzzy logic engine files are missing
    # --- Define membresia_triangular fallback ---
    def membresia_triangular(x: int, a: int, b: int, c: int) -> float:
        if a == b:
            if x <= a:
                return 1.0
            if x >= c:
                return 0.0
            return (c - x) / (c - a) if (c - a) != 0 else 0.0
        if b == c:
            if x >= c:
                return 1.0
            if x <= a:
                return 0.0
            return (x - a) / (c - a) if (c - a) != 0 else 0.0
        if x <= a or x >= c:
            return 0.0
        if a < x <= b:
            return (x - a) / (b - a) if (b - a) != 0 else 0.0
        if b < x < c:
            return (c - x) / (c - b) if (c - b) != 0 else 0.0
        return 0.0

    # --- Define REGLAS fallback ---
    REGLAS = [
        {
            "if": {
                "Tipo de Suciedad": "Media",
                "Grado de Suciedad": "Media",
                "Cantidad de Ropa": "Media",
            },
            "then": "Medio",
        }
    ]  # Minimal rule

    # --- Define SALIDA_MEMBRESIA fallback ---
    SALIDA_MEMBRESIA = {
        "Muy Corto": lambda x: membresia_triangular(x, 0, 8, 23),
        "Corto": lambda x: membresia_triangular(x, 8, 23, 38),
        "Medio": lambda x: membresia_triangular(x, 23, 38, 53),
        "Largo": lambda x: membresia_triangular(x, 38, 53, 60),
        "Muy Largo": lambda x: membresia_triangular(x, 53, 60, 60),
    }

    # --- Define fuzzy/inference/defuzzify fallbacks ---
    def fuzzify_tipo_suciedad(v):
        return {"Media": 1.0, "No Grasosa": 0.0, "Grasosa": 0.0}

    def fuzzify_grado_suciedad(v):
        return {"Media": 1.0, "Poca": 0.0, "Mucha": 0.0}

    def fuzzify_cantidad_ropa(v):
        return {"Media": 1.0, "Ligera": 0.0, "Pesada": 0.0}

    def motor_de_inferencia(valores_fuzzificados):
        activacion_salidas = {
            "Muy Corto": 0.0,
            "Corto": 0.0,
            "Medio": 0.0,
            "Largo": 0.0,
            "Muy Largo": 0.0,
        }
        for regla in REGLAS:
            try:
                fuerza = min(
                    valores_fuzzificados["tipo"].get(
                        regla["if"]["Tipo de Suciedad"], 0.0
                    ),
                    valores_fuzzificados["grado"].get(
                        regla["if"]["Grado de Suciedad"], 0.0
                    ),
                    valores_fuzzificados["cantidad"].get(
                        regla["if"]["Cantidad de Ropa"], 0.0
                    ),
                )
                termino_salida = regla["then"]
                activacion_salidas[termino_salida] = max(
                    activacion_salidas[termino_salida], fuerza
                )
            except KeyError:
                continue  # Ignore rule if keys don't match fallbacks
        if all(
            v == 0.0 for v in activacion_salidas.values()
        ):  # Ensure at least one output has strength if using minimal rule
            activacion_salidas["Medio"] = 1.0
        return activacion_salidas

    def defuzzify_centroide(activacion_salidas):
        numerador = 0.0
        denominador = 0.0
        paso = 0.5
        for x in range(int(60 / paso) + 1):
            tiempo = x * paso
            grado_agregado = 0.0
            for termino, fuerza in activacion_salidas.items():
                if termino in SALIDA_MEMBRESIA:  # Check if term exists
                    membresia_cortada = min(fuerza, SALIDA_MEMBRESIA[termino](tiempo))
                    grado_agregado = max(grado_agregado, membresia_cortada)
            numerador += tiempo * grado_agregado
            denominador += grado_agregado
        if denominador == 0:
            return 45.0  # Return default time if no rule fired
        return numerador / denominador


class FuzzyWashSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("FuzzyWash Simulator")
        self.root.geometry("750x650")
        self.root.configure(bg="#E0E5EC")
        self.root.resizable(False, False)

        self.running = False
        self.current_time = 0.0
        self.total_time = 45.0
        self.modo_centrifugado = False
        self.indicadores = []  # Initialize indicators list

        self._create_panel()
        self.calcular()  # Calculate initial time

    def _create_panel(self):
        self.panel_principal = tk.Frame(self.root, bg="#E0E5EC", bd=0)
        self.panel_principal.pack(fill="both", expand=True, padx=20, pady=15)

        title_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        title_frame.pack(pady=5)

        tk.Label(
            title_frame,
            text="FUZZYWASH SIMULATOR",
            font=("Helvetica", 20, "bold"),
            bg="#E0E5EC",
            fg="#2C3E50",
        ).pack()

        tk.Label(
            title_frame,
            text="Sistema Inteligente de Lavado",
            font=("Helvetica", 10),
            bg="#E0E5EC",
            fg="#7F8C8D",
        ).pack(pady=2)

        self._create_controles_superiores()
        self._create_seccion_media()
        self._create_animaciones_con_leds()

    def _create_controles_superiores(self):
        controles_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        controles_frame.pack(fill="x", padx=15, pady=15)

        self.perilla_tipo_suciedad = PerillaAreaIndicador(
            controles_frame, label_text="TIPO SUCIEDAD", command=self.calcular
        )
        self.perilla_tipo_suciedad.pack(side="left", padx=15)

        self.perilla_grado_suciedad = PerillaAreaIndicador(
            controles_frame, label_text="GRADO SUCIEDAD", command=self.calcular
        )
        self.perilla_grado_suciedad.pack(side="left", padx=15)

        self.perilla_cantidad_ropa = PerillaAreaIndicador(
            controles_frame, label_text="CANTIDAD ROPA", command=self.calcular
        )
        self.perilla_cantidad_ropa.pack(side="left", padx=15)

        boton_container = tk.Frame(controles_frame, bg="#E0E5EC")
        boton_container.pack(side="right", padx=15)

        self.boton_inicio = BotonNeumorphism(
            boton_container,
            text="INICIO",
            command=self.toggle_inicio,
        )
        self.boton_inicio.pack(pady=3)

        luz_frame = tk.Frame(boton_container, bg="#E0E5EC")
        luz_frame.pack()

        tk.Label(
            luz_frame,
            text="EN MARCHA",
            bg="#E0E5EC",
            font=("Helvetica", 7),
            fg="#7F8C8D",
        ).pack()

        self.luz_indicador = tk.Canvas(
            luz_frame, width=18, height=18, bg="#E0E5EC", highlightthickness=0
        )
        self.luz_indicador.pack()
        self.luz_id = self.luz_indicador.create_oval(
            2, 2, 16, 16, fill="#E74C3C", outline="#A3B1C6", width=1
        )

    def _create_seccion_media(self):
        media_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        media_frame.pack(fill="x", padx=15, pady=8)

        display_container = tk.Frame(media_frame, bg="#E0E5EC")
        display_container.pack(pady=8)

        self.display = DisplayDigital(display_container, width=280, height=90)
        self.display.pack()

    def _create_animaciones_con_leds(self):
        animaciones_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        animaciones_frame.pack(fill="x", padx=15, pady=10)

        fila_container = tk.Frame(animaciones_frame, bg="#E0E5EC")
        fila_container.pack()

        leds_izquierdos_frame = tk.Frame(fila_container, bg="#E0E5EC")
        leds_izquierdos_frame.pack(side="left", padx=10)

        indicadores_izquierdos = [("LAVADO", "#E0E5EC"), ("ENJUAGUE", "#E0E5EC")]

        for i, (texto, color) in enumerate(indicadores_izquierdos):
            frame = tk.Frame(leds_izquierdos_frame, bg="#E0E5EC")
            frame.pack(pady=8)
            led_canvas = tk.Canvas(
                frame, width=40, height=40, bg="#E0E5EC", highlightthickness=0
            )
            led_canvas.pack(pady=2)
            led_canvas.create_oval(5, 5, 35, 35, fill="#A3B1C6", outline="")
            led_canvas.create_oval(3, 3, 33, 33, fill="#FFFFFF", outline="")
            led_id = led_canvas.create_oval(8, 8, 30, 30, fill="#E74C3C", outline="")
            tk.Label(
                frame,
                text=texto,
                bg="#E0E5EC",
                font=("Helvetica", 9, "bold"),
                fg="#2C3E50",
            ).pack()
            self.indicadores.append(
                {"canvas": led_canvas, "led_id": led_id, "text": texto, "activo": False}
            )

        animaciones_centro_frame = tk.Frame(fila_container, bg="#E0E5EC")
        animaciones_centro_frame.pack(side="left", padx=20)

        tambor_frame = tk.Frame(animaciones_centro_frame, bg="#E0E5EC")
        tambor_frame.pack(side="left", padx=15, pady=5)
        tk.Label(
            tambor_frame,
            text="TAMBOR",
            bg="#E0E5EC",
            font=("Helvetica", 9, "bold"),
            fg="#2C3E50",
        ).pack(pady=(0, 3))
        self.tambor = TamborLavadora(tambor_frame, width=180, height=180)
        self.tambor.pack()

        agua_frame = tk.Frame(animaciones_centro_frame, bg="#E0E5EC")
        agua_frame.pack(side="left", padx=15, pady=5)
        tk.Label(
            agua_frame,
            text="AGUA Y DETERGENTE",
            bg="#E0E5EC",
            font=("Helvetica", 9, "bold"),
            fg="#2C3E50",
        ).pack(pady=(0, 3))
        self.agua = AguaBurbujas(agua_frame, width=180, height=180)
        self.agua.pack()

        leds_derechos_frame = tk.Frame(fila_container, bg="#E0E5EC")
        leds_derechos_frame.pack(side="left", padx=10)
        indicadores_derechos = [("CENTRIFUGADO", "#E0E5EC"), ("FINALIZADO", "#E0E5EC")]
        for i, (texto, color) in enumerate(indicadores_derechos):
            frame = tk.Frame(leds_derechos_frame, bg="#E0E5EC")
            frame.pack(pady=8)
            led_canvas = tk.Canvas(
                frame, width=40, height=40, bg="#E0E5EC", highlightthickness=0
            )
            led_canvas.pack(pady=2)
            led_canvas.create_oval(5, 5, 35, 35, fill="#A3B1C6", outline="")
            led_canvas.create_oval(3, 3, 33, 33, fill="#FFFFFF", outline="")
            led_id = led_canvas.create_oval(8, 8, 30, 30, fill="#E74C3C", outline="")
            tk.Label(
                frame,
                text=texto,
                bg="#E0E5EC",
                font=("Helvetica", 9, "bold"),
                fg="#2C3E50",
            ).pack()
            self.indicadores.append(
                {"canvas": led_canvas, "led_id": led_id, "text": texto, "activo": False}
            )

    def _formatear_tiempo(self, tiempo_minutos):
        minutos_enteros = int(tiempo_minutos)
        segundos = int((tiempo_minutos - minutos_enteros) * 60)
        return f"{minutos_enteros:02d}:{segundos:02d}"

    def toggle_inicio(self):
        self.running = not self.running
        if self.running:
            self.boton_inicio.config(text="PAUSAR", fg="#E67E22")
            self.luz_indicador.itemconfig(self.luz_id, fill="#27AE60")
            self._iniciar_animaciones()
            self._iniciar_conteo()
        else:
            self.boton_inicio.config(text="INICIO", fg="#27AE60")
            self.luz_indicador.itemconfig(self.luz_id, fill="#E74C3C")
            self._detener_animaciones()

    def _iniciar_animaciones(self):
        if self.modo_centrifugado:
            self.tambor.iniciar_centrifugado()
        else:
            self.tambor.iniciar_lavado()
        self.agua.iniciar_animacion()
        self.agua.set_nivel_agua(self.perilla_tipo_suciedad.get_value())
        self._actualizar_indicadores_fase()

    def _detener_animaciones(self):
        self.tambor.detener()
        self.agua.detener_animacion()

    def _actualizar_indicadores_fase(self):
        tiempo_restante = self.total_time - self.current_time
        fase_activa = -1  # Index of the active phase indicator

        if tiempo_restante > self.total_time * 0.6:
            fase_activa = 0  # LAVADO
            self.modo_centrifugado = False
        elif tiempo_restante > self.total_time * 0.3:
            fase_activa = 1  # ENJUAGUE
            self.modo_centrifugado = False
        elif tiempo_restante > 0:
            fase_activa = 2  # CENTRIFUGADO
            self.modo_centrifugado = True
            # Re-trigger spin if already running in this phase
            if self.running and not self.tambor.is_spinning_fast():
                self.tambor.detener()
                self.tambor.iniciar_centrifugado()
        else:  # tiempo_restante <= 0
            fase_activa = 3  # FINALIZADO
            self.modo_centrifugado = False  # Ensure spin stops when finished

        for idx, indicador in enumerate(self.indicadores):
            color = "#27AE60" if idx == fase_activa else "#E74C3C"
            indicador["canvas"].itemconfig(indicador["led_id"], fill=color)
            indicador["activo"] = idx == fase_activa

    def _iniciar_conteo(self):
        if self.running and self.current_time < self.total_time:
            # Increment time slightly faster for simulation feel if needed, here 1 sec = 1/60 min
            self.current_time += 1 / 60
            tiempo_restante = max(0, self.total_time - self.current_time)
            tiempo_formateado = self._formatear_tiempo(tiempo_restante)
            self.display.set_time(tiempo_formateado)
            self._actualizar_indicadores_fase()
            self.root.after(
                1000, self._iniciar_conteo
            )  # Call again after 1000 ms (1 second)
        elif self.current_time >= self.total_time and self.running:
            # Ensure state consistency before calling completed
            self.current_time = self.total_time
            tiempo_formateado = self._formatear_tiempo(0)
            self.display.set_time(tiempo_formateado)
            self._ciclo_completado()

    def _ciclo_completado(self):
        self.running = False
        self.boton_inicio.config(text="INICIO", fg="#27AE60")
        self.luz_indicador.itemconfig(self.luz_id, fill="#E74C3C")
        self.display.set_time("00:00")
        self.current_time = 0.0
        self._detener_animaciones()
        self._actualizar_indicadores_fase()  # Should light up FINALIZADO
        self.display.set_time("LISTO!")

    def calcular(self, event=None):
        val_cantidad = self.perilla_cantidad_ropa.get_value()
        val_tipo = self.perilla_tipo_suciedad.get_value()
        val_grado = self.perilla_grado_suciedad.get_value()

        fuzz_tipo = fuzzify_tipo_suciedad(val_tipo)
        fuzz_grado = fuzzify_grado_suciedad(val_grado)
        fuzz_cantidad = fuzzify_cantidad_ropa(val_cantidad)

        valores_fuzzificados = {
            "tipo": fuzz_tipo,
            "grado": fuzz_grado,
            "cantidad": fuzz_cantidad,
        }

        activacion_salidas = motor_de_inferencia(valores_fuzzificados)
        tiempo_final = defuzzify_centroide(activacion_salidas)

        self.total_time = (
            tiempo_final if tiempo_final > 0 else 0.1
        )  # Ensure minimum time
        self.current_time = 0.0

        if not self.running:
            tiempo_formateado = self._formatear_tiempo(self.total_time)
            self.display.set_time(tiempo_formateado)

        self.agua.set_nivel_agua(self.perilla_tipo_suciedad.get_value())


def iniciar_app():
    root = tk.Tk()
    app = FuzzyWashSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_app()
