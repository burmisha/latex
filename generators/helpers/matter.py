from generators.helpers.value import UnitValue

FIELDS = {
    'rho': '\\rho',
    'c': 'c',
    'lmbd': '\\lambda',
    'L': '\\Ell',
    'mu': '\\mu',
}

SUFFIX = '_name'

class Matter:
    def __init__(self, name=None, **kws):
        self.Name = name
        for key, value in kws.items():
            letter = FIELDS[key]
            setattr(self, key, UnitValue(value).SetLetter(letter))
            letter_name = letter + f'_{{\\text{{{name[:1]}}}}}'
            setattr(self, key + SUFFIX, UnitValue(value).SetLetter(letter_name))
