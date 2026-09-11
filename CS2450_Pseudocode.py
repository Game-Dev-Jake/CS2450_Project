class VCPU(accumulator: VRegister, memory: VMem, current: int = 0)
    def __init__
	Current: int
    	memory = VMem(address_count);
accumulator = VRegister();
    def add()
    
    def sub()

//virtual memory class. Takes a register count and initializes with that many registers. Uses a current to track the current location in memory
class VMem(register_count: int = 1)
	def __init__
		Registercount: int;
		registers: list;
		for i in range(register_count):
			register = VRegister();
			registers.append(register);

//Virtual register class
class VRegister(value: int = 0)
	def __init__
		Self._value = value
	@Property
	Def value(self):
		Return self._value
	@value.setter
	Def value(self, value):
		Value verification goes here
		

//load handler class. Handles loading from files as well as serves lines upon request.
class LoadHandler()
	def load_from(source: string) -> bool:
		attempts to load a file from a source filepath, upon failure returns false and prints an error message.
	def load_next() -> bool:
		loads the next line from the 


Main:
	User Prompt Loop:
		Ask user for command:
			Load File
				Load and run full file
				Load and run 1 at a time
					continue
					exit
			Display 
				Memory
				Accumulator
			Exit


//testing