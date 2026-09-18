import unittest
from cpu import VCPU

def make_sim(inputs=None):
    queue = list(inputs or [])
    captured = []

    def fake_input(prompt=""):
        if not queue:
            raise EOFError
        return queue.pop(0)

    def fake_output(text):
        captured.append(str(text))

    return VCPU(input_fn=fake_input, output_fn=fake_output), captured

class TestRead(unittest.TestCase):
    def test_read_valid_word(self):
        sim, _ = make_sim(["+1234"])
        self.assertTrue(sim.cpu.read(5))
        self.assertEqual(sim.memory.read_at(5), 1234)

    def test_rejects_bad_input(self):
        sim, out = make_sim(["abcd", ""])
        self.assertFalse(sim.cpu.read(5))
        self.assertEqual(sim.memory.read_at(5), 0)
        self.assertTrue(any("not a signed four-digit" in m for m in out))
    
    def test_read_reprompts_on_oversized_value(self):
        sim, _ = make_sim(["12345", "+0042"])
        self.assertTrue(sim.cpu.read(3))
        self.assertEqual(sim.memory.read_at(3), 42)

class TestWrite(unittest.TestCase):
    def test_prints_formatted_word(self):
        sim, out = make_sim()
        sim.memory.write_at(10, -7)
        self.assertTrue(sim.cpu.write(10))
        self.assertIn("-0007", out)

    def test_invalid_address(self):
        sim, out = make_sim()
        self.assertFalse(sim.cpu.write(150))
        self.assertTrue(any("WRITE" in m for m in out))

class TestLoad(unittest.TestCase):
    def test_load_copies_without_clearing_memory(self):
        sim, _ = make_sim()
        sim.memory.write_at(20, 55)
        self.assertTrue(sim.cpu.load(20))
        self.assertEqual(sim.accumulator.value, 55)
        self.assertEqual(sim.memory.read_at(20), 55)

    def test_load_invalid_address_leaves_accumulator_alone(self):
        sim, out = make_sim()
        sim.accumulator.set_value(99)
        self.assertFalse(sim.cpu.load(-1))
        self.assertEqual(sim.accumulator.value, 99)
        self.assertTrue(any("LOAD" in m for m in out))

class TestStore(unittest.TestCase):
    def test_store_copies_without_clearing_accumulator(self):
        sim, _ = make_sim()
        sim.accumulator.set_value(99)
        self.assertTrue(sim.cpu.store(30))
        self.assertEqual(sim.memory.read_at(30), 99)
        self.assertEqual(sim.accumulator.value, 99)

    def test_store_invalid_address_leaves_memory_alone(self):
        sim, out = make_sim()
        sim.accumulator.set_value(99)
        self.assertFalse(sim.cpu.store(100))
        self.assertTrue(any("STORE" in m for m in out))