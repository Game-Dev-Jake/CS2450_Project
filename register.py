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
            self._value = int(str(val)[:4])


    #TODO We no longer need this function now that we truncate an invalid value.
    def set_value(self, value: int = 0) -> bool:
        if value < 10000 and value > -10000:
            self._value = value
            return True
        else:
            self._value = int(str(value)[:4])
            return False