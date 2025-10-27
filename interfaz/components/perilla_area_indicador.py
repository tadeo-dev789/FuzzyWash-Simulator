import tkinter as tk
import math


class PerillaAreaIndicador(tk.Canvas):
    def __init__(
        self,
        parent,
        width=110,
        height=130,
        min_val=0,
        max_val=100,
        label_text="",
        command=None,
        initial_val=50,
    ):
        super().__init__(
            parent, width=width, height=height, bg="#E0E5EC", bd=0, highlightthickness=0
        )

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
            self.center_x - self.radius - 2,
            self.center_y - self.radius - 2,
            self.center_x + self.radius + 2,
            self.center_y + self.radius + 2,
            fill=self.shadow_dark,
            outline="",
            tags="shadow_dark",
        )

        self.create_oval(
            self.center_x - self.radius - 1,
            self.center_y - self.radius - 1,
            self.center_x + self.radius + 1,
            self.center_y + self.radius + 1,
            fill=self.shadow_light,
            outline="",
            tags="shadow_light",
        )

        self.knob_base = self.create_oval(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            fill=self.knob_color,
            outline="",
            tags="knob_base",
        )

        for angle in range(-135, 136, 45):
            rad = math.radians(angle)
            inner_x = self.center_x + (self.radius - 6) * math.cos(rad)
            inner_y = self.center_y + (self.radius - 6) * math.sin(rad)
            outer_x = self.center_x + (self.radius - 12) * math.cos(rad)
            outer_y = self.center_y + (self.radius - 12) * math.sin(rad)

            self.create_line(
                inner_x,
                inner_y,
                outer_x,
                outer_y,
                fill="#A3B1C6",
                width=2,
                tags="scale_marks",
            )

    def _create_label(self, label_text):
        self.create_text(
            self.center_x,
            self.center_y + self.radius + 15,
            text=label_text,
            font=("Helvetica", 9, "bold"),
            fill=self.text_color,
            tags="label",
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
                self.center_x - self.radius + 4,
                self.center_y - self.radius + 4,
                self.center_x + self.radius - 4,
                self.center_y + self.radius - 4,
                start=start_angle,
                extent=extent,
                fill=self.area_color,
                outline="",
                width=0,
                style="arc",
                tags="indicator",
            )

        self.value_text = self.create_text(
            self.center_x,
            self.center_y,
            text=f"{int(self._value)}",
            font=("Helvetica", 14, "bold"),
            fill=self.indicator_color,
            tags="value_text",
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
