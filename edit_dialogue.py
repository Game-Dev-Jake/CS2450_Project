
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from cpu import format_word


class EditDialogue(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)

        #set access to the main app, and the size, title, and behavior
        self.app = app
        self.title("UVSim - Edit Program")
        self.geometry("500x550")
        self.resizable(True, True)
        self.transient(app)
        
        ##edit menu
        
        #create a menu bar for the window
        self.menu_bar = tk.Menu(self)
        
        #edit dropdown menu created
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0) #tearoff prevents from being detatched
        
        #Cut removes text and copies it to the clipboard 
        self.edit_menu.add_command(
            label="cut",
            command=lambda: self.editor.event_generate("<<Cut>>")
        )
        #copy placed the selected text in the clipboard
        self.edit_menu.add_command(
            label="copy",
            command=lambda: self.editor.event_generate("<<Copy>>")
        )
        #paste  inserts text from the clipboard
        self.edit_menu.add_command(
            label="paste",
            command=lambda: self.editor.event_generate("<<Paste>>")
        )
        #delete calls our custom delete_text method
        self.edit_menu.add_command(
            label="delete",
            command=self.delete_text
        )
        #add the edit dropdown to the menu bar and attaches the menu bar to the popup window
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.config(menu=self.menu_bar)

        ##popup title
        #title of the popup window
        self.label_title = ttk.Label(
            self,
            text="BasicML Program Editor",
            font=("Arial", 16, "bold")
        )
        #places the heading 
        self.label_title.pack(pady=15)

        ## editing toolbar
        # creates a frame to hold the four editing buttons
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(pady=5)
        
        #cut button
        self.cut_button = ttk.Button(
            self.toolbar,
            text="Cut",
            command=lambda: self.editor.event_generate("<<Cut>>")
        )
        self.cut_button.pack(side="left", padx=5)
        
        #copy button
        self.copy_button = ttk.Button(
            self.toolbar,
            text="Copy",
            command=lambda: self.editor.event_generate("<<Copy>>")
        )
        self.copy_button.pack(side="left", padx=5)
        
        #paste button
        self.paste_button = ttk.Button(
            self.toolbar,
            text="Paste",
            command=lambda: self.editor.event_generate("<<Paste>>")
        )
        self.paste_button.pack(side="left", padx=5)
        #delete button
        self.delete_button = ttk.Button(
            self.toolbar,
            text="Delete",
            command=self.delete_text
        )
        self.delete_button.pack(side="left", padx=5)
        
        ##basicml text editor
        #creating a scrolling text box where users can edit the basicml
        self.editor = scrolledtext.ScrolledText(
            self,
            font=("Courier", 12),
            undo=True, #allow undo while editing
            wrap="none" #keep long lines from automatically wrapping
        )
        #making the editor expand to fil available space
        self.editor.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        ##load current memory into the editor
        #loop through every memory address in UVSim 
        for address in range(self.app.memory.register_count):
            value = self.app.memory.read(address) 
            #formats the value as four-digit ML and inserts
            self.editor.insert("end", format_word(value) + "\n") 
        
        ##apply changes button
        #when clicked, run the apply_changes method
        self.apply_button = ttk.Button(
            self,
            text="Apply Changes",
            command=self.apply_changes
        )
        self.apply_button.pack(pady=5)

        ##close button
        #closes the popup without applying any pendings
        self.close_button = ttk.Button(
            self,
            text="Close",
            command=self.destroy
        )
        self.close_button.pack(pady=15)

    
    ##apply changes methods
    #reads the edited program,validate it and update memory
    def apply_changes(self):
        #get all the text from the editor
        text = self.editor.get("1.0", "end-1c")
        lines = text.splitlines()
        
        #make sure the program fits in memory
        if len(lines) > self.app.memory.register_count:
            messagebox.showerror(
                "Error",
                "Too many instructions for UVSim memory.",
                parent=self
            )
            return
        #store valid ML
        values = []
        
        #check every instruction before changing memory
        for line_number, line in enumerate(lines, start=1):
            word = line.strip()
            
            #exactly five characters
            #a + or - sign
            #four ascii digits
            if (
                len(word) != 5
                or word[0] not in "+-"
                or not word[1:].isascii()
                or not word[1:].isdigit()
            ):
                #identify the errors
                messagebox.showerror(
                    "Invalid BasicML",
                    f"Invalid instruction on line {line_number}: {word!r}\n"
                    "Use a sign and four digits, like +1007.",
                    parent=self
                )
                return
            
            values.append(int(word)) #convert and becomes integer
         
        ##update memory   
        #all instructions are valid, so update the memory
        self.app.memory.reset_memory()

        #write each valids to its adddress
        for address, value in enumerate(values):
            self.app.memory.write(address, value)
        
        self.app.cpu.current = 0 #reset address
        self.app.accumulator.value = 0 #reset values
        
        messagebox.showinfo(
            "Success",
            "Program changes applied to UVSim memory!",
            parent=self
        )
        
    ##deletes the selected text   
    def delete_text(self):
        try:
            self.editor.delete("sel.first", "sel.last")#  delete text between the first and last selected 
        except tk.TclError:
            pass
        