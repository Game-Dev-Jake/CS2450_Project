from cpu import pytest
from memory import VCPU
from register import VMemory 
import VRegister 

# ============================================================ 
# # ADD TESTS 
# # ============================================================ 
def test_ADD_positive(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, 1010) 
    cpu = VCPU(accumulator, memory) 

    cpu.ADD(10, None) 

    assert cpu.accumulator.value == 4040 

def test_ADD_negative(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, -2020) 
    cpu = VCPU(accumulator, memory) 

    cpu.ADD(10, None) 

    assert cpu.accumulator.value == 1010 

# ============================================================ 
# SUBTRACT TESTS 
# ============================================================ 
def test_SUBTRACT_positive(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, 1010) 
    cpu = VCPU(accumulator, memory) 

    cpu.SUBTRACT(10, None) 

    assert cpu.accumulator.value == 2020 

def test_SUBTRACT_negative(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, -1010) 
    cpu = VCPU(accumulator, memory) 

    cpu.SUBTRACT(10, None) 

    assert cpu.accumulator.value == 4040 

# ============================================================ 
# DIVIDE TESTS 
# ============================================================ 
def test_DIVIDE_positive(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, 5) 
    cpu = VCPU(accumulator, memory) 

    cpu.DIVIDE(10, None) 

    assert cpu.accumulator.value == 606 

def test_DIVIDE_negative(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, -5) 
    cpu = VCPU(accumulator, memory) 

    cpu.DIVIDE(10, None) 

    assert cpu.accumulator.value == -606 

def test_DIVIDE_floor_and_int(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, 7) 
    cpu = VCPU(accumulator, memory) 

    cpu.DIVIDE(10, None) 

    assert cpu.accumulator.value == 432 
    assert isinstance(cpu.accumulator.value, int) 

def test_DIVIDE_by_zero(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, 0) 
    cpu = VCPU(accumulator, memory) 

    with pytest.raises(ZeroDivisionError): 
        cpu.DIVIDE(10, None) 

# ============================================================ 
# MULTIPLY TESTS 
# ============================================================ 
def test_MULTIPLY_positive(): 
    accumulator = VRegister(1000) 
    memory = VMemory(100) 
    memory.write(10, 5) 
    cpu = VCPU(accumulator, memory) 

    cpu.MULTIPLY(10, None) 

    assert cpu.accumulator.value == 5000 

def test_MULTIPLY_negative(): 
    accumulator = VRegister(3030) 
    memory = VMemory(100) 
    memory.write(10, -2) 
    cpu = VCPU(accumulator, memory) 

    cpu.MULTIPLY(10, None) 

    assert cpu.accumulator.value == -6060