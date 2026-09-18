class VRegister():
    def __init__(self, value: int = 0):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val < 10000 and val > -10000:
            self._value = val
        else:
            # TODO however we end up handling errors, this is the spot to check if a word has overflowed. -Jake
            pass

    def set_value(self, value: int = 0) -> bool:
        if value < 10000 and value > -10000:
            self._value = value
            return True
        else:
            return False