from cpu import VCPU, VRegister, VMemory
from load_handler import LoadHandler
from pathlib import Path
from application import Application

def main():
    loader = LoadHandler()
    logs: list[str] = []
    memory_count: int = 100
    main_mem: VMemory = VMemory(logs,memory_count)
    accumulator: VRegister = VRegister(0)
    cpu: VCPU = VCPU(accumulator,main_mem,logs)
    app = Application("UVSim Application",cpu,main_mem,accumulator,logs)
    app.mainloop()

if __name__ == "__main__":
    main()