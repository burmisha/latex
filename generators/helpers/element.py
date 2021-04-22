import logging
log = logging.getLogger(__name__)


Z_A_X_Ru = [
    # see https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2
    (1, 1, 'H', 'водород'),
    (1, 2, 'D', 'дейтерий'),
    (1, 3, 'T', 'тритий'),
    (2, 3, 'He', 'гелий'),
    (2, 4, 'He', 'гелий'),
    (3, 6, 'Li', 'литий'),
    (3, 7, 'Li', 'литий'),
    (4, 7, 'Be', 'бериллий'),
    (4, 9, 'Be', 'бериллий'),
    (4, 10, 'Be', 'бериллий'),
    (5, 10, 'B', 'бор'),
    (5, 10, 'B', 'бор'),
    (6, 12, 'C', 'углерод'),
    (6, 13, 'C', 'углерод'),
    (6, 14, 'C', 'углерод'),
    (7, 14, 'N', 'азот'),
    (7, 15, 'N', 'азот'),
    (8, 16, 'O', 'кислород'),
    (8, 17, 'O', 'кислород'),
    (8, 18, 'O', 'кислород'),
    (9, 19, 'F', 'фтор'),
    (10, 20, 'Ne', 'неон'),
    (10, 21, 'Ne', 'неон'),
    (10, 22, 'Ne', 'неон'),
    (11, 22, 'Na', 'натрий'),
    (11, 23, 'Na', 'натрий'),
    (11, 24, 'Mg', 'магний'),
    (11, 25, 'Mg', 'магний'),

    (18, 36, 'Ar', 'аргон'),
    (18, 37, 'Ar', 'аргон'),
    (18, 38, 'Ar', 'аргон'),
    (18, 39, 'Ar', 'аргон'),
    (18, 42, 'Ar', 'аргон'),

    (19, 39, 'K', 'калий'),
    (19, 40, 'K', 'калий'),
    (19, 41, 'K', 'калий'),

    (20, 40, 'Ca', 'кальций'),
    (20, 41, 'Ca', 'кальций'),
    (20, 42, 'Ca', 'кальций'),
    (20, 43, 'Ca', 'кальций'),
    (20, 44, 'Ca', 'кальций'),
    (20, 45, 'Ca', 'кальций'),
    (20, 46, 'Ca', 'кальций'),
    (20, 47, 'Ca', 'кальций'),
    (20, 48, 'Ca', 'кальций'),

    (33, 71, 'As', 'мышьяк'),
    (33, 72, 'As', 'мышьяк'),
    (33, 73, 'As', 'мышьяк'),
    (33, 74, 'As', 'мышьяк'),
    (33, 75, 'As', 'мышьяк'),
    (33, 76, 'As', 'мышьяк'),
    (33, 77, 'As', 'мышьяк'),

    (34, 72, 'Se', 'селен'),
    (34, 74, 'Se', 'селен'),
    (34, 75, 'Se', 'селен'),
    (34, 76, 'Se', 'селен'),
    (34, 77, 'Se', 'селен'),
    (34, 78, 'Se', 'селен'),
    (34, 79, 'Se', 'селен'),
    (34, 80, 'Se', 'селен'),
    (34, 82, 'Se', 'селен'),

    (49, 111, 'In', 'индий'),
    (49, 113, 'In', 'индий'),
    (49, 115, 'In', 'индий'),

    (51, 119, 'Sb', 'сурьма'),
    (51, 121, 'Sb', 'сурьма'),
    (51, 122, 'Sb', 'сурьма'),
    (51, 123, 'Sb', 'сурьма'),
    (51, 124, 'Sb', 'сурьма'),
    (51, 125, 'Sb', 'сурьма'),
    (51, 126, 'Sb', 'сурьма'),
    (51, 128, 'Sb', 'сурьма'),
    (51, 130, 'Sb', 'сурьма'),

    (53, 124, 'I', 'йод'),
    (53, 125, 'I', 'йод'),
    (53, 126, 'I', 'йод'),
    (53, 127, 'I', 'йод'),
    (53, 129, 'I', 'йод'),
    (53, 131, 'I', 'йод'),

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

    (95, 240, 'Am', 'амерций'),
    (95, 241, 'Am', 'амерций'),
    (95, 243, 'Am', 'амерций'),

    (97, 245, 'Bk', 'берклий'),
    (97, 246, 'Bk', 'берклий'),
    (97, 247, 'Bk', 'берклий'),
    (97, 248, 'Bk', 'берклий'),
    (97, 249, 'Bk', 'берклий'),
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
        return f'\\ce{{^{{{self._A}}}_{{{self._Z}}}{{{self._X}}}}}'

    def get_ru(self):
        return f'\\text{{{self._ru}-{self._A}}}'

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
            log.error(f'Error in __format__ for {fmt}')
            raise



class AllElements:
    def __init__(self, Z_A_X_Ru_list):
        self._za_map = {}
        self._za_list = []
        for z, a, x, ru in Z_A_X_Ru_list:
            element = Element(Z=z, A=a, X=x, ru=ru)
            self._za_map[(z, a)] = element
            self._za_list.append(element)

    def get_by_z_a(self, z=None, a=None):
        return self._za_map[(z, a)]


Elements = AllElements(Z_A_X_Ru)
ElementsList = list(Elements._za_list)
