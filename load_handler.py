from pathlib import Path
from memory import VMemory
import json

#TODO Reset Memory When Loading
class LoadHandler():
    def __init__(self):
        self.loaded_file: Path = None

    def load_memory(self, mem: VMemory):
        try:
            with self.loaded_file.open("r",encoding="utf-8") as file:
                for index, line in enumerate(file):
                    mem.write(index, int(line))
        except OSError:
            pass
            #print("Failed to open file from directory.")
        except ValueError as e:
            pass
            #print(f"Invalid word in the file at line {index + 1}: {line!r}")

    def get_json_value(self, key) -> str:
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data[key]

    def save_json_value(self, key: str, value: str):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)