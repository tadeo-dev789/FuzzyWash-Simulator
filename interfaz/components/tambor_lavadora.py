import tkinter as tk
import math


class TamborLavadora(tk.Canvas):
    def __init__(self, parent, width=180, height=180):
        super().__init__(
            parent, width=width, height=height, bg="#E0E5EC", highlightthickness=0
        )
        self.center_x = width // 2
        self.center_y = height // 2
        self.radius = 50
        self.angle = 0
        self.animating = False

        self._crear_tambor()
        self._crear_ropa()

    def _crear_tambor(self):
        # Tambor exterior (cristal)
        self.create_oval(
            self.center_x - self.radius - 8,
            self.center_y - self.radius - 8,
            self.center_x + self.radius + 8,
            self.center_y + self.radius + 8,
            fill="#A3B1C6",
            outline="#7F8C8D",
            width=2,
        )

        # Tambor interior
        self.tambor_interior = self.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            fill="#3498DB",
            outline="#2980B9",
            width=2,
        )

        # Agujeros del tambor
        for i in range(0, 360, 30):
            rad = math.radians(i)
            x = self.center_x + (self.radius - 4) * math.cos(rad)
            y = self.center_y + (self.radius - 4) * math.sin(rad)
            self.create_oval(
                x - 1.5, y - 1.5, x + 1.5, y + 1.5, fill="#FFFFFF", outline=""
            )

    def _crear_ropa(self):
        # Crear prendas de ropa dentro del tambor con puntos iniciales
        puntos_camiseta = [self.center_x, self.center_y] * 4
        self.camiseta = self.create_polygon(
            puntos_camiseta, fill="#E74C3C", outline="#C0392B", tags="ropa"
        )

        puntos_pantalon = [self.center_x, self.center_y] * 4
        self.pantalon = self.create_polygon(
            puntos_pantalon, fill="#2C3E50", outline="#34495E", tags="ropa"
        )

        self.calcetin = self.create_oval(
            self.center_x - 4,
            self.center_y - 2,
            self.center_x + 4,
            self.center_y + 2,
            fill="#F39C12",
            outline="#E67E22",
            tags="ropa",
        )

        self._actualizar_ropa()

    def _actualizar_ropa(self):
        angle_rad = math.radians(self.angle)

        # Posicionar camiseta
        camiseta_points = []
        base_points = [(12, 8), (-12, 8), (-16, -4), (16, -4)]
        for dx, dy in base_points:
            x = self.center_x + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            y = self.center_y + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            camiseta_points.extend([x, y])
        self.coords(self.camiseta, camiseta_points)

        # Posicionar pantalón
        pantalon_points = []
        base_points_pantalon = [(8, 16), (-8, 16), (-6, -8), (6, -8)]
        for dx, dy in base_points_pantalon:
            x = (
                self.center_x
                + dx * math.cos(angle_rad + 0.5)
                - dy * math.sin(angle_rad + 0.5)
            )
            y = (
                self.center_y
                + dx * math.sin(angle_rad + 0.5)
                + dy * math.cos(angle_rad + 0.5)
            )
            pantalon_points.extend([x, y])
        self.coords(self.pantalon, pantalon_points)

        # Posicionar calcetín
        sock_x = self.center_x + 20 * math.cos(angle_rad + 1.0)
        sock_y = self.center_y + 20 * math.sin(angle_rad + 1.0)
        self.coords(self.calcetin, sock_x - 4, sock_y - 2, sock_x + 4, sock_y + 2)

    def girar(self, velocidad=1):
        if self.animating:
            self.angle = (self.angle + velocidad) % 360
            self._actualizar_ropa()
            self.after(50, lambda: self.girar(velocidad))

    def iniciar_lavado(self):
        self.animating = True
        self.girar(3)

    def iniciar_centrifugado(self):
        self.animating = True
        self.girar(10)

    def detener(self):
        self.animating = False
