import tkinter as tk  # La librería para dibujar ventanas y formas
import math  # Para hacer los cálculos de giros (senos y cosenos, ¡qué pro!)


class TamborLavadora(
    tk.Canvas
):  # Hereda de tk.Canvas, o sea, es un "lienzo" para dibujar
    def __init__(self, parent, width=180, height=180):
        # El constructor: se ejecuta cuando creas un TamborLavadora
        # Llama al constructor del "lienzo" (tk.Canvas) para configurarlo
        super().__init__(
            parent, width=width, height=height, bg="#E0E5EC", highlightthickness=0
        )
        # Calcula el mero centro del lienzo
        self.center_x = width // 2
        self.center_y = height // 2
        # Define qué tan grande será el tambor interno
        self.radius = 50
        # Guarda el ángulo actual de giro (empieza en 0 grados)
        self.angle = 0
        # Bandera para saber si la animación está activa o no (empieza apagada)
        self.animating = False

        # Llama a las funciones para dibujar el tambor y la ropa
        self._crear_tambor()
        self._crear_ropa()

    def _crear_tambor(self):
        # Dibuja las partes fijas del tambor
        # 1. El óvalo de afuera (como el cristal de la lavadora)
        self.create_oval(
            self.center_x - self.radius - 8,
            self.center_y - self.radius - 8,
            self.center_x + self.radius + 8,
            self.center_y + self.radius + 8,
            fill="#A3B1C6",
            outline="#7F8C8D",
            width=2,
        )
        # 2. El óvalo de adentro (el tambor metálico que gira)
        self.tambor_interior = self.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            fill="#3498DB",
            outline="#2980B9",
            width=2,
        )
        # 3. Los agujeritos del tambor (decoración)
        #    Usa matemáticas (coseno y seno) para ponerlos en círculo
        for i in range(0, 360, 30):  # Un agujero cada 30 grados
            rad = math.radians(i)  # Convierte grados a radianes
            # Calcula la posición (x, y) en el borde del círculo
            x = self.center_x + (self.radius - 4) * math.cos(rad)
            y = self.center_y + (self.radius - 4) * math.sin(rad)
            # Dibuja un circulito blanco pequeño
            self.create_oval(
                x - 1.5, y - 1.5, x + 1.5, y + 1.5, fill="#FFFFFF", outline=""
            )

    def _crear_ropa(self):
        # Dibuja las "prendas" de ropa (formas simples)
        # Las crea en el centro al principio, luego _actualizar_ropa las mueve
        puntos_camiseta = [self.center_x, self.center_y] * 4  # Lista inicial de puntos
        self.camiseta = self.create_polygon(  # Dibuja un polígono (simulando camiseta)
            puntos_camiseta, fill="#E74C3C", outline="#C0392B", tags="ropa"
        )
        puntos_pantalon = [self.center_x, self.center_y] * 4
        self.pantalon = self.create_polygon(  # Otro polígono (simulando pantalón)
            puntos_pantalon, fill="#2C3E50", outline="#34495E", tags="ropa"
        )
        self.calcetin = self.create_oval(  # Un óvalo (simulando calcetín)
            self.center_x - 4,
            self.center_y - 2,
            self.center_x + 4,
            self.center_y + 2,
            fill="#F39C12",
            outline="#E67E22",
            tags="ropa",
        )
        # Llama a la función para poner la ropa en su posición inicial según el ángulo 0
        self._actualizar_ropa()

    def _actualizar_ropa(self):
        # La magia matemática para mover la ropa como si estuviera girando
        angle_rad = math.radians(self.angle)  # El ángulo actual en radianes

        # --- Mover la camiseta ---
        camiseta_points = []
        # Puntos base de la forma de la camiseta (coordenadas relativas al centro)
        base_points = [(12, 8), (-12, 8), (-16, -4), (16, -4)]
        # Aplica la fórmula de rotación a cada punto base
        for dx, dy in base_points:
            # Nueva X = x*cos(angulo) - y*sin(angulo) + centroX
            x = self.center_x + dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            # Nueva Y = x*sin(angulo) + y*cos(angulo) + centroY
            y = self.center_y + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            camiseta_points.extend([x, y])  # Añade las coordenadas X, Y a la lista
        self.coords(
            self.camiseta, camiseta_points
        )  # Actualiza la posición del polígono

        # --- Mover el pantalón (similar, pero con un ligero desfase de ángulo) ---
        pantalon_points = []
        base_points_pantalon = [(8, 16), (-8, 16), (-6, -8), (6, -8)]
        for dx, dy in base_points_pantalon:
            # Usamos angle_rad + 0.5 para que no gire exactamente igual que la camiseta
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

        # --- Mover el calcetín (más simple, solo movemos su centro) ---
        # Usamos angle_rad + 1.0 para otro desfase
        sock_x = self.center_x + 20 * math.cos(angle_rad + 1.0)
        sock_y = self.center_y + 20 * math.sin(angle_rad + 1.0)
        # Actualizamos las coordenadas de las esquinas del óvalo
        self.coords(self.calcetin, sock_x - 4, sock_y - 2, sock_x + 4, sock_y + 2)

    def girar(self, velocidad=1):
        # La función que hace la animación cuadro por cuadro (recursiva)
        if self.animating:  # Solo si la bandera 'animating' está encendida
            # Aumenta el ángulo según la velocidad (y usa % 360 para que vuelva a 0 después de 360)
            self.angle = (self.angle + velocidad) % 360
            # Llama a la función que redibuja la ropa en la nueva posición
            self._actualizar_ropa()
            # Le dice a Tkinter: "Oye, en 50 milisegundos, vuelve a llamar a esta misma función 'girar'"
            # Esto crea el efecto de movimiento continuo
            self.after(50, lambda: self.girar(velocidad))

    # --- Métodos Públicos para Controlar la Animación ---
    def iniciar_lavado(self):
        # Prende la bandera de animación y empieza a girar lento (velocidad 3)
        self.animating = True
        self.girar(3)

    def iniciar_centrifugado(self):
        # Prende la bandera de animación y empieza a girar rápido (velocidad 10)
        self.animating = True
        self.girar(10)

    def is_spinning_fast(self):  # Helper function to check spin mode
        # You might need to track speed explicitly if mixing speeds becomes complex
        # For now, assumes if animating and not explicitly stopped/slowed, it could be fast
        # A better way would be to store the current speed: self.current_speed = 10
        return self.animating  # A simple approximation for now

    def detener(self):
        # Apaga la bandera de animación, lo que detiene el bucle en 'girar'
        self.animating = False
