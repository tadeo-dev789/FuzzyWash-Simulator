import tkinter as tk
from tkinter import ttk

from motor_difuso.fuzzificacion import fuzzify_tipo_suciedad, fuzzify_grado_suciedad, fuzzify_cantidad_ropa
from motor_difuso.inferencia import motor_de_inferencia
from motor_difuso.defuzzificacion import defuzzify_centroide

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Difuso")
        self.root.geometry("450x350")

        # --- Contenedor Principal ---
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill='both')

        # --- Crear los 3 Sliders ---
        self.crear_slider(main_frame, "Tipo de Suciedad", "tipo_suciedad")
        self.crear_slider(main_frame, "Grado de Suciedad", "grado_suciedad")
        self.crear_slider(main_frame, "Cantidad de Ropa", "cantidad_ropa")
        
        # --- Botón y Resultado ---
        self.calcular_btn = ttk.Button(main_frame, text="Calcular Tiempo", command=self.calcular, style='Accent.TButton')
        self.calcular_btn.pack(pady=20)
        
        self.resultado_label = ttk.Label(main_frame, text="Tiempo de Lavado: -- min", font=("Arial", 16, "bold"))
        self.resultado_label.pack()

        # Configurar estilo para el botón
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 12, 'bold'))

    def crear_slider(self, parent, texto, nombre_var):
        """Función para crear un slider con su título y valor."""
        
        # Frame para el título
        frame_titulo = ttk.Frame(parent)
        frame_titulo.pack(pady=(10,0), fill='x')
        ttk.Label(frame_titulo, text=texto, font=("Arial", 11)).pack(side='left')

        # Frame para el slider y el número
        frame_control = ttk.Frame(parent)
        frame_control.pack(fill='x', padx=10)
        
        # Etiqueta para mostrar el valor numérico
        valor_label = ttk.Label(frame_control, text="0.0", font=("Arial", 10, "bold"), width=5)
        valor_label.pack(side='right', padx=(10,0))

        # El widget Slider (Scale)
        slider = ttk.Scale(
            frame_control, 
            from_=0, 
            to=100, 
            orient='horizontal',
            command=lambda val: valor_label.config(text=f"{float(val):.1f}")
        )
        slider.pack(side='left', expand=True, fill='x')

        # Guardamos la referencia al slider y a la etiqueta
        setattr(self, f"slider_{nombre_var}", slider)
        setattr(self, f"label_{nombre_var}", valor_label)

    def calcular(self):
        """
        Esta función es el 'centro de mando'.
        ¡Observa que la lógica aquí es IDÉNTICA a la versión con Knobs!
        """
        # 1. Leer Sliders
        val_tipo = self.slider_tipo_suciedad.get()
        val_grado = self.slider_grado_suciedad.get()
        val_cantidad = self.slider_cantidad_ropa.get()

        # 2. Fuzzificar
        fuzz_tipo = fuzzify_tipo_suciedad(val_tipo)
        fuzz_grado = fuzzify_grado_suciedad(val_grado)
        fuzz_cantidad = fuzzify_cantidad_ropa(val_cantidad)
        
        valores_fuzzificados = {'tipo': fuzz_tipo, 'grado': fuzz_grado, 'cantidad': fuzz_cantidad}
        
        # 3. Inferir
        activacion_salidas = motor_de_inferencia(valores_fuzzificados)
        
        # 4. Defuzzificar
        tiempo_final = defuzzify_centroide(activacion_salidas)

        # 5. Mostrar Resultado
        self.resultado_label.config(text=f"Tiempo de Lavado: {tiempo_final:.2f} min")

def iniciar_app():
    root = tk.Tk()
    app = App(root)
    
    valor_inicial = 50
    
    # 1. Poner los sliders en el valor inicial
    app.slider_tipo_suciedad.set(valor_inicial)
    app.slider_grado_suciedad.set(valor_inicial)
    app.slider_cantidad_ropa.set(valor_inicial)
    
    # 2. Actualizar las etiquetas de texto manualmente
    app.label_tipo_suciedad.config(text=f"{valor_inicial:.1f}")
    app.label_grado_suciedad.config(text=f"{valor_inicial:.1f}")
    app.label_cantidad_ropa.config(text=f"{valor_inicial:.1f}")
    
    # 3. Hacer el primer cálculo al iniciar
    app.calcular()
    
    root.mainloop()
