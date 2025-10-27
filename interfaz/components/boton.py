import tkinter as tk  # Importa la librería para crear la interfaz gráfica


# Define la clase BotonNeumorphism, que hereda de tk.Button (es un botón normal, pero tuneado)
class BotonNeumorphism(tk.Button):
    # El constructor, se llama cuando creas un BotonNeumorphism
    def __init__(self, parent, text="INICIO", command=None):
        # Llama al constructor de tk.Button para crear el botón base
        super().__init__(
            parent,  # El 'padre' donde se dibujará (ventana o frame)
            text=text,  # El texto que mostrará el botón
            font=("Helvetica", 12, "bold"),  # Tipo de letra
            bg="#E0E5EC",  # Color de fondo (el grisáceo del neumorphism)
            fg="#27AE60",  # Color del texto (verde)
            relief="flat",  # Estilo del borde (plano, sin efecto 3D inicial)
            bd=2,  # Grosor del borde (aunque sea plano, se usa para el highlight)
            padx=25,  # Espacio extra a los lados del texto
            pady=12,  # Espacio extra arriba y abajo del texto
            command=command,  # La función que se ejecutará al hacer clic
        )

        # Configura las opciones de "highlight" para simular las sombras del neumorphism
        # Esto crea un borde doble con colores diferentes para dar el efecto de luz y sombra
        self.configure(
            highlightbackground="#A3B1C6",  # Color del borde exterior cuando NO tiene foco (sombra oscura)
            highlightcolor="#FFFFFF",  # Color del borde exterior cuando SÍ tiene foco (sombra clara/brillo)
            highlightthickness=2,  # Grosor de este borde exterior
        )
