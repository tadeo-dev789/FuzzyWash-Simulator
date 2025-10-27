import tkinter as tk  # Importa la librería para crear la interfaz gráfica


# Define la clase DisplayDigital, que hereda de tk.Frame (un contenedor rectangular)
class DisplayDigital(tk.Frame):
    # El constructor, se llama cuando creas un DisplayDigital
    def __init__(self, parent, width=300, height=100):
        # Llama al constructor de tk.Frame para configurar el contenedor base
        super().__init__(parent, width=width, height=height, bg="#E0E5EC")
        # Evita que el frame cambie de tamaño automáticamente para ajustarse a su contenido
        self.pack_propagate(False)

        # Define los colores para el display (fondo azul oscuro, texto cian brillante)
        self.display_bg = "#0066CC"  # Fondo del display
        self.display_fg = "#00FFFF"  # Color del texto (números/mensaje)

        # Llama al método interno para dibujar los elementos del display
        self._create_display()

    # Método interno para crear los elementos visuales del display
    def _create_display(self):
        # Crea un frame (contenedor) para la etiqueta superior "TIEMPO RESTANTE"
        label_frame = tk.Frame(self, bg="#E0E5EC")
        label_frame.pack(pady=(0, 3))  # Lo coloca arriba con un pequeño espacio abajo

        # Crea la etiqueta de texto "TIEMPO RESTANTE"
        tk.Label(
            label_frame,
            text="TIEMPO RESTANTE",
            font=("Helvetica", 11, "bold"),  # Tipo de letra
            bg="#E0E5EC",  # Color de fondo
            fg="#2C3E50",  # Color de texto
        ).pack()  # Lo coloca dentro del label_frame

        # Crea el frame principal del display (el rectángulo azul hundido)
        display_frame = tk.Frame(
            self, bg=self.display_bg, bd=3, relief="sunken"
        )  # bd=borde, relief=efecto hundido
        display_frame.pack(
            fill="both", expand=True, padx=8, pady=3
        )  # Lo coloca ocupando el espacio restante

        # Crea una variable especial de Tkinter para guardar el texto que se mostrará
        # Esto permite actualizar el texto fácilmente más tarde
        self.display_var = tk.StringVar(
            value="50:19"
        )  # Inicializa con un valor de ejemplo

        # Crea la etiqueta (Label) que mostrará el tiempo (los números)
        self.display_label = tk.Label(
            display_frame,  # Se coloca dentro del frame azul
            textvariable=self.display_var,  # Asocia el texto de esta etiqueta a la variable display_var
            font=("Courier New", 36, "bold"),  # Tipo de letra (estilo digital)
            bg=self.display_bg,  # Color de fondo (el mismo azul)
            fg=self.display_fg,  # Color del texto (cian)
        )
        # Coloca la etiqueta dentro del display_frame, haciendo que ocupe todo el espacio
        self.display_label.pack(expand=True, fill="both")

    # Método público para cambiar el texto que se muestra en el display
    def set_time(self, time_str):
        # Actualiza el valor de la variable display_var
        # Tkinter automáticamente redibuja la etiqueta display_label para mostrar el nuevo texto
        self.display_var.set(time_str)
