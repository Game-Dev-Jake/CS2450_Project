from cpu import VCPU, VRegister, VMemory
from load_handler import LoadHandler
from pathlib import Path
from application import Application

def main():
    app = Application("UVSim Application")
    loader = LoadHandler()
    memory_count: int = 100
    main_mem: VMemory = VMemory(memory_count)
    accumulator: VRegister = VRegister(0)
    cpu: VCPU = VCPU(accumulator,main_mem)
    app.mainloop()

if __name__ == "__main__":
    main()