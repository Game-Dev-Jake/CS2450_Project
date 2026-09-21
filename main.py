from cpu import VCPU, VRegister, VMemory
from load_handler import LoadHandler
from pathlib import Path

def main():
    loader = LoadHandler()
    memory_count: int = 100
    main_mem: VMemory = VMemory(memory_count)
    accumulator: VRegister = VRegister(0)
    cpu: VCPU = VCPU(accumulator,main_mem)
    print(f"Welcome to UVSim, CPU has been built with {memory_count} registers. Please enter a command to continue:")
    running = True
    while running:
        user_input = input("1: Load a File\n2: Display Values\n3. Run Program\n4. Exit\n")
        if not user_input.strip():
            print("Invalid input, must enter 1, 2, 3 or 4.")
            continue
        match user_input[0]:
            case "1":
                loader.load_menu(main_mem)
            case "2":
                valid = True
                print("Please select option to display.")
                while valid:
                    display_input = input("1: Display Accumulator\n2: Display Memory\n3. Exit\n")
                    if not display_input.strip():
                        print("Invalid input, must enter 1, 2 or 3.")
                        continue
                    match display_input[0]:
                        case "1":
                            print(f"Current Accumulator Value: {accumulator.value:04d}")
                            valid = False
                        case "2":
                            print(f"Current Memory Address Values: \n{main_mem.display_values()}")
                            valid = False
                        case "3":
                            valid = False
                        case _:
                            print("Invalid input, must enter 1, 2, or 3.")
            case "3":
                cpu.run()
            case "4":
                print("Exiting Program")
                running = False
            case _:
                print("Invalid input, must enter 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()