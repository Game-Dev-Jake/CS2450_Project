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
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return data[key]
        except (FileNotFoundError, json.JSONDecodeError):
            return ""

    def save_json_value(self, path: tuple, value: str):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        current_level = data

        for key in path[:-1]:
            if key not in current_level or not isinstance(current_level[key], dict):
                current_level[key] = {}
            current_level = current_level[key]

        last_key = path[-1]
        current_level[last_key] = value

        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        