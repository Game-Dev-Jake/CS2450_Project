from register import VRegister

class VMemory():
    def __init__(self, count: int = 1):
        self.registers: list = []
        self.register_count: int = count
        for i in range(self.register_count):
            register = VRegister()
            self.registers.append(register)

    def read(self, address: int) -> int:
        return self.registers[address].value

    def write(self, address: int, value: int):
        self.registers[address].value = value


    def display_values(self) -> str:
        lines = []
        for index, register in enumerate(self.registers):
            lines.append(f"Register: {index}. Value: {register.value:04d}")
        return "\n".join(lines)