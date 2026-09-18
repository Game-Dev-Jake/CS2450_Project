from cpu import VCPU

def test_ADD(): 
    VCPU = VCPU(3030, 0)
    assert VCPU.ADD(1010) == 4040
    assert VCPU.ADD(-2020) == 1010

def test_SUBTRACT():
    VCPU = VCPU(3030, 0)
    assert VCPU.SUBTRACT(1010) == 2020
    assert VCPU.SUBTRACT(-1010) == 4040

def test_DIVIDE(): 
    VCPU = VCPU(3030, 0)
    assert VCPU.DIVIDE(5) == 606
    assert VCPU.DIVIDE(30) == 101

def test_MULTIPLY(): 
    VCPU = VCPU(3030, 0)
    assert VCPU.MULTIPLY(5) ==15150
    assert VCPU.MULTIPLY(30) == 90900