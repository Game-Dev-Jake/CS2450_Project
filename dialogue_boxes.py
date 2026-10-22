import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

class DialogueTheme(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("Theme")
        self.geometry("270x155")
        self.resizable(False,False)
        self.transient(app)

        self.label_primary_color = tk.Label(self, text="Primary Color")
        self.label_primary_color.place(x=10, y=20, width=120, height=30)

        self.frame_primary_color = tk.Frame(self, bg=self.app.colors["primary"])
        self.frame_primary_color.place(x=125,y=25, width=20, height=20)

        self.button_set_primary_color = tk.Button(self, text="Select", command=self.on_button_set_primary_color)
        self.button_set_primary_color.place(x=150, y=20, width=96, height=32)

        self.frame_secondary_color = tk.Frame(self, bg=self.app.colors["secondary"])
        self.frame_secondary_color.place(x=125,y=65, width=20, height=20)

        self.label_secondary_color = tk.Label(self, text="Secondary Color")
        self.label_secondary_color.place(x=20, y=60, width=100, height=30)

        self.button_set_secondary_color = tk.Button(self, text="Select", command=self.on_button_set_secondary_color)
        self.button_set_secondary_color.place(x=150, y=60, width=96, height=32)

        self.button_save_theme = tk.Button(self, text="Save", command=self.on_button_save_theme)
        self.button_save_theme.place(x=10, y=110, width=80, height=25)

        self.button_reset_theme = tk.Button(self, text="Reset", command=self.on_button_reset_theme)
        self.button_reset_theme.place(x=95, y=110, width=80, height=25)

        self.button_ok_theme = tk.Button(self, text="Ok", command=self.destroy)
        self.button_ok_theme.place(x=180, y=110, width=80, height=25)

    def on_button_set_primary_color(self):
        color_info = colorchooser.askcolor(title="Select a primary color", color=self.app.colors["primary"])
        if color_info[1]:
            self.app.colors["primary"] = color_info[1]
            self.app.apply_theme()
            self.apply_theme()

    def on_button_set_secondary_color(self):
        color_info = colorchooser.askcolor(title="Select a secondary color", color=self.app.colors["secondary"])
        if color_info[1]:
            self.app.colors["secondary"] = color_info[1]
            self.app.apply_theme()
            self.apply_theme()

    def on_button_save_theme(self):
        self.app.loader.save_json_value(["theme", "colors", "primary"],self.app.colors["primary"])
        self.app.loader.save_json_value(["theme", "colors", "secondary"],self.app.colors["secondary"])

    def on_button_reset_theme(self):
        self.app.load_theme()
        self.app.apply_theme()
        self.apply_theme()

    def apply_theme(self):
        self.frame_primary_color.config(bg=self.app.colors["primary"])
        self.frame_secondary_color.config(bg=self.app.colors["secondary"])