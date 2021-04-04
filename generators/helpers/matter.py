from generators.helpers.value import UnitValue


class Matter:
    def __init__(self, name=None, **kws):
        self.Name = name
        for key, value in kws.items():
            assert key in ['rho', 'c', 'lmbd', 'L', 'mu']
            setattr(self, key, UnitValue(value))
