import tkinter as tk
import math
import time
import random


class AguaBurbujas(tk.Canvas):
    def __init__(self, parent, width=180, height=180):
        super().__init__(
            parent, width=width, height=width, bg="#E0E5EC", highlightthickness=0
        )
        self.nivel_agua = 0.5
        self.burbujas = []
        self.animando = False

        self._dibujar_agua()
        self._crear_burbujas()

    def _dibujar_agua(self):
        self.delete("agua")
        self.delete("contenedor")

        altura_agua = 130 * self.nivel_agua

        # Contenedor de agua
        self.create_rectangle(
            8,
            180 - altura_agua,
            172,
            172,
            fill="#A3B1C6",
            outline="#7F8C8D",
            width=2,
            tags="contenedor",
        )

        # Agua
        self.create_rectangle(
            12,
            180 - altura_agua + 4,
            168,
            168,
            fill="#3498DB",
            outline="#2980B9",
            width=1,
            tags="agua",
        )

        # Superficie del agua con efecto de onda
        for i in range(12, 168, 8):
            altura_onda = math.sin(i * 0.1 + time.time() * 2) * 2
            self.create_line(
                i,
                180 - altura_agua + 4 + altura_onda,
                i + 8,
                180 - altura_agua + 4 + altura_onda,
                fill="#2980B9",
                width=2,
                tags="agua",
            )

    def _crear_burbujas(self):
        for _ in range(8):
            self.crear_burbuja()

    def crear_burbuja(self):
        x = random.randint(20, 160)
        y = random.randint(80, 150)
        radio = random.randint(2, 5)
        velocidad = random.uniform(0.3, 1.2)

        burbuja = {
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
            "x": x,
            "y": y,
            "radio": radio,
            "velocidad": velocidad,
        }
        self.burbujas.append(burbuja)

    def animar_burbujas(self):
        if self.animando:
            for burbuja in self.burbujas:
                burbuja["y"] -= burbuja["velocidad"]

                if burbuja["y"] < 40:
                    burbuja["y"] = 150
                    burbuja["x"] = random.randint(20, 160)

                self.coords(
                    burbuja["id"],
                    burbuja["x"] - burbuja["radio"],
                    burbuja["y"] - burbuja["radio"],
                    burbuja["x"] + burbuja["radio"],
                    burbuja["y"] + burbuja["radio"],
                )

            if random.random() < 0.3:
                self.crear_burbuja()

            if len(self.burbujas) > 12:
                burbuja_antigua = self.burbujas.pop(0)
                self.delete(burbuja_antigua["id"])

            self._dibujar_agua()
            self.after(100, self.animar_burbujas)

    def set_nivel_agua(self, nivel):
        self.nivel_agua = nivel / 100.0
        self._dibujar_agua()

    def iniciar_animacion(self):
        self.animando = True
        self.animar_burbujas()

    def detener_animacion(self):
        self.animando = False
        for burbuja in self.burbujas:
            self.delete(burbuja["id"])
        self.burbujas = []
        self._crear_burbujas()
