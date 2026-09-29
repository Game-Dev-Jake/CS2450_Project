from register import VRegister

class VMemory():
    def __init__(self, count: int = 1):
        self.registers: list = []
        self.register_count: int = count
        for i in range(self.register_count):
            register = VRegister()
            self.registers.append(register)


    def read(self, address: int) -> int:
        if self.is_valid_address(address):
            if self.registers[address].value == None:
                return 0
            return self.registers[address].value
        else:
            pass
            #TODO Error log that WRITE call attempted to write an invalid address.


    def write(self, address: int, value: int):
        if self.is_valid_address(address):
            self.registers[address].value = value
        else:
            pass
            #TODO Error log that WRITE call attempted to write an invalid address.


    def is_valid_address(self, address):
            return isinstance(address, int) and 0 <= address < self.register_count


    def reset_memory(self):
        for i in range(self.register_count):
            self.registers[i].value = 0

    
    def display_values(self) -> str:
        lines = []
        for index, register in enumerate(self.registers):
            lines.append(f"Register: {index}. Value: {register.value:04d}")
        return "\n".join(lines)