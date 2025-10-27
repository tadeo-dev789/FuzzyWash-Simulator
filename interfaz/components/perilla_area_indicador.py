import tkinter as tk  # Importa la librería para crear la interfaz gráfica
import math  # Importa la librería de matemáticas para cálculos de ángulos


# Define la clase de la Perilla, que hereda de tk.Canvas (un lienzo para dibujar)
class PerillaAreaIndicador(tk.Canvas):
    # El constructor de la clase, se llama cuando creas una PerillaAreaIndicador
    def __init__(
        self,
        parent,  # El 'padre' donde se dibujará (una ventana o un frame)
        width=110,  # Ancho del lienzo en píxeles
        height=130,  # Alto del lienzo en píxeles
        min_val=0,  # Valor mínimo que puede representar la perilla
        max_val=100,  # Valor máximo que puede representar la perilla
        label_text="",  # Texto que aparecerá debajo de la perilla
        command=None,  # Función a ejecutar cuando se suelta el clic después de mover la perilla
        initial_val=50,  # Valor inicial con el que empieza la perilla
    ):
        # Llama al constructor de la clase padre (tk.Canvas) para inicializar el lienzo
        super().__init__(
            parent, width=width, height=height, bg="#E0E5EC", bd=0, highlightthickness=0
        )

        # Guarda los valores de configuración en variables internas de la instancia
        self.min_val = min_val
        self.max_val = max_val
        self.command = command
        self._value = initial_val  # Guarda el valor actual (privado con '_')

        # Define la paleta de colores para el estilo neumórfico
        self.bg_color = "#E0E5EC"  # Color de fondo general
        self.shadow_dark = "#A3B1C6"  # Color para la sombra oscura
        self.shadow_light = "#FFFFFF"  # Color para la sombra clara (brillo)
        self.knob_color = "#E0E5EC"  # Color de la perilla misma
        self.indicator_color = (
            "#007AFF"  # Color del texto del valor y el arco indicador
        )
        self.area_color = "#007AFF"  # Color del arco que muestra el valor
        self.text_color = "#2C3E50"  # Color del texto de la etiqueta inferior

        # Define las dimensiones y posición de la perilla
        self.radius = 35  # Radio de la perilla
        self.center_x = width / 2  # Coordenada X del centro
        self.center_y = (
            height / 2 - 8
        )  # Coordenada Y del centro (un poco arriba para la etiqueta)

        # Define los ángulos de inicio y fin del movimiento de la perilla (en grados)
        self.start_angle = -135  # Ángulo inicial (como las 7 en un reloj)
        self.end_angle = 135  # Ángulo final (como las 5 en un reloj)

        # Llama a los métodos internos para dibujar la base y la etiqueta
        self._create_neumorphism_base()
        self._create_label(label_text)

        # Asocia eventos del mouse (clic, arrastrar, soltar) con métodos de la clase
        self.bind(
            "<ButtonPress-1>", self._on_press
        )  # Cuando se presiona el botón izquierdo
        self.bind(
            "<B1-Motion>", self._on_drag
        )  # Cuando se arrastra con el botón izquierdo presionado
        self.bind(
            "<ButtonRelease-1>", self._on_release
        )  # Cuando se suelta el botón izquierdo

        # Establece el valor inicial y dibuja el indicador correspondiente
        self.set_value(initial_val)

    # Método para dibujar la base estática de la perilla con efecto neumórfico
    def _create_neumorphism_base(self):
        # Dibuja la sombra oscura (círculo un poco más grande)
        self.create_oval(
            self.center_x - self.radius - 2,
            self.center_y - self.radius - 2,
            self.center_x + self.radius + 2,
            self.center_y + self.radius + 2,
            fill=self.shadow_dark,
            outline="",
            tags="shadow_dark",  # Etiqueta para poder referenciarla luego
        )

        # Dibuja la sombra clara (círculo un poco más grande, encima de la oscura)
        self.create_oval(
            self.center_x - self.radius - 1,
            self.center_y - self.radius - 1,
            self.center_x + self.radius + 1,
            self.center_y + self.radius + 1,
            fill=self.shadow_light,
            outline="",
            tags="shadow_light",  # Etiqueta
        )

        # Dibuja la base de la perilla (círculo del tamaño exacto, encima de las sombras)
        self.knob_base = self.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            fill=self.knob_color,
            outline="",
            tags="knob_base",  # Etiqueta
        )

        # Dibuja las marcas de la escala alrededor de la perilla
        for angle in range(
            -135, 136, 45
        ):  # Itera en ángulos de -135 a 135, de 45 en 45
            rad = math.radians(
                angle
            )  # Convierte el ángulo a radianes para usar seno/coseno
            # Calcula el punto interior de la marca
            inner_x = self.center_x + (self.radius - 6) * math.cos(rad)
            inner_y = self.center_y + (self.radius - 6) * math.sin(rad)
            # Calcula el punto exterior de la marca
            outer_x = self.center_x + (self.radius - 12) * math.cos(rad)
            outer_y = self.center_y + (self.radius - 12) * math.sin(rad)

            # Dibuja la línea (marca)
            self.create_line(
                inner_x,
                inner_y,
                outer_x,
                outer_y,
                fill="#A3B1C6",  # Color de la marca
                width=2,  # Grosor de la marca
                tags="scale_marks",  # Etiqueta
            )

    # Método para dibujar la etiqueta de texto debajo de la perilla
    def _create_label(self, label_text):
        # Crea un objeto de texto en el lienzo
        self.create_text(
            self.center_x,  # Posición X (centrada)
            self.center_y + self.radius + 15,  # Posición Y (debajo de la perilla)
            text=label_text,  # El texto a mostrar
            font=("Helvetica", 9, "bold"),  # Tipo de letra
            fill=self.text_color,  # Color del texto
            tags="label",  # Etiqueta
        )

    # Método para dibujar/actualizar el arco indicador y el texto del valor
    def _draw_area_indicator(self):
        # Borra los elementos anteriores (arco y texto) si existen
        self.delete("indicator")
        self.delete("value_text")

        # Calcula la proporción del valor actual dentro del rango (0.0 a 1.0)
        val_ratio = (
            (self._value - self.min_val) / (self.max_val - self.min_val)
            if (self.max_val - self.min_val) != 0
            else 0
        )
        # Convierte la proporción a un ángulo en grados dentro del rango de la perilla
        angle_deg = self.start_angle + (self.end_angle - self.start_angle) * val_ratio

        # Define el ángulo de inicio del arco (siempre -135)
        start_angle_arc = -135
        # Calcula la apertura (extent) del arco desde el inicio hasta el ángulo actual
        extent = angle_deg - start_angle_arc

        # Solo dibuja el arco si la apertura es positiva
        if extent > 0:
            # Dibuja el arco azul que representa el valor
            self.create_arc(
                self.center_x
                - self.radius
                + 4,  # Coordenadas del rectángulo que contiene el arco
                self.center_y - self.radius + 4,
                self.center_x + self.radius - 4,
                self.center_y + self.radius - 4,
                start=start_angle_arc,  # Ángulo de inicio
                extent=extent,  # Apertura del arco
                fill=self.area_color,  # Color de relleno
                outline="",  # Sin borde
                width=0,  # Grosor del borde (cero)
                style="arc",  # Estilo de dibujo (solo el arco)
                tags="indicator",  # Etiqueta
            )

        # Dibuja el texto con el valor numérico actual en el centro
        self.value_text = self.create_text(
            self.center_x,  # Posición X
            self.center_y,  # Posición Y
            text=f"{int(self._value)}",  # El valor actual (convertido a entero para mostrar)
            font=("Helvetica", 14, "bold"),  # Tipo de letra
            fill=self.indicator_color,  # Color del texto
            tags="value_text",  # Etiqueta
        )

    # Método para cambiar la apariencia (sombras) al presionar/soltar la perilla
    def _update_neumorphism_effect(self, pressed=False):
        if pressed:  # Si se está presionando
            # Invierte los colores de las sombras y oscurece la base para dar efecto de "hundido"
            self.itemconfig("shadow_dark", fill=self.shadow_light)
            self.itemconfig("shadow_light", fill=self.shadow_dark)
            self.itemconfig("knob_base", fill=self.shadow_dark)
        else:  # Si no se está presionando (estado normal)
            # Restaura los colores originales de las sombras y la base
            self.itemconfig("shadow_dark", fill=self.shadow_dark)
            self.itemconfig("shadow_light", fill=self.shadow_light)
            self.itemconfig("knob_base", fill=self.knob_color)

    # Método para calcular y actualizar el valor de la perilla basado en la posición del mouse
    def _update_value_from_event(self, event):
        # Calcula la diferencia entre la posición del mouse (event.x, event.y) y el centro
        dx = event.x - self.center_x
        dy = event.y - self.center_y

        # Calcula el ángulo de esa diferencia usando arcotangente2 (maneja todos los cuadrantes)
        angle_rad = math.atan2(dy, dx)
        # Convierte el ángulo a grados
        angle_deg = math.degrees(angle_rad)

        # Limita el ángulo calculado para que esté dentro del rango permitido (-135 a 135)
        # Asegura que no puedas girar la perilla más allá de los límites
        angle_deg = max(self.start_angle, min(self.end_angle, angle_deg))
        # Equivalente a:
        # if angle_deg < self.start_angle:
        #     angle_deg = self.start_angle
        # elif angle_deg > self.end_angle:
        #     angle_deg = self.end_angle

        # Convierte el ángulo (limitado) de nuevo a una proporción (0.0 a 1.0)
        total_angle_range = self.end_angle - self.start_angle
        val_ratio = (
            (angle_deg - self.start_angle) / total_angle_range
            if total_angle_range != 0
            else 0
        )
        # Calcula el nuevo valor basado en la proporción y los límites (min_val, max_val)
        new_value = self.min_val + (self.max_val - self.min_val) * val_ratio

        # Actualiza el valor interno de la perilla y redibuja el indicador
        self.set_value(new_value)
        # Devuelve el nuevo valor (útil para la función _on_press)
        return new_value

    # Método que se ejecuta cuando se presiona el botón izquierdo del mouse sobre la perilla
    def _on_press(self, event):
        # Aplica el efecto visual de "hundido"
        self._update_neumorphism_effect(True)
        # Calcula y actualiza el valor inmediatamente según dónde se hizo clic
        self._update_value_from_event(event)

    # Método que se ejecuta cuando se arrastra el mouse con el botón izquierdo presionado
    def _on_drag(self, event):
        # Calcula y actualiza el valor continuamente mientras se arrastra
        self._update_value_from_event(event)

    # Método que se ejecuta cuando se suelta el botón izquierdo del mouse
    def _on_release(self, event):
        # Restaura el efecto visual normal (no hundido)
        self._update_neumorphism_effect(False)
        # Si se definió una función 'command' al crear la perilla, la llama ahora
        if self.command:
            # Ejecuta la función 'command' pasándole el valor final de la perilla
            self.command(self._value)

    # Método público para obtener el valor actual de la perilla desde fuera de la clase
    def get_value(self):
        return self._value

    # Método público para establecer un valor a la perilla desde fuera de la clase
    def set_value(self, value):
        # Asegura que el valor esté dentro de los límites (min_val, max_val)
        self._value = max(self.min_val, min(self.max_val, value))
        # Redibuja el arco indicador y el texto para mostrar el nuevo valor
        self._draw_area_indicator()
