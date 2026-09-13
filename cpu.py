from memory import VMemory
from register import VRegister

class VCPU():
    def __init__(self, accum: VRegister, mem: VMemory, cur: int = 1):
        self.accumulator: VRegister = accum
        self.memory: VMemory = mem
        self.current: int = cur
        
    def READ():
        pass

    def WRITE():
        pass

    def LOAD():
        pass

    def STORE():
        pass

    def ADD():
        pass

    def SUBTRACT():
        pass

    def DIVIDE():
        pass

    def MULTIPLY():
        pass

    def BRANCH():
        pass

    def BRANCHNEG():
        pass

    def BRANCHZERO():
        pass

    def HALT():
        pass
