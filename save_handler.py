from pathlib import Path
from memory import VMemory

class SaveHandler():
    # saves the sate of VMemory to a text file
    def __init__(self):
        # tracks the file path
        self.saved_file: Path = None

    def save_memory(self, mem: VMemory, file_path: Path) -> bool:
        try:
            with file_path.open("w", encoding="utf-8") as file:
                for index in range(mem.register_count):
                    word = mem.read(index)
                    if word == 0:
                        return True
                    file.write(f"{word:+07d}\n")

            self.saved_file = file_path
            return True
        
        except OSError as e:
            #print(f"Failed to open or write file to directory: {e}")
            return False