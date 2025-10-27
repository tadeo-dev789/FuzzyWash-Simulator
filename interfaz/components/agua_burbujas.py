import tkinter as tk  # La librería para dibujar
import math  # Para la onda del agua (seno)
import time  # Para que la onda del agua cambie con el tiempo
import random  # Para que las burbujas salgan y se muevan diferente


# Define la clase AguaBurbujas, que hereda de tk.Canvas (un lienzo)
class AguaBurbujas(tk.Canvas):
    # El constructor, se llama al crear un AguaBurbujas
    def __init__(self, parent, width=180, height=180):
        # Llama al constructor de tk.Canvas para preparar el lienzo
        super().__init__(
            parent,
            width=width,
            height=height,
            bg="#E0E5EC",
            highlightthickness=0,  # OJO: height aquí usa width, quizás un typo? Debería ser height=height.
        )
        # Guarda el nivel del agua (0.0 = vacío, 1.0 = lleno), empieza a la mitad
        self.nivel_agua = 0.5
        # Lista para guardar la información de cada burbuja
        self.burbujas = []
        # Bandera para saber si la animación está corriendo
        self.animando = False

        # Llama a las funciones para dibujar el agua inicial y crear las primeras burbujas
        self._dibujar_agua()
        self._crear_burbujas()

    # Método para dibujar (o redibujar) el contenedor y el agua
    def _dibujar_agua(self):
        # Borra los dibujos anteriores de agua y contenedor para actualizarlos
        self.delete("agua")
        self.delete("contenedor")

        # Calcula la altura del agua en píxeles basado en self.nivel_agua
        # Asume que el área de agua tiene una altura máxima de 130 píxeles
        altura_agua = 130 * self.nivel_agua

        # Dibuja el rectángulo exterior (como el recipiente gris)
        self.create_rectangle(
            8,
            180
            - altura_agua,  # Coordenada superior izquierda (Y depende de la altura del agua)
            172,
            172,  # Coordenada inferior derecha
            fill="#A3B1C6",
            outline="#7F8C8D",
            width=2,
            tags="contenedor",
        )

        # Dibuja el rectángulo interior (el agua azul)
        self.create_rectangle(
            12,
            180 - altura_agua + 4,  # Un poco más adentro y abajo que el contenedor
            168,
            168,
            fill="#3498DB",
            outline="#2980B9",
            width=1,
            tags="agua",
        )

        # Dibuja la superficie del agua con un efecto de onda
        # Usa la función seno y el tiempo actual para que la línea suba y baje
        for i in range(
            12, 168, 8
        ):  # Dibuja pequeños segmentos de línea horizontalmente
            # Calcula qué tan alta debe ser la onda en este punto
            altura_onda = math.sin(i * 0.1 + time.time() * 2) * 2
            # Dibuja un segmento de línea en la superficie, con la altura de la onda
            self.create_line(
                i,
                180 - altura_agua + 4 + altura_onda,
                i + 8,
                180 - altura_agua + 4 + altura_onda,
                fill="#2980B9",
                width=2,
                tags="agua",
            )

    # Método para crear el lote inicial de burbujas
    def _crear_burbujas(self):
        # Llama a la función crear_burbuja 8 veces
        for _ in range(8):
            self.crear_burbuja()

    # Método para crear UNA nueva burbuja
    def crear_burbuja(self):
        # Elige una posición X al azar dentro del agua
        x = random.randint(20, 160)
        # Elige una posición Y inicial al azar (más abajo)
        y = random.randint(80, 150)
        # Elige un tamaño (radio) al azar
        radio = random.randint(2, 5)
        # Elige una velocidad de subida al azar
        velocidad = random.uniform(0.3, 1.2)

        # Guarda la información de la burbuja en un diccionario
        burbuja = {
            # Dibuja el óvalo (la burbuja) y guarda su ID para poder moverla luego
            "id": self.create_oval(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                fill="white",
                outline="#AED6F1",
                width=1,
                tags="burbuja",
            ),
            "x": x,  # Guarda su posición X
            "y": y,  # Guarda su posición Y
            "radio": radio,  # Guarda su tamaño
            "velocidad": velocidad,  # Guarda su velocidad
        }
        # Añade la nueva burbuja a la lista de burbujas activas
        self.burbujas.append(burbuja)

    # El motor de la animación de las burbujas (y la onda del agua)
    def animar_burbujas(self):
        # Solo se ejecuta si la bandera 'animando' está encendida
        if self.animando:
            # Recorre cada burbuja en la lista
            for burbuja in self.burbujas:
                # Mueve la burbuja hacia arriba restando su velocidad a la coordenada Y
                burbuja["y"] -= burbuja["velocidad"]

                # Si la burbuja llega muy arriba (cerca de la superficie)...
                if burbuja["y"] < 40:
                    # ...la "reinicia" abajo con una nueva posición X al azar
                    burbuja["y"] = 150
                    burbuja["x"] = random.randint(20, 160)

                # Actualiza la posición del dibujo de la burbuja en el lienzo
                self.coords(
                    burbuja["id"],
                    burbuja["x"] - burbuja["radio"],
                    burbuja["y"] - burbuja["radio"],
                    burbuja["x"] + burbuja["radio"],
                    burbuja["y"] + burbuja["radio"],
                )

            # --- Gestión de cantidad de burbujas ---
            # A veces (30% de probabilidad) crea una nueva burbuja
            if random.random() < 0.3:
                self.crear_burbuja()

            # Si hay demasiadas burbujas (más de 12)...
            if len(self.burbujas) > 12:
                # ...elimina la burbuja más vieja de la lista
                burbuja_antigua = self.burbujas.pop(0)
                # Y borra su dibujo del lienzo
                self.delete(burbuja_antigua["id"])

            # Redibuja el agua (para actualizar la onda de la superficie)
            self._dibujar_agua()
            # Le dice a Tkinter: "En 100 milisegundos, vuelve a llamar a esta función 'animar_burbujas'"
            # Esto crea el bucle de animación
            self.after(100, self.animar_burbujas)

    # Método público para cambiar el nivel del agua desde fuera
    def set_nivel_agua(self, nivel):
        # Convierte el nivel (0-100) a una proporción (0.0-1.0)
        self.nivel_agua = (
            nivel / 100.0 if nivel >= 0 and nivel <= 100 else 0.5
        )  # Ensure level is valid
        # Redibuja el agua con la nueva altura
        self._dibujar_agua()

    # Método público para iniciar la animación
    def iniciar_animacion(self):
        # Prende la bandera 'animando'
        self.animando = True
        # Llama a la función de animación para empezar el bucle
        self.animar_burbujas()

    # Método público para detener la animación
    def detener_animacion(self):
        # Apaga la bandera 'animando' (esto detendrá el bucle en 'animar_burbujas')
        self.animando = False
        # Borra todas las burbujas existentes del lienzo
        for burbuja in self.burbujas:
            self.delete(burbuja["id"])
        # Vacía la lista de burbujas
        self.burbujas = []
        # Crea un nuevo lote inicial de burbujas (para la próxima vez que inicie)
        self._crear_burbujas()
