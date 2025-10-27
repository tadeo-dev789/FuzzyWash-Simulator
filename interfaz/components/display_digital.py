import tkinter as tk


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
            fg="#2C3E50",
        ).pack()

        display_frame = tk.Frame(self, bg=self.display_bg, bd=3, relief="sunken")
        display_frame.pack(fill="both", expand=True, padx=8, pady=3)

        self.display_var = tk.StringVar(value="50:19")

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Courier New", 36, "bold"),
            bg=self.display_bg,
            fg=self.display_fg,
        )
        self.display_label.pack(expand=True, fill="both")

    def set_time(self, time_str):
        self.display_var.set(time_str)
