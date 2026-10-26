from cpu import VCPU, VRegister, VMemory
from load_handler import LoadHandler
from save_handler import SaveHandler
from pathlib import Path
from application import Application
from master_app import MasterApp

def main():
    loader = LoadHandler()
    save_handler = SaveHandler()
    logs: list[str] = []
    memory_count: int = 250
    main_mem: VMemory = VMemory(logs,memory_count)
    accumulator: VRegister = VRegister(0)
    cpu: VCPU = VCPU(accumulator,main_mem,logs)
    #app = Application("UVSim Application",loader,save_handler,cpu,main_mem,accumulator,logs)
    master = MasterApp()
    master.mainloop()

if __name__ == "__main__":
    main()