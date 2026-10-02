from pathlib import Path
from memory import VMemory

#TODO Reset Memory When Loading
class LoadHandler():
    def __init__(self):
        self.loaded_file: Path = None
        pass

    def load_memory(self, mem: VMemory):
        try:
            with self.loaded_file.open("r",encoding="utf-8") as file:
                for index, line in enumerate(file):
                    mem.write(index, int(line))
        except OSError:
            print("Failed to open file from directory.")
        except ValueError as e:
            print(f"Invalid word in the file at line {index + 1}: {line!r}")