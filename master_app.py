import tkinter as tk
from tkinter import ttk
from application import Application

class MasterApp():
    def __init__(self):
        root = tk.Tk()
        root.geometry('600x600')
        root.title('UVSim')

        self.main_notebook = ttk.Notebook(root)
        self.main_notebook.pack(pady=10,expand=True)

        self.new_tab()

    def new_tab(self, title:str = "Default"):
        new_frame = ttk.Frame(self.main_notebook,width=600,height=600)
        new_frame.pack(fill='both',expand=True)

        self.main_notebook.add(new_frame, text=title)