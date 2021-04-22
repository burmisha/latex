import logging
log = logging.getLogger(__name__)


Z_A_X_Ru = [
    (1, 1, 'H', 'водород'),
    (2, 4, 'He', 'гелий'),
    (11, 22, 'Na', 'натрий'),
    (55, 137, 'Cs', 'цезий'),
    (60, 142, 'Nd', 'неодим'),
    (60, 143, 'Nd', 'неодим'),
    (60, 144, 'Nd', 'неодим'),
    (60, 145, 'Nd', 'неодим'),
    (60, 146, 'Nd', 'неодим'),
    (60, 148, 'Nd', 'неодим'),
    (60, 150, 'Nd', 'неодим'),
    (62, 147, 'Sm', 'самарий'),
    (62, 148, 'Sm', 'самарий'),
    (63, 153, 'Eu', 'европий'),
    (63, 151, 'Eu', 'европий'),
    (74, 180, 'W', 'вольфрам'),
    (92, 234, 'U', 'уран'),
    (92, 235, 'U', 'уран'),
    (92, 238, 'U', 'уран'),
]

class Element:
    def __init__(self, Z=None, A=None, X=None, ru=None):
        assert isinstance(A, int)
        assert isinstance(Z, int)
        assert 1 <= Z <= A
        self._A = A
        self._Z = Z
        self._ru = ru
        self._X = X


    def get_ce(self):
        return f'\\ce{{ ^{{ {self.A} }}_{{ {self.Z} }}{{ {self.X} }}'

    def get_ru(self):
        return f'{self._ru}={self.A}'

    def __format__(self, fmt):
        try:
            fmt_parts = fmt.replace(':', '|').split('|')
            if len(fmt_parts) == 1:
                main_format = fmt_parts[0]
                if main_format == 'LaTeX':
                    return self.get_ce()
                elif main_format == 'RuText':
                    return self.get_ru()
                elif main_format == 'electrons':
                    return str(int(self._Z))
                elif main_format == 'nuclons':
                    return str(int(self._A))
                elif main_format == 'protons':
                    return str(int(self._Z))
                elif main_format == 'neutrons':
                    return str(int(self._A) - int(self._Z))
                else:
                    raise RuntimeError(f'Unknown main format: {main_format!r} from {fmt!r}')
            else:
                raise RuntimeError()
        except Exception:
            log.error(f'Error in __format__ for {fmt} and {self._fraction}')
            raise



class AllElements:
    def __init__(self, Z_A_X_Ru_list):
        self._za_map = {}
        for z, a, x, ru in Z_A_X_Ru_list:
            element = Element(Z=z, A=a, X=x, ru=ru)
            self._za_map[(z, a)] = element

    def get_by_z_a(self, z=None, a=None):
        return self._za_map[(z, a)]


Elements = AllElements(Z_A_X_Ru)
