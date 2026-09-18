from memory import VMemory
from register import VRegister

class VCPU():
    def __init__(self, accum: VRegister, mem: VMemory, cur: int = 0):
        self.accumulator: VRegister = accum
        self.memory: VMemory = mem
        self.current: int = cur
        self.opcode_table: dict = {
            10: self.READ,
            11: self.WRITE,
            20: self.LOAD,
            21: self.STORE,
            30: self.ADD,
            31: self.SUBTRACT,
            32: self.DIVIDE,
            33: self.MULTIPLY,
            40: self.BRANCH,
            41: self.BRANCHNEG,
            42: self.BRANCHZERO,
            43: self.HALT
        }

    def step(self):
        word: int = self.memory.read(self.current)
        opcode, address = divmod(word, 100)
        self.current +=1
        if opcode not in self.opcode_table:
            self.UNKOWN(address)
        self.opcode_table[opcode](address)

    def UNKOWN(self, address: int):
        # TODO An unknown opcode has been found. Whatever we do for error handling will go here. For now, I'm printing it -Jake
        print("An unkown opcode has been loaded.")
        pass

    def READ(self, address: int):
        pass

    def WRITE(self, address: int):
        pass

    def LOAD(self, address: int):
        pass

    def STORE(self, address: int):
        pass

    def ADD(self, address: int):
        pass

    def SUBTRACT(self, address: int):
        pass

    def DIVIDE(self, address: int):
        pass

    def MULTIPLY(self, address: int):
        pass

    def BRANCH(self, address: int):
        # branch to a valid address
        if not (0 <= address <= 99):
            raise ValueError("Invalid branch address")
        self.current = address

    def BRANCHNEG(self, address: int):
        # branch when accumulator is negative
        if not (0 <= address <= 99):
            raise ValueError("Invalid branch address")
        if self.accumulator.value < 0:
            self.current = address

    def BRANCHZERO(self, address: int):
        # branch when accumulator equals zero
        if not (0 <= address <= 99):
            raise ValueError("Invalid branch address")
        if self.accumulator.value == 0:
            self.current = address

    def HALT(self, address: int):
        # halt stops execution
        self.running = False
