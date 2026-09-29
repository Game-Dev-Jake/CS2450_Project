import tkinter as tk
from tkinter import ttk
from cpu import VCPU, format_word
from memory import VMemory
from register import VRegister

RED = "#ff0000"
GREEN = "#00FF00"

class Application(tk.Tk):
    def __init__(self, title: str, cpu: VCPU, memory: VMemory, accumulator: VRegister, width: int = 600, height: int = 600):
        super().__init__()

        self.title(title)
        self.geometry(f"{width}x{height}")

        self.cpu = cpu
        self.memory = memory
        self.accumulator = accumulator

        self.resizable(False,False)

        menubar = tk.Menu(self)
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="Load", command=self.on_file_load)
        self.file_menu.add_command(label="Reset Program", command=self.on_file_reset_program)
        self.file_menu.add_command(label="Logs", command=self.on_file_logs)
        self.file_menu.add_command(label="Exit", command=self.on_file_exit)
        menubar.add_cascade(label="File", menu=self.file_menu)
        self.configure(menu=menubar)

        self.memory_tree = ttk.Treeview(self, columns=("col1", "col2"), show="headings")
        self.memory_tree.heading("col1", text="Address")
        self.memory_tree.heading("col2", text="Value")
        self.memory_tree.column("col1", width=120,anchor="center")
        self.memory_tree.column("col2", width=120,anchor="center")
        self.memory_tree.place(x=330, y=20, width=240, height=560)

        self.memory_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.memory_tree.yview)
        self.memory_tree.configure(yscrollcommand=self.memory_scrollbar.set)
        self.memory_scrollbar.place(x=570, y=20, width=20, height=560)

        self.frame2 = tk.Frame(self, relief="groove", bd=2)
        self.frame2.place(x=40, y=26, width=260, height=250)

        self.button_run = tk.Button(self.frame2, text="Run", command=self.on_button_run)
        self.button_run.place(x=20, y=20, width=100, height=30)

        self.button_stop = tk.Button(self.frame2, text="Stop", command=self.on_button_stop)
        self.button_stop.place(x=140, y=20, width=100, height=32)

        self.button_step = tk.Button(self.frame2, text="Step", command=self.on_button_step)
        self.button_step.place(x=20, y=70, width=220, height=32)

        self.button_clear_memory = tk.Button(self.frame2, text="Clear Memory", command=self.on_button_clear_memory)
        self.button_clear_memory.place(x=20, y=120, width=220, height=32)

        self.button_clear_accumulator = tk.Button(self.frame2, text="Clear Accumulator", command=self.on_button_clear_accumulator)
        self.button_clear_accumulator.place(x=20, y=170, width=220, height=32)

        self.label_controls = tk.Label(self.frame2, text="Controls")
        self.label_controls.place(x=85, y=210, width=90, height=26)

        self.label_accumulator = tk.Label(self, text="Accumulator:")
        self.label_accumulator.place(x=60, y=289, width=130, height=26)

        self.label_accumulator_value = tk.Label(self, text="0000", font=("Helvetica", 10, "bold"), state="disabled")
        self.label_accumulator_value.place(x=170, y=289, width=90, height=26)

        self.label_status_indicator = tk.Label(self, text="Stopped", fg=RED)
        self.label_status_indicator.place(x=125, y=0, width=90, height=26)

        self.listbox_user_console = tk.Listbox(self)
        self.listbox_user_console.place(x=20, y=330, width=300, height=250)

        self.cpu.output_fn = self.log_to_console

        self.load_memory_tree()

    def log_to_console(self, message):
        self.listbox_user_console.insert("end", str(message))
        self.listbox_user_console.see("end")

    def on_button_run(self):
        self.cpu.run()

    def on_button_stop(self):
        pass

    def on_button_step(self):
        self.cpu.step()

    def on_button_clear_memory(self):
        self.memory.reset_memory()
        self.load_memory_tree()

    def on_button_clear_accumulator(self):
        pass

    def on_file_load(self):
        pass

    def on_file_reset_program(self):
        pass

    def on_file_logs(self):
        pass

    def on_file_exit(self):
        pass

    def load_memory_tree(self):
        self.memory_tree.delete(*self.memory_tree.get_children())
        for address in range(self.memory.register_count):
            value = self.memory.read(address)
            self.memory_tree.insert("", "end", values=(f"{address:02d}", format_word(value)))
