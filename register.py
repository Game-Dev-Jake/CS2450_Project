import math

class VRegister():
    def __init__(self, value: int = 0):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        int_val = int(math.floor(val))
        if int_val < 10000 and int_val > -10000:
            self._value = int_val
        else:
            magnitude = abs(val)
            truncated_val = int(str(magnitude)[:4])
            self._value = truncated_val if val >= 0 else -truncated_val