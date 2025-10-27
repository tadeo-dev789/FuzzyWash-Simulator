import tkinter as tk


class BotonNeumorphism(tk.Button):
    def __init__(self, parent, text="INICIO", command=None):
        super().__init__(
            parent,
            text=text,
            font=("Helvetica", 12, "bold"),
            bg="#E0E5EC",
            fg="#27AE60",
            relief="flat",
            bd=2,
            padx=25,
            pady=12,
            command=command,
        )

        self.configure(
            highlightbackground="#A3B1C6",
            highlightcolor="#FFFFFF",
            highlightthickness=2,
        )
