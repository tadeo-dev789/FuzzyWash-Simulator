import tkinter as tk
from tkinter import ttk
import math
import random
import time

try:
    from motor_difuso.fuzzificacion import (
        fuzzify_tipo_suciedad, 
        fuzzify_grado_suciedad, 
        fuzzify_cantidad_ropa
    )
    from motor_difuso.inferencia import motor_de_inferencia
    from motor_difuso.defuzzificacion import defuzzify_centroide
except ImportError:
    print("Error: No se encontraron los archivos del 'motor_difuso'.")
    def fuzzify_tipo_suciedad(v): return {'Media': 1.0}
    def fuzzify_grado_suciedad(v): return {'Media': 1.0}
    def fuzzify_cantidad_ropa(v): return {'Media': 1.0}
    def motor_de_inferencia(v): return {'Medio': 1.0}
    def defuzzify_centroide(v): return 45.7

class TamborLavadora(tk.Canvas):
    def __init__(self, parent, width=180, height=180):
        super().__init__(parent, width=width, height=height, bg="#E0E5EC", 
                        highlightthickness=0)
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
            self.center_x - self.radius - 8, self.center_y - self.radius - 8,
            self.center_x + self.radius + 8, self.center_y + self.radius + 8,
            fill="#A3B1C6", outline="#7F8C8D", width=2
        )
        
        # Tambor interior
        self.tambor_interior = self.create_oval(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            fill="#3498DB", outline="#2980B9", width=2
        )
        
        # Agujeros del tambor
        for i in range(0, 360, 30):
            rad = math.radians(i)
            x = self.center_x + (self.radius - 4) * math.cos(rad)
            y = self.center_y + (self.radius - 4) * math.sin(rad)
            self.create_oval(x-1.5, y-1.5, x+1.5, y+1.5, fill="#FFFFFF", outline="")
    
    def _crear_ropa(self):
        # Crear prendas de ropa dentro del tambor con puntos iniciales
        puntos_camiseta = [self.center_x, self.center_y] * 4
        self.camiseta = self.create_polygon(puntos_camiseta, fill="#E74C3C", outline="#C0392B", tags="ropa")
        
        puntos_pantalon = [self.center_x, self.center_y] * 4
        self.pantalon = self.create_polygon(puntos_pantalon, fill="#2C3E50", outline="#34495E", tags="ropa")
        
        self.calcetin = self.create_oval(self.center_x-4, self.center_y-2, 
                                       self.center_x+4, self.center_y+2, 
                                       fill="#F39C12", outline="#E67E22", tags="ropa")
        
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
            x = self.center_x + dx * math.cos(angle_rad + 0.5) - dy * math.sin(angle_rad + 0.5)
            y = self.center_y + dx * math.sin(angle_rad + 0.5) + dy * math.cos(angle_rad + 0.5)
            pantalon_points.extend([x, y])
        self.coords(self.pantalon, pantalon_points)
        
        # Posicionar calcetín
        sock_x = self.center_x + 20 * math.cos(angle_rad + 1.0)
        sock_y = self.center_y + 20 * math.sin(angle_rad + 1.0)
        self.coords(self.calcetin, sock_x-4, sock_y-2, sock_x+4, sock_y+2)
    
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

class AguaBurbujas(tk.Canvas):
    def __init__(self, parent, width=180, height=180):
        super().__init__(parent, width=width, height=width, bg="#E0E5EC", 
                        highlightthickness=0)
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
        self.create_rectangle(8, 180 - altura_agua, 172, 172,
                            fill="#A3B1C6", outline="#7F8C8D", width=2,
                            tags="contenedor")
        
        # Agua
        self.create_rectangle(12, 180 - altura_agua + 4, 168, 168,
                            fill="#3498DB", outline="#2980B9", width=1,
                            tags="agua")
        
        # Superficie del agua con efecto de onda
        for i in range(12, 168, 8):
            altura_onda = math.sin(i * 0.1 + time.time() * 2) * 2
            self.create_line(i, 180 - altura_agua + 4 + altura_onda, 
                           i + 8, 180 - altura_agua + 4 + altura_onda,
                           fill="#2980B9", width=2, tags="agua")
    
    def _crear_burbujas(self):
        for _ in range(8):
            self.crear_burbuja()
    
    def crear_burbuja(self):
        x = random.randint(20, 160)
        y = random.randint(80, 150)
        radio = random.randint(2, 5)
        velocidad = random.uniform(0.3, 1.2)
        
        burbuja = {
            'id': self.create_oval(x-radio, y-radio, x+radio, y+radio,
                                 fill="white", outline="#AED6F1", width=1,
                                 tags="burbuja"),
            'x': x, 'y': y, 'radio': radio, 'velocidad': velocidad
        }
        self.burbujas.append(burbuja)
    
    def animar_burbujas(self):
        if self.animando:
            for burbuja in self.burbujas:
                burbuja['y'] -= burbuja['velocidad']
                
                if burbuja['y'] < 40:
                    burbuja['y'] = 150
                    burbuja['x'] = random.randint(20, 160)
                
                self.coords(burbuja['id'],
                          burbuja['x'] - burbuja['radio'],
                          burbuja['y'] - burbuja['radio'],
                          burbuja['x'] + burbuja['radio'],
                          burbuja['y'] + burbuja['radio'])
            
            if random.random() < 0.3:
                self.crear_burbuja()
                
            if len(self.burbujas) > 12:
                burbuja_antigua = self.burbujas.pop(0)
                self.delete(burbuja_antigua['id'])
            
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
            self.delete(burbuja['id'])
        self.burbujas = []
        self._crear_burbujas()

class PerillaAreaIndicador(tk.Canvas):
    def __init__(self, parent, width=110, height=130, min_val=0, max_val=100, 
                 label_text="", command=None, initial_val=50):
        super().__init__(parent, width=width, height=height, 
                         bg="#E0E5EC", bd=0, highlightthickness=0)
        
        self.min_val = min_val
        self.max_val = max_val
        self.command = command
        self._value = initial_val
        
        self.bg_color = "#E0E5EC"
        self.shadow_dark = "#A3B1C6"
        self.shadow_light = "#FFFFFF"
        self.knob_color = "#E0E5EC"
        self.indicator_color = "#007AFF" 
        self.area_color = "#007AFF" 
        self.text_color = "#2C3E50"
        
        self.radius = 35
        self.center_x = width / 2
        self.center_y = height / 2 - 8
        
        self.start_angle = -135
        self.end_angle = 135
        
        self._create_neumorphism_base()
        self._create_label(label_text)
        
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        self.set_value(initial_val)

    def _create_neumorphism_base(self):
        self.create_oval(
            self.center_x - self.radius - 2, self.center_y - self.radius - 2,
            self.center_x + self.radius + 2, self.center_y + self.radius + 2,
            fill=self.shadow_dark, outline="", tags="shadow_dark"
        )
        
        self.create_oval(
            self.center_x - self.radius - 1, self.center_y - self.radius - 1,
            self.center_x + self.radius + 1, self.center_y + self.radius + 1,
            fill=self.shadow_light, outline="", tags="shadow_light"
        )
        
        self.knob_base = self.create_oval(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            fill=self.knob_color, outline="", tags="knob_base"
        )
        
        for angle in range(-135, 136, 45):
            rad = math.radians(angle)
            inner_x = self.center_x + (self.radius - 6) * math.cos(rad)
            inner_y = self.center_y + (self.radius - 6) * math.sin(rad)
            outer_x = self.center_x + (self.radius - 12) * math.cos(rad)
            outer_y = self.center_y + (self.radius - 12) * math.sin(rad)
            
            self.create_line(inner_x, inner_y, outer_x, outer_y, 
                           fill="#A3B1C6", width=2, tags="scale_marks")

    def _create_label(self, label_text):
        self.create_text(
            self.center_x, self.center_y + self.radius + 15, 
            text=label_text, font=("Helvetica", 9, "bold"), 
            fill=self.text_color, tags="label"
        )

    def _draw_area_indicator(self):
        self.delete("indicator")
        self.delete("value_text")
        
        val_ratio = (self._value - self.min_val) / (self.max_val - self.min_val)
        angle_deg = self.start_angle + (self.end_angle - self.start_angle) * val_ratio
        
        start_angle = -135 
        extent = angle_deg - start_angle
        
        if extent > 0:
            self.create_arc(
                self.center_x - self.radius + 4, self.center_y - self.radius + 4,
                self.center_x + self.radius - 4, self.center_y + self.radius - 4,
                start=start_angle, extent=extent,
                fill=self.area_color, outline="", width=0, style="arc", 
                tags="indicator"
            )
        
        self.value_text = self.create_text(
            self.center_x, self.center_y, 
            text=f"{int(self._value)}", 
            font=("Helvetica", 14, "bold"), 
            fill=self.indicator_color, 
            tags="value_text"
        )

    def _update_neumorphism_effect(self, pressed=False):
        if pressed:
            self.itemconfig("shadow_dark", fill=self.shadow_light)
            self.itemconfig("shadow_light", fill=self.shadow_dark)
            self.itemconfig("knob_base", fill=self.shadow_dark)
        else:
            self.itemconfig("shadow_dark", fill=self.shadow_dark)
            self.itemconfig("shadow_light", fill=self.shadow_light)
            self.itemconfig("knob_base", fill=self.knob_color)

    def _update_value_from_event(self, event):
        dx = event.x - self.center_x
        dy = event.y - self.center_y
        
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        
        if angle_deg < self.start_angle:
            angle_deg = self.start_angle
        elif angle_deg > self.end_angle:
            angle_deg = self.end_angle
            
        val_ratio = (angle_deg - self.start_angle) / (self.end_angle - self.start_angle)
        new_value = self.min_val + (self.max_val - self.min_val) * val_ratio
        
        self.set_value(new_value)
        return new_value

    def _on_press(self, event):
        self._update_neumorphism_effect(True)
        self._update_value_from_event(event)

    def _on_drag(self, event):
        self._update_value_from_event(event)

    def _on_release(self, event):
        self._update_neumorphism_effect(False)
        if self.command:
            self.command(self._value)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = max(self.min_val, min(self.max_val, value))
        self._draw_area_indicator()

class DisplayDigital(tk.Frame):
    def __init__(self, parent, width=300, height=100):
        super().__init__(parent, width=width, height=height, bg="#E0E5EC")
        self.pack_propagate(False)
        
        self.display_bg = "#0066CC" 
        self.display_fg = "#00FFFF" 
        
        self._create_display()

    def _create_display(self):
        label_frame = tk.Frame(self, bg="#E0E5EC")
        label_frame.pack(pady=(0, 3))
        
        tk.Label(
            label_frame,
            text="TIEMPO RESTANTE",
            font=("Helvetica", 11, "bold"),
            bg="#E0E5EC",
            fg="#2C3E50"
        ).pack()
        
        display_frame = tk.Frame(self, bg=self.display_bg, bd=3, relief="sunken")
        display_frame.pack(fill="both", expand=True, padx=8, pady=3)
        
        self.display_var = tk.StringVar(value="45:00")
        
        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Courier New", 36, "bold"),
            bg=self.display_bg,
            fg=self.display_fg
        )
        self.display_label.pack(expand=True, fill="both")

    def set_time(self, time_str):
        self.display_var.set(time_str)

class BotonNeumorphism(tk.Button):
    def __init__(self, parent, text="INICIO", command=None):
        super().__init__(parent, text=text, 
                         font=("Helvetica", 12, "bold"),
                         bg="#E0E5EC",
                         fg="#27AE60",
                         relief="flat",
                         bd=2,
                         padx=25,
                         pady=12,
                         command=command)
        
        self.configure(
            highlightbackground="#A3B1C6",
            highlightcolor="#FFFFFF",
            highlightthickness=2
        )

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
        
        self._create_panel()

    def _create_panel(self):
        self.panel_principal = tk.Frame(self.root, bg="#E0E5EC", bd=0)
        self.panel_principal.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título
        title_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        title_frame.pack(pady=5)
        
        tk.Label(title_frame, text="FUZZYWASH SIMULATOR",
                 font=("Helvetica", 20, "bold"), 
                 bg="#E0E5EC", fg="#2C3E50").pack()
        
        tk.Label(title_frame, text="Sistema Inteligente de Lavado", 
                 font=("Helvetica", 10), 
                 bg="#E0E5EC", fg="#7F8C8D").pack(pady=2)
        
        self._create_controles_superiores()
        self._create_seccion_media()
        self._create_animaciones_con_leds()  # Ahora las animaciones y LEDs van juntos

    def _create_controles_superiores(self):
        controles_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        controles_frame.pack(fill="x", padx=15, pady=15)
        
        # Perillas
        self.perilla_agua = PerillaAreaIndicador(controles_frame, 
                                               label_text="NIVEL AGUA", 
                                               command=self.calcular)
        self.perilla_agua.pack(side="left", padx=15)
        
        self.perilla_temp = PerillaAreaIndicador(controles_frame, 
                                               label_text="TEMPERATURA", 
                                               command=self.calcular)
        self.perilla_temp.pack(side="left", padx=15)
        
        self.perilla_suciedad = PerillaAreaIndicador(controles_frame, 
                                                   label_text="TIPO SUCIEDAD", 
                                                   command=self.calcular)
        self.perilla_suciedad.pack(side="left", padx=15)
        
        boton_container = tk.Frame(controles_frame, bg="#E0E5EC")
        boton_container.pack(side="right", padx=15)
        
        self.boton_inicio = BotonNeumorphism(boton_container, 
                                           text="INICIO", 
                                           command=self.toggle_inicio)
        self.boton_inicio.pack(pady=3)
        
        luz_frame = tk.Frame(boton_container, bg="#E0E5EC")
        luz_frame.pack()
        
        tk.Label(luz_frame, text="EN MARCHA", 
                 bg="#E0E5EC", font=("Helvetica", 7), fg="#7F8C8D").pack()
        
        self.luz_indicador = tk.Canvas(luz_frame, width=18, height=18, 
                                     bg="#E0E5EC", highlightthickness=0)
        self.luz_indicador.pack()
        self.luz_id = self.luz_indicador.create_oval(2, 2, 16, 16, 
                                                   fill="#E74C3C", outline="#A3B1C6", width=1)

    def _create_seccion_media(self):
        media_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        media_frame.pack(fill="x", padx=15, pady=8)
        
        display_container = tk.Frame(media_frame, bg="#E0E5EC")
        display_container.pack(pady=8)
        
        self.display = DisplayDigital(display_container, width=280, height=90)
        self.display.pack()

    def _create_animaciones_con_leds(self):
        # Frame principal para animaciones y LEDs
        animaciones_frame = tk.Frame(self.panel_principal, bg="#E0E5EC")
        animaciones_frame.pack(fill="x", padx=15, pady=10)
        
        # Contenedor para toda la fila (LEDs + Animaciones + LEDs)
        fila_container = tk.Frame(animaciones_frame, bg="#E0E5EC")
        fila_container.pack()
        
        # LEDs IZQUIERDOS (2 LEDs)
        leds_izquierdos_frame = tk.Frame(fila_container, bg="#E0E5EC")
        leds_izquierdos_frame.pack(side="left", padx=10)
        
        indicadores_izquierdos = [
            ("LAVADO", "#E0E5EC"),
            ("ENJUAGUE", "#E0E5EC")
        ]
        
        for i, (texto, color) in enumerate(indicadores_izquierdos):
            frame = tk.Frame(leds_izquierdos_frame, bg="#E0E5EC")
            frame.pack(pady=8)
            
            led_canvas = tk.Canvas(frame, width=40, height=40, bg="#E0E5EC", highlightthickness=0)
            led_canvas.pack(pady=2)
            
            led_canvas.create_oval(5, 5, 35, 35, fill="#A3B1C6", outline="")
            led_canvas.create_oval(3, 3, 33, 33, fill="#FFFFFF", outline="")
            led_id = led_canvas.create_oval(8, 8, 30, 30, fill="#E74C3C", outline="")
            
            tk.Label(frame, text=texto, bg="#E0E5EC", 
                     font=("Helvetica", 9, "bold"), fg="#2C3E50").pack()
            
            # Guardar en la lista de indicadores
            if not hasattr(self, 'indicadores'):
                self.indicadores = []
            self.indicadores.append({
                'canvas': led_canvas,
                'led_id': led_id,
                'text': texto,
                'activo': False
            })
        
        # ANIMACIONES (TAMBOR + AGUA) EN EL CENTRO
        animaciones_centro_frame = tk.Frame(fila_container, bg="#E0E5EC")
        animaciones_centro_frame.pack(side="left", padx=20)
        
        # Tambor giratorio
        tambor_frame = tk.Frame(animaciones_centro_frame, bg="#E0E5EC")
        tambor_frame.pack(side="left", padx=15, pady=5)
        
        tk.Label(tambor_frame, text="TAMBOR", bg="#E0E5EC", 
                font=("Helvetica", 9, "bold"), fg="#2C3E50").pack(pady=(0, 3))
        
        self.tambor = TamborLavadora(tambor_frame, width=180, height=180)
        self.tambor.pack()
        
        # Animación de agua y burbujas
        agua_frame = tk.Frame(animaciones_centro_frame, bg="#E0E5EC")
        agua_frame.pack(side="left", padx=15, pady=5)
        
        tk.Label(agua_frame, text="AGUA Y DETERGENTE", bg="#E0E5EC",
                font=("Helvetica", 9, "bold"), fg="#2C3E50").pack(pady=(0, 3))
        
        self.agua = AguaBurbujas(agua_frame, width=180, height=180)
        self.agua.pack()
        
        # LEDs DERECHOS (2 LEDs)
        leds_derechos_frame = tk.Frame(fila_container, bg="#E0E5EC")
        leds_derechos_frame.pack(side="left", padx=10)
        
        indicadores_derechos = [
            ("CENTRIFUGADO", "#E0E5EC"),
            ("FINALIZADO", "#E0E5EC")
        ]
        
        for i, (texto, color) in enumerate(indicadores_derechos):
            frame = tk.Frame(leds_derechos_frame, bg="#E0E5EC")
            frame.pack(pady=8)
            
            led_canvas = tk.Canvas(frame, width=40, height=40, bg="#E0E5EC", highlightthickness=0)
            led_canvas.pack(pady=2)
            
            led_canvas.create_oval(5, 5, 35, 35, fill="#A3B1C6", outline="")
            led_canvas.create_oval(3, 3, 33, 33, fill="#FFFFFF", outline="")
            led_id = led_canvas.create_oval(8, 8, 30, 30, fill="#E74C3C", outline="")
            
            tk.Label(frame, text=texto, bg="#E0E5EC", 
                     font=("Helvetica", 9, "bold"), fg="#2C3E50").pack()
            
            # Guardar en la lista de indicadores
            self.indicadores.append({
                'canvas': led_canvas,
                'led_id': led_id,
                'text': texto,
                'activo': False
            })

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
        self.agua.set_nivel_agua(self.perilla_agua.get_value())
        self._actualizar_indicadores_fase()

    def _detener_animaciones(self):
        self.tambor.detener()
        self.agua.detener_animacion()

    def _actualizar_indicadores_fase(self):
        tiempo_restante = self.total_time - self.current_time
        
        for indicador in self.indicadores:
            indicador['canvas'].itemconfig(indicador['led_id'], fill="#E74C3C")
            indicador['activo'] = False
        
        if tiempo_restante > self.total_time * 0.6:
            # LAVADO (LED 0)
            self.indicadores[0]['canvas'].itemconfig(self.indicadores[0]['led_id'], fill="#27AE60")
            self.indicadores[0]['activo'] = True
            self.modo_centrifugado = False
            
        elif tiempo_restante > self.total_time * 0.3:
            # ENJUAGUE (LED 1)
            self.indicadores[1]['canvas'].itemconfig(self.indicadores[1]['led_id'], fill="#27AE60")
            self.indicadores[1]['activo'] = True
            self.modo_centrifugado = False
            
        elif tiempo_restante > 0:
            # CENTRIFUGADO (LED 2)
            self.indicadores[2]['canvas'].itemconfig(self.indicadores[2]['led_id'], fill="#27AE60")
            self.indicadores[2]['activo'] = True
            self.modo_centrifugado = True
            if self.running:
                self.tambor.detener()
                self.tambor.iniciar_centrifugado()
        else:
            # FINALIZADO (LED 3)
            self.indicadores[3]['canvas'].itemconfig(self.indicadores[3]['led_id'], fill="#27AE60")
            self.indicadores[3]['activo'] = True

    def _iniciar_conteo(self):
        if self.running and self.current_time < self.total_time:
            self.current_time += 1/60
            tiempo_restante = max(0, self.total_time - self.current_time)
            
            tiempo_formateado = self._formatear_tiempo(tiempo_restante)
            self.display.set_time(tiempo_formateado)
            
            self._actualizar_indicadores_fase()
            
            self.root.after(1000, self._iniciar_conteo)
        elif self.current_time >= self.total_time and self.running:
            self._ciclo_completado()

    def _ciclo_completado(self):
        self.running = False
        self.boton_inicio.config(text="INICIO", fg="#27AE60")
        self.luz_indicador.itemconfig(self.luz_id, fill="#E74C3C")
        self.display.set_time("00:00")
        self.current_time = 0.0
        self._detener_animaciones()
        self._actualizar_indicadores_fase()
        self.display.set_time("¡LISTO!")

    def calcular(self, event=None):
        val_tipo = self.perilla_suciedad.get_value()
        val_grado = self.perilla_agua.get_value() 
        val_cantidad = self.perilla_temp.get_value()

        fuzz_tipo = fuzzify_tipo_suciedad(val_tipo)
        fuzz_grado = fuzzify_grado_suciedad(val_grado)
        fuzz_cantidad = fuzzify_cantidad_ropa(val_cantidad)
        
        valores_fuzzificados = {'tipo': fuzz_tipo, 'grado': fuzz_grado, 'cantidad': fuzz_cantidad}
        
        activacion_salidas = motor_de_inferencia(valores_fuzzificados)
        
        tiempo_final = defuzzify_centroide(activacion_salidas)

        self.total_time = tiempo_final
        self.current_time = 0.0
        
        if not self.running:
            tiempo_formateado = self._formatear_tiempo(tiempo_final)
            self.display.set_time(tiempo_formateado)
        
        self.agua.set_nivel_agua(self.perilla_agua.get_value())

def iniciar_app():
    root = tk.Tk()
    app = FuzzyWashSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_app()