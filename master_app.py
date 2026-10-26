import tkinter as tk
from tkinter import ttk
from cpu import VCPU, VRegister, VMemory
from load_handler import LoadHandler
from save_handler import SaveHandler
from application import Application
from edit_dialogue import EditDialogue
from config import Config
import dialogue_boxes as dialogues

CONFIG_FILE = "config.json"

class MasterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x640')
        self.title('UVSim')

        self.colors = {
            "primary": "",
            "secondary": ""
        }

        self.themed: list[tuple[tk.Widget, dict[str, str]]] = []

        self.resizable(False,False)

        self.main_notebook = ttk.Notebook(self)
        self.main_notebook.pack(fill='both',expand=True)

        menubar = tk.Menu(self)
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="Load", command=self.on_file_load)
        self.file_menu.add_command(label="Reset Program", command=self.on_file_reset_program)
        self.file_menu.add_command(label="Save", command=self.on_file_save)
        self.file_menu.add_command(label="Save As", command=self.on_file_save_as)
        self.file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(menubar,tearoff=0)
        self.edit_menu.add_command(label="Edit", command=self.on_file_edit)
        self.edit_menu.add_command(label="New Tab", command=self.new_tab)
        menubar.add_cascade(label="Edit", menu=self.edit_menu)

        self.window_menu = tk.Menu(menubar, tearoff=0)
        self.window_menu.add_command(label="Theme", command=self.on_window_theme)
        self.window_menu.add_command(label="Logs", command=self.on_file_logs)
        menubar.add_cascade(label="Window", menu=self.window_menu)

        self.configure(menu=menubar)

        self.load_theme()

        self.new_tab()

        self.mainloop()


    def load_theme(self):
        config = Config.load_file(CONFIG_FILE)
        if config:
            self.colors["primary"] = config.theme.colors.primary
            self.colors["secondary"] = config.theme.colors.secondary


    def themed_widget(self, widget, **roles):
        if (widget, roles) not in self.themed:
            self.themed.append((widget,roles))

    
    def apply_theme(self):
        self.themed = [(w, r) for w, r in self.themed if w.winfo_exists()]

        for widget, roles in self.themed:
            widget.config(**{opt: self.colors[role] for opt, role in roles.items()})


    def new_tab(self, title:str = "UVSim"):
        loader = LoadHandler()
        save_handler = SaveHandler()
        logs: list[str] = []
        memory_count: int = 250
        main_mem: VMemory = VMemory(logs,memory_count)
        accumulator: VRegister = VRegister(0)
        cpu: VCPU = VCPU(accumulator,main_mem,logs)
        app = Application(self.main_notebook,loader,save_handler,cpu,main_mem,accumulator,logs,self.themed_widget)
        self.themed_widget(app, bg="primary")

        self.main_notebook.add(app, text=title)
        self.main_notebook.select(app)
        self.apply_theme()

    def current_app(self) -> Application:
        try:
            return self.nametowidget(self.main_notebook.select())
        except:
            return None

    def on_file_load(self):
        try:
            self.current_app().on_file_load()
            self.main_notebook.tab("current",text=self.current_app().current_file_path.name)
        except:
            pass

    def on_file_edit(self):
        EditDialogue(self,self.current_app())

    def on_file_reset_program(self):
        self.current_app().on_file_reset_program()

    def on_file_save(self):
        self.current_app().on_file_save()

    def on_file_save_as(self):
        self.current_app().on_file_save_as()
        self.main_notebook.tab("current",text=self.current_app().current_file_path.name)

    def on_window_theme(self):
        dialogues.DialogueTheme(self)

    def on_file_logs(self):
        self.current_app().on_file_logs()