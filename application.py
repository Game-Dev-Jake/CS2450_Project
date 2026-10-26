import tkinter as tk
import dialogue_boxes as dialogues
from tkinter import ttk, filedialog, simpledialog, scrolledtext
from cpu import VCPU, format_word
from load_handler import LoadHandler
from memory import VMemory
from register import VRegister
from load_handler import LoadHandler
from pathlib import Path
from edit_dialogue import EditDialogue
from save_handler import SaveHandler
from config import Config

RED = "#ff0000"
GREEN = "#00FF00"

class Application(tk.Frame):
    def __init__(self, parent, loader: LoadHandler, saver: SaveHandler, cpu: VCPU, memory: VMemory, accumulator: VRegister, logs: list[str], themed_widget: callable, width: int = 600, height: int = 600):
        super().__init__(parent, width=width, height=height)

        self.save_handler = saver
        self.current_file_path: Path = None

        self.colors = {
            "primary": "",
            "secondary": ""
        }

        self.loader = loader
        
        self.logs = logs

        self._current_highlight_iid = None
        

        self.cpu = cpu
        self.memory = memory
        self.accumulator = accumulator

        self.cpu.add_current_observer(self.on_current_changed)
        self.cpu.add_read_observer(self.on_read_prompt)
        self.memory._memory_observer = self.on_memory_changed

        self.accumulator.add_accumulator_observer(self.on_accumulator_changed)

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
        themed_widget(self.frame2, bg="secondary")
        
        self.button_run = tk.Button(self.frame2, text="Run", command=self.on_button_run)
        self.button_run.place(x=20, y=20, width=100, height=30)
        themed_widget(self.button_run, bg="primary", fg="secondary")

        self.button_stop = tk.Button(self.frame2, text="Stop", command=self.on_button_stop)
        self.button_stop.place(x=140, y=20, width=100, height=32)
        themed_widget(self.button_stop, bg="primary", fg="secondary")

        self.button_step = tk.Button(self.frame2, text="Step", command=self.on_button_step)
        self.button_step.place(x=20, y=70, width=220, height=32)
        themed_widget(self.button_step, bg="primary", fg="secondary")

        self.button_clear_memory = tk.Button(self.frame2, text="Clear Memory", command=self.on_button_clear_memory)
        self.button_clear_memory.place(x=20, y=120, width=220, height=32)
        themed_widget(self.button_clear_memory, bg="primary", fg="secondary")

        self.button_clear_accumulator = tk.Button(self.frame2, text="Clear Accumulator", command=self.on_button_clear_accumulator)
        self.button_clear_accumulator.place(x=20, y=170, width=220, height=32)
        themed_widget(self.button_clear_accumulator, bg="primary", fg="secondary")

        self.label_controls = tk.Label(self.frame2, text="Controls")
        self.label_controls.place(x=85, y=210, width=90, height=26)
        themed_widget(self.label_controls, bg="secondary", fg="primary")

        self.label_accumulator = tk.Label(self, text="Accumulator:")
        self.label_accumulator.place(x=60, y=289, width=130, height=26)
        themed_widget(self.label_accumulator, bg="primary", fg="secondary")

        self.label_accumulator_value = tk.Label(self, text="+000000", font=("Helvetica", 10, "bold"), state="disabled")
        self.label_accumulator_value.place(x=170, y=289, width=90, height=26)
        themed_widget(self.label_accumulator_value, bg="secondary", fg="primary")

        #self.label_status_indicator = tk.Label(self, text="Stopped", fg=RED)
        #self.label_status_indicator.place(x=125, y=0, width=90, height=26)
        #self.themed_widget(self.label_status_indicator, bg="primary")

        self.listbox_user_console = tk.Listbox(self)
        self.listbox_user_console.place(x=20, y=330, width=300, height=250)
        themed_widget(self.listbox_user_console, fg="primary", bg="secondary")

        self.cpu.output_fn = self.log_to_console

        self.load_memory_tree()

        self.on_current_changed(self.cpu.current)
            
    
    def on_memory_changed(self, address: int, value: int):
        iid = str(address)
        if self.memory_tree.exists(iid):
            self.memory_tree.set(iid, "col2", format_word(value))


    def on_read_prompt(self) -> int:
        user_input = dialogues.IntegerPrompt("Number Input","Please enter an integer between -999999 and +999999:", minvalue=-999999, maxvalue=999999)
        if user_input != None:
            return user_input.result
        else: return 0


    def on_current_changed(self, new_current):
        i = str(new_current)
        if self.memory_tree.exists(i):
            self.memory_tree.selection_set(i)
            self.memory_tree.see(i)


    def on_accumulator_changed(self, new_value):
        self.label_accumulator_value.config(text=format_word(new_value))


    def log_to_console(self, message):
        self.listbox_user_console.insert("end", str(message))
        self.listbox_user_console.see("end")


    def on_button_run(self):
        self.listbox_user_console.delete(0, tk.END)
        self.cpu.run()


    def on_button_stop(self):
        # Stop the CPU execution
        self.cpu.running = False 
        

    def on_button_step(self):
        self.cpu.step()


    def on_button_clear_memory(self):
        self.memory.reset_memory()


    def on_button_clear_accumulator(self):
        # clear the accumulator value to zero
        self.accumulator.value = 0
        
    def on_file_edit(self):
        #open the basicML editor popup
        EditDialogue(self)
    
    def on_file_load(self):
        # Open a file dialog so the user can select a BasicML program
        file_path = filedialog.askopenfilename(
            title="Select a program file",
            filetypes=[("Text Files","*.txt"), ("All Files", "*.*")]
        )
        
        # if the user cancels the file selection, stop the function
        if not file_path:
            return  

        self.current_file_path = Path(file_path)
        
        # create a loader and give it the file selected by the user
        loader = LoadHandler()
        loader.loaded_file = Path(file_path)

        # Clear memory and user console before loading
        self.on_button_clear_memory()
        self.listbox_user_console.delete(0, tk.END)
        
        # load the selected program into UVSim memory
        loader.load_memory(self.memory,self.cpu.opcode_table)

        # Make sure the first element is selected
        self.memory_tree.selection_set(0)
        self.memory_tree.see(0)

        self.accumulator.value = 0
        self.cpu.current = 0


    def on_file_reset_program(self):
        self.current_file_path = None
        self.memory.reset_memory()
        self.accumulator.value = 0
        self.listbox_user_console.delete(0, tk.END)


    def on_file_logs(self):
        log_window = tk.Toplevel(self)
        log_window.title("Logs")
        log_window.geometry("600x300")

        log_text = scrolledtext.ScrolledText(log_window, wrap="word")
        log_text.pack(fill="both", expand=True)

        if self.cpu.logs:
            log_text.insert("end","\n".join(self.cpu.logs))
        else:
            log_text.insert("end", "No logs recorded.")

        log_text.config(state="disabled")


    def load_memory_tree(self):
        self.memory_tree.delete(*self.memory_tree.get_children())
        for address in range(self.memory.register_count):
            value = self.memory.read(address)
            self.memory_tree.insert("", "end", iid=str(address), values=(f"{address:03d}", format_word(value)))

    def on_file_save(self):
            #print("DEBUG: save button was clicked")
            if not hasattr(self, 'current_file_path') or self.current_file_path is None:
                self.on_file_save_as()
            else:
                self._perform_save(self.current_file_path)

    def on_file_save_as(self):
        path_str = filedialog.asksaveasfilename(
            title = "Save Program As",
            defaultextension = ".txt",
            filetypes = [("Test files", "*.txt"), ("All files", "*.*")]
        )

        if not path_str:
            self.cpu.logs.append("No valid path was found!")
            return

        self.current_file_path = Path(path_str)
        self._perform_save(self.current_file_path)

    def _perform_save(self, file_path: Path):
        handler = SaveHandler()

        success = handler.save_memory(self.memory, file_path)

        if success:
            msg = f"Program successfully saved to {file_path.name}"
            if hasattr(self, "cpu") and hasattr(self.cpu, "logs"):
                self.cpu.logs.append(msg)
            #messagebox.showinfo("Saved", f"File saved successfully:\n{file_path}")
        else:
            pass
            #messagebox.showerror("Error", f"Failed to save file:\n{file_path}")
