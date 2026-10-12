import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

class DialogueTheme(tk.Toplevel):
    def __init__(self, app):
        super.__init__(self, app)
        self.app = app
        self.title("Theme")
        self.geometry("250x120")
        self.resizable(False,False)
        self.transient(app.root)

        self.label_primary_color = tk.Label(self, text="Primary Color")
        self.label_primary_color.place(x=10, y=20, width=120, height=30)

        self.button_set_primary_color = tk.Button(self, text="Select", command=self.on_button_set_primary_color)
        self.button_set_primary_color.place(x=130, y=18, width=96, height=32)

        self.label_secondary_color = tk.Label(self, text="Secondary Color")
        self.label_secondary_color.place(x=20, y=60, width=100, height=30)

        self.button_set_secondary_color = tk.Button(self, text="Select", command=self.on_button_set_secondary_color)
        self.button_set_secondary_color.place(x=130, y=60, width=96, height=32)

    def on_button_set_primary_color(self):
        pass

    def on_button_set_secondary_color(self):
        pass