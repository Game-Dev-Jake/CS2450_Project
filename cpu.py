from memory import VMemory
from register import VRegister
import math

MIN_WORD = -9999
MAX_WORD = 9999

# True if `address` refers to a real memory location.
def is_valid_address(address, register_count):
        return isinstance(address, int) and 0 <= address < register_count

# true if the value is a UVSim word    
def is_valid_word(value):
    if isinstance(value, bool) or not isinstance(value, int):
        return False
    return MIN_WORD <= value <= MAX_WORD

# True if `value` is a legal UVSim word.    
def format_word(value):
    sign = "+" if value >= 0 else "-"
    return "{}{:04d}".format(sign, abs(value))

class VCPU():
    def __init__(self, accum: VRegister, mem: VMemory, cur: int = 0, run_limit: int = 999, output_fn = print):
        self.output_fn = output_fn
        self.running = False
        self.accumulator: VRegister = accum
        self.memory: VMemory = mem
        self.current: int = cur
        self.run_limit: int = run_limit
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
        self.current = 0
        if count == 0:
            while self.running:
                self.step()
                run_count += 1
                if run_count > self.run_limit:
                    print("Runtime limit reached, aborting process.")
                    self.running = False
        else:
            for i in range(count):
                if self.running:
                    self.step()

    def step(self):
        word: int = self.memory.read(self.current)
        opcode, address = divmod(word, 100)
        self.current +=1
        if opcode == 0:
            print("Program reached empty register, aborting execution.")
            self.HALT(0)
        elif opcode not in self.opcode_table:
            self.UNKOWN(address)
        else:
            self.opcode_table[opcode](address)


    def UNKOWN(self, address: int):
        self.running = False
        print("An unkown opcode has been loaded.")
        pass


    def READ(self, address):
        if not is_valid_address(address, self.memory.register_count):
            return False
        value = 1000 #Temp value until we figure out input.
        #TODO Adjust input here, we need to gather input from a dialogue box.
        self.memory.write(address, value)


    def WRITE(self, address):
        value = self.memory.read(address)
        self.output_fn(format_word(value))


    def LOAD(self,address):
        value = self.memory.read(address)
        self.accumulator.value = value


    def STORE(self, address):
        value = self.accumulator.value
        self.memory.write(address, value)


    def ADD(self, address: int):
        """Adds the value at a given address to the accumulator,
        and stores the result back in the accumulator."""
        print(f"Adding {self.memory.read(address)} to {self.accumulator.value}")
        result = self.memory.read(address) + self.accumulator.value
        self.accumulator.value = result


    def SUBTRACT(self, address: int):
        """"Subtracts the value at a given address from the accumulator,
        and stores the result back in the accumulator."""
        print(f"Subtracting {self.memory.read(address)} from {self.accumulator.value}")
        result = self.accumulator.value - self.memory.read(address)
        self.accumulator.value = result


    def DIVIDE(self, address: int):
        """Divides the accumulator by the value at a given address, 
        and stores the result back in the accumulator.
        Result is be an integer by using floor division. 
        ***IF THE RESULT IS PUSHED TO A REGISTER IT WILL LIKELY RESULT 
           IN AN UNKNOWN OPCODE ERROR***"""
        print(f"Dividing {self.accumulator.value} from {self.memory.read(address)}")
        if self.memory.read(address) != 0:
            result:int = math.floor(self.accumulator.value / self.memory.read(address))
        else:
            result = 0
            #TODO Error logging goes here - Divide by zero error, auto returns 0.
        self.accumulator.value = result


    def MULTIPLY(self, address: int):
        """Multiplies the accumulator by the vaule at a given address, 
        and stores the result back in the accumulator.
        ***IF THE RESULT IS PUSHED TO A REGISTER IT WILL LIKELY RESULT 
           IN AN OUT OF BOUNDS ERROR***"""
        print(f"Multiplying {self.memory.read(address)} by {self.accumulator.value}")
        result = self.memory.read(address) * self.accumulator.value
        self.accumulator.value = result


    def BRANCH(self, address: int):
        # branch to a valid address
        if not (0 <= address <= 99):
            raise ValueError("Invalid branch address")
        
        self.current = address
        print(f"BRANCH: jumping to address {address}")


    def BRANCHNEG(self, address: int):
        # branch when accumulator is negative
        if not (0 <= address <= 99):
            raise ValueError("Invalid branch address")
        
        if self.accumulator.value < 0:
            self.current = address
            print(f"BRANCHNEG: accumulator is negative, jumping to address {address}")
        else:
            print(f"BRANCHNEG: accumulator is not negative, continuing execution")


    def BRANCHZERO(self, address: int):
        # branch when accumulator equals zero
        if not (0 <= address <= 99):
            raise ValueError("Invalid branch address")
        
        if self.accumulator.value == 0:
            self.current = address
            print(f"BRANCHZERO: accumulator is zero, jumping to address {address}")
        else:
            print(f"BRANCHZERO: accumulator is not zero, continuing execution")


    def HALT(self, address: int):
        self.running = False