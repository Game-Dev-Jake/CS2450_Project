from cpu import VCPU, VRegister, VMemory
from load_handler import LoadHandler
from save_handler import SaveHandler
from pathlib import Path
from application import Application

def main():
    loader = LoadHandler()
    save_handler = SaveHandler
    logs: list[str] = []
    memory_count: int = 100
    main_mem: VMemory = VMemory(logs,memory_count)
    accumulator: VRegister = VRegister(0)
    cpu: VCPU = VCPU(accumulator,main_mem,logs)
    app = Application("UVSim Application",cpu,main_mem,accumulator,logs)
    app.current_file_path = None
    app.save_handler = save_handler
    app.mainloop()

if __name__ == "__main__":
    main()