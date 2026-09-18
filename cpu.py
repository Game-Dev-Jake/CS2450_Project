from memory import VMemory
from register import VRegister
import sys

MIN_WORD = -9999
MAX_WORD = 9999

def is_valid_address(address, register_count):
        return isinstance(address, int) and 0 <= address <register_count
    
def is_valid_word(value):
    # true if the value is a UVSim word
    if isinstance(value, bool) or not isinstance(value, int):
        return False
    return MIN_WORD <= value <= MAX_WORD
    
def format_word(value):
    sign = "+" if value >= 0 else "-"
    return "{}{:04d}".format(sign, abs(value))

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

    def read(self, address):
        if not is_valid_address(address, self.memory.register_count):
            self.output_fn("Error: read: address {} out of range".format(address))
            return False

        while True:
            try:
                raw = self.input_fn(
                    "Enter a word from location {:02d}:".format(address)
                    )
            except (EOFError, KeyboardInterrupt):
                self.output_fn("ERROR: Read: no input received")
                return False
            if raw is None or raw.strip() == "":
                self.output_fn("ERROR: Read: no input received")
                return False

            try:
                value = int(raw.strip())
            except ValueError:
                self.output_fn(
                    "ERROR: Read: '{}' is not a signed four-digit "
                    "number".format(raw.strip())
                )
                continue

            if not is_valid_word(value):
                    self.output_fn(
                        "ERROR: READ: value must be between {} and {}".format(
                            MIN_WORD, MAX_WORD
                        )
                    )
                    continue
            break

        if not self.memory.write_at(address, value):
            self.output_fn(
                "ERROR: READ: could not write to location {}".format(address)
            )
            return False
        return True

    def write(self, address):
        value= self.memory.read_at(address)
        if value is None:
            self.output_fn(
                "ERROR: Write: cound not read location {}".format(address)
            )
            return False
        self.output_fn(format_word(value))
        return True

    def load(self,address):
        value = self.memory.read_at(address)
        if value is None:
            self.output_fn(
                "ERROR: Load: cound not read location {}".format(address)
            )
            return False

        if not self.accumulator.set_value(value):
            self.output_fn(
                "ERROR: Load: invalid word {}".format(address)
            )
            return False

    def store(self, address):
        value = self.accumulator.value
        if not is_valid_word(value):
            self.outout_fn("ERROR: Store: accumulator holds an invalid word")
            return False

        if not self.memory.write_at(address, value):
                self.output_fn(
                    "ERROR: Store: could not write to location {}".format(address)
                )
                return False
        return True

    def ADD(self, address: int):
        pass

    def SUBTRACT(self, address: int):
        pass

    def DIVIDE(self, address: int):
        pass

    def MULTIPLY(self, address: int):
        pass

    def BRANCH(self, address: int):
        pass

    def BRANCHNEG(self, address: int):
        pass

    def BRANCHZERO(self, address: int):
        pass

    def HALT(self, address: int):
        pass
