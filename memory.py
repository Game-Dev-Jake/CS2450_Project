from register import VRegister

class VMemory():
    def __init__(self, count: int = 1):
        self.registers: list = []
        self.register_count: int = count
        for i in range(self.register_count):
            register = VRegister()
            self.registers.append(register)

    def read():
        pass
    
    def write():
        pass