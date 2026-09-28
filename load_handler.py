from pathlib import Path
from memory import VMemory

#TODO Reset Memory When Loading
class LoadHandler():
    def __init__(self):
        self.loaded_file: Path = None
        pass

    def load_menu(self, mem: VMemory):
        running = True
        print("Load file menu, please select from the following options:")
        while running:
            user_input = input("1: Load local file\n2: Select file on directory\n3: Exit\n")
            if not user_input.strip():
                print("Invalid input, must enter 1 or 2.")
                continue
            match user_input[0]:
                case "1":
                    self.loaded_file = self.load_local()
                    if self.loaded_file:
                        self.load_memory(mem)
                        print(f"Successfully loaded file: {self.loaded_file.name} into memory.")
                        running = False
                    else:
                        print("No file was loaded")
                case "2":
                    self.load_directory()
                case "3":
                    running = False
                case _:
                    print("Invalid input, please enter 1 or 2.")

    def load_local(self):
        path = Path("./UVSim_Files")
        files = [f for f in path.iterdir() if f.is_file()]
        if not files:
            print("No files found within UVSim_files.")
            return None

        print("\nFound files:")
        for index, file in enumerate(files, start=1):
            print(f"{index}: {file.name}")

        while True:
            user_input = input(f"\nSelect a file or 0 to Exit: (1-{len(files)}): ").strip()
            if user_input == "0":
                return None
            try:
                choice_index = int(user_input) - 1
            except ValueError:
                print("Invalid input, please enter a number.")
                continue

            if 0 <= choice_index < len(files):
                return files[choice_index]
            else:
                print(f"You must select a file between 1 and {len(files)}")

    def load_directory(self):
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