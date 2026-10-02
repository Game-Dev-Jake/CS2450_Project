import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, ttk

RUNNING_COLOR = "#16a34a"      # green
STOPPED_COLOR = "#dc2626"      # red
CONSOLE_BACKGROUND = "#e5e7eb" # light grey

class AccumulatorPanel(ttk.LabelFrame):
    def __init__(self, parent):
        # build the panal
        super().__init__(parent, text="Accumulator", padding=8)
        ttk.Label(self, text="4-digit register to hold\ntemporary integer values.",
                  justify="left").grid(row=0, column=0, sticky="w")

        # A StringVar is a "live" piece of text: when we call
        # self._text.set("0012") the label on screen changes by itself.
        self._text = tk.StringVar(value="0000")
        tk.Label(self, textvariable=self._text, font=("Consolas", 18, "bold"),
                 relief="solid", borderwidth=1, width=6, bg="white",
                 padx=6, pady=2).grid(row=0, column=1, padx=(10, 0))
        self.columnconfigure(0, weight=1)

    def show(self, value):
        # Display a new accumulator value.
        text = f"{abs(value):04d}"     # :04d means "at least 4 digits, pad with zeros": 12 -> "0012"
        if value < 0:
            text = "-" + text          # put the minus sign back in front
        self._text.set(text)

    def reset(self):
        """Go back to the default value 0000."""
        self.show(0)

    def get_text(self):
        """Return what is on screen right now, e.g. "0012" (handy for testing)."""
        return self._text.get()

class StatusIndicator(ttk.LabelFrame):
    # tells the user if a program is running or not.
    def __init__(self, parent):
        """Build the panel. Post-condition: it shows the red "Stopped"."""
        super().__init__(parent, text="Status", padding=8)

        ttk.Label(self, text="Indicates program state.\nWill either be running or stopped.",
                  justify="left").grid(row=0, column=0, sticky="w")
        self._label = tk.Label(self, font=("Consolas", 16, "bold"))
        self._label.grid(row=0, column=1, padx=(10, 0))
        self.columnconfigure(0, weight=1)

        self.running = False
        self.set_running(False)

    def set_running(self, running):
        """ Switch between Running and Stopped. """
        self.running = running
        if running:
            self._label.config(text="● Running", fg=RUNNING_COLOR)
        else:
            self._label.config(text="● Stopped", fg=STOPPED_COLOR)

class MainConsole(ttk.LabelFrame):
    """
    displays WRITE output to the user.
    Every time the program runs a WRITE instruction (opcode 11) the value is
    printed on its own line in big bold text.
    """

    def __init__(self, parent):
        """Build the panel. Post-condition: the console is empty."""
        super().__init__(parent, text="Main Console", padding=8)

        self._text = scrolledtext.ScrolledText(self, height=12, wrap="word",
                                               font=("Consolas", 13), bg=CONSOLE_BACKGROUND,
                                               relief="flat", state="disabled")
        self._text.pack(fill="both", expand=True)

        # "Tags" are named text styles we can apply to each line.
        self._text.tag_configure("output", font=("Consolas", 13, "bold"), foreground="#111")
        self._text.tag_configure("message", font=("Consolas", 10, "italic"), foreground="#666")
        self._text.tag_configure("error", font=("Consolas", 10, "bold"), foreground=STOPPED_COLOR)

        ttk.Button(self, text="Clear Console", command=self.clear).pack(anchor="e", pady=(6, 0))

    def write(self, value):
        self._add_line(str(value), "output")

    def write_message(self, text):
        # Show a simulator note
        self._add_line(">> " + text, "message")

    def write_error(self, text):
        # Show an error in red
        self._add_line(">> ERROR: " + text, "error")

    def clear(self):
        # Remove every line. ("1.0" means line 1, character 0 = the very start.)
        self._text.config(state="normal")
        self._text.delete("1.0", "end")
        self._text.config(state="disabled")

    def get_text(self):
        # Return everything in the console as one string
        return self._text.get("1.0", "end-1c")

    def _add_line(self, text, style):
        # Unlock, add one line with the given style, scroll to it, lock again.
        self._text.config(state="normal")
        self._text.insert("end", text + "\n", style)
        self._text.see("end")                  # auto-scroll so the newest line is visible
        self._text.config(state="disabled")

class FileMenuActions:
    def add_log(self, text):
        if not hasattr(self, "_log_entries"):
            self._log_entries = []
        entry = f"{datetime.now():%H:%M:%S}  {text}"
        self._log_entries.append(entry)

        logs_text = getattr(self, "_logs_text", None)
        if logs_text is not None:           # Logs window is open -> show it live
            logs_text.config(state="normal")
            logs_text.insert("end", entry + "\n")
            logs_text.see("end")
            logs_text.config(state="disabled")

    def on_file_reset_program(self):
        """ Puts everything back to how it was right after the file was loaded, 
        so the same program can be run again from the beginning"""
        # Stop the program if it is running.
        if self.is_running:
            self.stop_program()

        # Put the original program back (or clear memory if nothing was loaded).
        if self.loaded_program is not None:
            self.memory.load_program(self.loaded_program)
        else:
            self.memory.clear()

        # Accumulator = 0, program counter = 0.
        self.cpu.reset()

        # Update my three panels.
        self.accumulator_panel.reset()
        self.status_indicator.set_running(False)
        self.main_console.clear()

        # Redraw the memory panel
        self.refresh_memory_view()

        # Tell the user and record it in the log.
        if self.loaded_program is not None:
            self.main_console.write_message("Program reset. Press Run to start again.")
            self.add_log("Program reset to its original state.")
        else:
            self.add_log("Reset with no program loaded - memory cleared.")

    def on_file_logs(self):
        """ Opens the Logs window (dialog [I] in our wireframe).
        While the window is open, new events appear in it automatically."""
        window = getattr(self, "_logs_window", None)
        if window is not None and window.winfo_exists():
            window.deiconify()
            window.lift()
            window.focus_force()
            return

        if not hasattr(self, "_log_entries"):
            self._log_entries = []

        # A Toplevel is a second window that belongs to the main window.
        window = tk.Toplevel(self.root)
        window.title("UVSim Logs")
        window.geometry("640x400")
        self._logs_window = window

        text = scrolledtext.ScrolledText(window, wrap="none", font=("Consolas", 10))
        text.pack(fill="both", expand=True, padx=8, pady=(8, 4))
        for entry in self._log_entries:          # show everything logged so far
            text.insert("end", entry + "\n")
        text.see("end")
        text.config(state="disabled")            # read-only
        self._logs_text = text                   # add_log() now updates this live

        buttons = ttk.Frame(window, padding=(8, 0, 8, 8))
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Save to File...", command=self._save_logs).pack(side="left")
        ttk.Button(buttons, text="Clear", command=self._clear_logs).pack(side="left", padx=6)
        ttk.Button(buttons, text="Close", command=self._close_logs).pack(side="right")

        # The window's own X button should clean up the same way as "Close".
        window.protocol("WM_DELETE_WINDOW", self._close_logs)

    def _save_logs(self):
        """Ask where to save, then write every log line into a .txt file."""
        path = filedialog.asksaveasfilename(parent=self._logs_window, title="Save Logs",
                                            defaultextension=".txt", initialfile="uvsim_log.txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:                              # user pressed Cancel
            return
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write("\n".join(self._log_entries) + "\n")
            messagebox.showinfo("Logs Saved", f"Log saved to:\n{path}", parent=self._logs_window)
        except OSError as error:
            messagebox.showerror("Save Failed", f"Could not save the log:\n{error}", parent=self._logs_window)

    def _clear_logs(self):
        """Empty the log and the Logs window."""
        self._log_entries.clear()
        self._logs_text.config(state="normal")
        self._logs_text.delete("1.0", "end")
        self._logs_text.config(state="disabled")

    def _close_logs(self):
        """Close the Logs window. After this, add_log() stops updating it."""
        if getattr(self, "_logs_window", None) is not None:
            self._logs_window.destroy()
        self._logs_window = None
        self._logs_text = None

    # Exit
    def on_file_exit(self):
        if self.is_running:
            question = "A program is still running.\nStop it and exit UVSim?"
        else:
            question = "Are you sure you want to exit UVSim?"

        if not messagebox.askyesno("Exit UVSim", question, parent=self.root):
            return                                   # user changed their mind

        if self.is_running:                          # 1. stop the program
            self.stop_program()
        self._close_logs()                           # 2. close the Logs window
        self.root.destroy()                          # 3. close UVSim
