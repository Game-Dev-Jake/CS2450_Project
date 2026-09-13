class VRegister():
    def __init__(self, value: int = 0):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        #verification here
        self._value = val