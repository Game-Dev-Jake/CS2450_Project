import tkinter as tk

class Application(tk.Tk):
    def __init__(self, title: str,height: int = 500, width: int = 400):
        super().__init__()

        self.title(title)
        self.geometry(f"{height}x{width}")