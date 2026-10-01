from register import VRegister
from collections.abc import Callable
from datetime import datetime

class VMemory():
    def __init__(self, logs: list[str], count: int = 1):
        self.registers: list = []
        self.register_count: int = count
        self.logs = logs
        self._memory_observer: Callable = None
        for i in range(self.register_count):
            register = VRegister()
            self.registers.append(register)

    def set_memory_observer(self, callable):
        self._memory_observer = callable

    def read(self, address: int) -> int:
        if self.is_valid_address(address):
            if self.registers[address].value == None:
                return 0
            return self.registers[address].value
        else:
            self.log("ERROR: Attempted to write to an invalid address.")


    def write(self, address: int, value: int):
        if self.is_valid_address(address):
            self.registers[address].value = value
            if self._memory_observer:
                self._memory_observer(address, self.registers[address].value)
        else:
            self.log("ERROR: Attempted to write to an invalid address.")


    def is_valid_address(self, address):
            return isinstance(address, int) and 0 <= address < self.register_count


    def reset_memory(self):
        for i in range(self.register_count):
            self.write(i, 0)

    
    def display_values(self) -> str:
        lines = []
        for index, register in enumerate(self.registers):
            lines.append(f"Register: {index}. Value: {register.value:04d}")
        return "\n".join(lines)

    def log(self, log_message: str = ""):
        now = datetime.now()
        current_time: str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(current_time + " " + log_message)