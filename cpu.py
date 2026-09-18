from memory import VMemory
from register import VRegister

class VCPU():
    def __init__(self, accum: VRegister, mem: VMemory, cur: int = 0):
        self.running = False
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

    def run(self, count: int = 0):
        run_count: int = 0
        self.running = True
        if count == 0:
            while self.running:
                self.step()
                run_count += 1
                if run_count > 99:
                    print("Runtime limit reached, aborting process.")
                    running = False
        else:
            for i in range(count):
                if self.running:
                    self.step()

    def step(self):
        word: int = self.memory.read(self.current)
        opcode, address = divmod(word, 100)
        self.current +=1
        if opcode not in self.opcode_table:
            self.UNKOWN(address)
        elif opcode == 0:
            self.HALT()
        else:
            self.opcode_table[opcode](address)

    def UNKOWN(self, address: int):
        self.running = False
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

    def ADD(self, address: int, accum):
        result = address + accum
        return result

    def SUBTRACT(self, address: int, accum):
        result = accum - address
        return result

    def DIVIDE(self, address: int, accum):
        "Will currently always return an 'unknown opcode has been loaded' error because a 4 digit number divided by a 4 digit number is not a 4 digit number"
        result = accum / address
        return result

    def MULTIPLY(self, address: int, accum):
        "Will currently always return an 'out of bounds' error because a 4 digit number multiplied by a 4 digit number is not a 4 digit number"
        result = address * accum
        return result

    def BRANCH(self, address: int):
        pass

    def BRANCHNEG(self, address: int):
        pass

    def BRANCHZERO(self, address: int):
        pass

    def HALT(self, address: int):
        self.running = False
        pass
