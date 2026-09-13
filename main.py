from cpu import VCPU, VRegister, VMemory

def main():
    memory_count: int = 100
    main_mem: VMemory = VMemory(memory_count)
    accumulator: VRegister = VRegister(0)
    cpu: VCPU = VCPU(accumulator,main_mem)
    print("Welcome to UVSim, please enter a command to continue:")
    running = True
    while running:
        user_input = input("1: Load a File\n2: Display Values\n3. Exit\n")
        match user_input:
            case "1":
                print("Loading File Here")
            case "2":
                print("Display Values Here")
            case "3":
                print("Exiting Program")
                running = False
            case _:
                print("Invalid input, must enter 1, 2 or 3.")

if __name__ == "__main__":
    main()