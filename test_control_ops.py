import unittest
from cpu import VCPU
from register import VRegister
from memory import VMemory

"""
unit tests for VCPU control ops: BRANCH,BRANCHNEG, BRANCHZERO, HALT
"""


def make_cpu(accumulator_value=0, memory_count=100, current=0):
    # helper to build a fresh VCPU for each test
    accumulator = VRegister(accumulator_value)
    memory = VMemory(memory_count)
    return VCPU(accumulator, memory, current)

class TestBranch(unittest.TestCase):
    #  branch to a valid address
    
    def test_branch_success_valid_address(self):
        # test that BRANCH jumps to a valid address
        cpu = make_cpu() 
        cpu.BRANCH(10)
        self.assertEqual(cpu.current, 10)

    def test_branch_failure_invalid_address(self):
        # test that BRANCH raises ValueError for invalid address
        cpu = make_cpu()
        with self.assertRaises(ValueError):
            cpu.BRANCH(150) # out of 00-99 range

class TestBranchNeg(unittest.TestCase):
    #  branch when accumulator is negative
    
    def test_branchneg_success_accumulator_negative(self):
        # test that BRANCHNEG jumps when accumulator is negative
        cpu = make_cpu(accumulator_value=-5)
        cpu.BRANCHNEG(7)
        self.assertEqual(cpu.current, 7)
    
    def test_branchneg_failure_accumulator_not_negative(self):
        # test that BRANCHNEG does not jump when accumulator is not negative
        cpu = make_cpu(accumulator_value=3, current=20)
        cpu.BRANCHNEG(7)
        # current should stay wherever it was set not jump to 7
        
        # here we're calling BRANCHNEG directly so current stays at 20
        self.assertEqual(cpu.current, 20)
        
class TestBranchZero(unittest.TestCase):
    # branch wheen accumulator equals zero
    
    def test_branchzero_success_accumulator_zero(self):
        # test that BRANCHZERO jumps when accumulator equals zero
        cpu = make_cpu(accumulator_value=0)
        cpu.BRANCHZERO(12)
        self.assertEqual(cpu.current, 12)
        
    def test_branchzero_failure_accumulator_not_zero(self):
        # test that BRANCHZERO does not jump when accumulator is not zero
        cpu = make_cpu(accumulator_value=-8, current=5)
        cpu.BRANCHZERO(12)
        self.assertEqual(cpu.current, 5) # unchanged, no jump
        
class TestHalt(unittest.TestCase):
    # halt stops execution
    
    def test_halt_success_stops_running(self):
        # test that HALT stops the CPU from running
        cpu = make_cpu()
        self.assertTrue(cpu.running) # should be running at start
        cpu.HALT(0) # address is ignored for HALT
        self.assertFalse(cpu.running) # should be stopped after HALT
    
    def test_halt_failure_stop_does_not_run_after_halt(self):
        # test that after HALT, the CPU does not run any further instructions
        cpu = make_cpu()
        cpu.HALT(0)
        self.assertFalse(cpu.running)