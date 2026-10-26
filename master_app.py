import tkinter as tk
from tkinter import ttk
from cpu import VCPU, VRegister, VMemory
from load_handler import LoadHandler
from save_handler import SaveHandler
from application import Application

class MasterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x640')
        self.title('UVSim')

        self.resizable(False,False)

        menubar = tk.Menu(self)
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="Load", command=self.on_file_load)
        self.file_menu.add_command(label="Edit", command=self.on_file_edit)
        self.file_menu.add_command(label="Reset Program", command=self.on_file_reset_program)
        self.file_menu.add_command(label="Save", command=self.on_file_save)
        self.file_menu.add_command(label="Save As", command=self.on_file_save_as)
        self.file_menu.add_command(label="Exit", command=self.on_file_exit)
        menubar.add_cascade(label="File", menu=self.file_menu)

        self.main_notebook = ttk.Notebook(self)
        self.main_notebook.pack(fill='both',expand=True)

        self.window_menu = tk.Menu(menubar, tearoff=0)
        self.window_menu.add_command(label="Theme", command=self.on_window_theme)
        self.window_menu.add_command(label="Logs", command=self.on_file_logs)
        menubar.add_cascade(label="Window", menu=self.window_menu)

        self.configure(menu=menubar)

        self.new_tab()
        self.new_tab()

        self.mainloop()

    def new_tab(self, title:str = "UVSim"):
        loader = LoadHandler()
        save_handler = SaveHandler()
        logs: list[str] = []
        memory_count: int = 250
        main_mem: VMemory = VMemory(logs,memory_count)
        accumulator: VRegister = VRegister(0)
        cpu: VCPU = VCPU(accumulator,main_mem,logs)
        app = Application(self.main_notebook,loader,save_handler,cpu,main_mem,accumulator,logs)

        self.main_notebook.add(app, text=title)

    def current_app(self) -> Application:
        return self.nametowidget(self.main_notebook.select())

    def on_file_load(self):
        self.current_app().on_file_load()

    def on_file_edit(self):
        self.current_app().on_file_edit()

    def on_file_reset_program(self):
        self.current_app().on_file_reset_program()

    def on_file_save(self):
        self.current_app().on_file_save()

    def on_file_save_as(self):
        self.current_app().on_file_save_as()

    def on_file_exit(self):
        self.current_app().on_file_exit()

    def on_window_theme(self):
        self.current_app().on_window_theme()

    def on_file_logs(self):
        self.current_app().on_file_logs()