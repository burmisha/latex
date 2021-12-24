import logging
log = logging.getLogger(__name__)


# see https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2
# https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2
isotopes_cfg = {
    1: ('H', 'водород', [1, 2, 3]),
    2: ('He', 'гелий', [3, 4, 6, 8]),
    3: ('Li', 'литий', [6, 7]),
    4: ('Be', 'бериллий', [7, 9, 10]),
    5: ('B', 'бор', [10, 10]),
    6: ('C', 'углерод', [12, 13, 14]),
    7: ('N', 'азот', [14, 15]),
    8: ('O', 'кислород', [16, 17, 18]),
    9: ('F', 'фтор', [19]),
    10: ('Ne', 'неон', [20, 21, 22]),
    11: ('Na', 'натрий', [22, 23]),
    12: ('Mg', 'магний', [24, 25]),
    13: ('Al', 'алюминий', []),
    14: ('Si', 'кремний', []),
    15: ('P', 'фосфор', []),
    16: ('S', 'сера', []),
    17: ('Cl', 'хлор', []),
    18: ('Ar', 'аргон', [36, 37, 38, 39, 42]),
    19: ('K', 'калий', [39, 40, 41]),
    20: ('Ca', 'кальций', [40, 41, 42, 43, 44, 45, 46, 47, 48]),
    21: ('Sc', 'скандий', []),
    22: ('Ti', 'титан', []),
    23: ('V', 'ванадий', []),
    24: ('Cr', 'хром', []),
    25: ('Mn', 'марганец', []),
    26: ('Fe', 'железо', []),
    27: ('Co', 'кобальт', []),
    28: ('Ni', 'никель', []),
    29: ('Cu', 'медь', [63, 65, 67]),
    30: ('Zn', 'цинк', []),
    31: ('Ga', 'галлий', []),
    32: ('Ge', 'германий', []),
    33: ('As', 'мышьяк', [71, 72, 73, 74, 75, 76, 77]),
    34: ('Se', 'селен', [72, 74, 75, 76, 77, 78, 79, 80, 82]),
    35: ('Br', 'бром', []),
    36: ('Kr', 'криптон', []),
    37: ('Rb', 'рубидий', []),
    38: ('Sr', 'стронций', []),
    39: ('Y', 'иттрий', []),
    40: ('Zr', 'цирконий', []),
    41: ('Nb', 'ниобий', []),
    42: ('Mo', 'молибден', []),
    43: ('Tc', 'технеций', []),
    44: ('Ru', 'рутений', []),
    45: ('Rh', 'родий', []),
    46: ('Pd', 'палладий', []),
    47: ('Ag', 'серебро', [105, 107, 108, 109, 111]),  # 108 is instable
    48: ('Cd', 'кадмий', []),
    49: ('In', 'индий', [111, 113, 115]),
    50: ('Sn', 'олово', []),
    51: ('Sb', 'сурьма', [119, 121, 122, 123, 124, 125, 126, 128, 130]),
    52: ('Te', 'теллур', []),
    54: ('Xe', 'ксенон', []),
    53: ('I', 'йод', [124, 125, 126, 127, 129, 131]),
    55: ('Cs', 'цезий', [137]),
    56: ('Ba', 'барий', []),
    57: ('La', 'лантан', []),
    58: ('Ce', 'церий', []),
    59: ('Pr', 'празеодим', []),
    60: ('Nd', 'неодим', [142, 143, 144, 145, 146, 148, 150]),
    61: ('Pm', 'прометий', []),
    62: ('Sm', 'самарий', [147, 148]),
    63: ('Eu', 'европий', [153, 151]),
    64: ('Gd', 'гадолиний', []),
    65: ('Tb', 'тербий', []),
    66: ('Dy', 'диспрозий', []),
    67: ('Ho', 'гольмий', []),
    68: ('Er', 'эрбий', []),
    69: ('Tm', 'тулий', []),
    70: ('Yb', 'иттербий', []),
    71: ('Lu', 'лютеций', []),
    72: ('Hf', 'гафний', []),
    73: ('Ta', 'тантал', []),
    74: ('W', 'вольфрам', [180]),
    75: ('Re', 'рений', []),
    76: ('Os', 'осмий', []),
    77: ('Ir', 'иридий', []),
    78: ('Pt', 'платина', [188, 190, 191, 192, 193, 194, 195, 196, 198, 202]),
    79: ('Au', 'золото', []),
    80: ('Hg', 'ртуть', []),
    81: ('Tl', 'таллий', []),
    82: ('Pb', 'свинец', []),
    83: ('Bi', 'висмут', []),
    84: ('Po', 'полоний', []),
    85: ('At', 'астат', []),
    86: ('Rn', 'радон', []),
    87: ('Fr', 'франций', []),
    88: ('Ra', 'радий', []),
    89: ('Ac', 'актиний', []),
    90: ('Th', 'торий', []),
    91: ('Pa', 'протактиний', []),
    92: ('U', 'уран', [234, 235, 238]),
    95: ('Am', 'амерций', [240, 241, 243]),
    97: ('Bk', 'берклий', [245, 246, 247, 248, 249]),
    93: ('Np', 'нептуний', []),
    94: ('Pu', 'плутоний', []),
    96: ('Cm', 'кюрий', []),
    98: ('Cf', 'калифорний', []),
    99: ('Es', 'эйнштейний', []),
    100: ('Fm', 'фермий', []),
    101: ('Md', 'менделевий', []),
    102: ('No', 'нобелий', []),
    103: ('Lr', 'лоуренсий', []),
    104: ('Rf', 'резерфордий', []),
    105: ('Db', 'дубний', []),
    106: ('Sg', 'сиборгий', []),
    107: ('Bh', 'борий', []),
    108: ('Hs', 'хассий', []),
    109: ('Mt', 'мейтнерий', []),
    110: ('Ds', 'дармштадтий', []),
    111: ('Rg', 'рентгений', []),
    112: ('Cn', 'коперниций', []),
    113: ('Nh', 'нихоний', []),
    114: ('Fl', 'флеровий', []),
    115: ('Mc', 'московий', []),
    116: ('Lv', 'ливерморий', []),
    117: ('Ts', 'теннессин', []),
    118: ('Og', 'оганесон', []),
}


class Element:
    def __init__(self, Z=None, A=None):
        assert isinstance(A, int)
        assert isinstance(Z, int)
        assert 1 <= Z <= A
        self._A = A
        self._Z = Z

        if Z == 1 and A == 2:
            self._ru = 'дейтерий'
            self._X = 'D'
        elif Z == 1 and A == 3:
            self._ru = 'тритий'
            self._X = 'T'
        else:
            self._ru = isotopes_cfg[Z][1]
            self._X = isotopes_cfg[Z][0]

        self.e = int(self._Z)
        self.p = int(self._Z)
        self.n = self._A - self._Z

    def get_ce(self):
        return f'\\ce{{^{{{self._A}}}_{{{self._Z}}}{{{self._X}}}}}'

    def get_ru(self):
        return f'\\text{{{self._ru}-{self._A}}}'

    def alpha(self):
        return Element(Z=self._Z - 2, A=self._A - 4)

    def beta_minus(self):
        return Element(Z=self._Z + 1, A=self._A)

    def beta_plus(self):
        return Element(Z=self._Z - 1, A=self._A)

    def beta(self):
        return self.beta_minus()

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
                    return str(self.e)
                elif main_format == 'nuclons':
                    return str(self.p + self.n)
                elif main_format == 'protons':
                    return str(self.p)
                elif main_format == 'neutrons':
                    return str(self.n)
                else:
                    raise RuntimeError(f'Unknown main format: {main_format!r} from {fmt!r}')
            else:
                raise RuntimeError()
        except Exception:
            log.error(f'Error in __format__ for {fmt}')
            raise


class Isotope:
    def __init__(self, Z, A=None):
        self._Z = Z
        self._A = set(A or [])

    def GetAll(self):
        for a in sorted(self._A):
            yield Element(Z=self._Z, A=a)

    def GetOne(self, a):
        assert a in self._A
        return Element(Z=self._Z, A=a)


class AllElements:
    def __init__(self, isotopes_cfg):
        self._za_map = {}
        self._za_list = []
        for Z, (_, _, A_list) in sorted(isotopes_cfg.items()):
            isotope = Isotope(Z, A=A_list)
            for element in isotope.GetAll():
                self._za_map[(element._Z, element._A)] = element
                self._za_list.append(element)

    def get_by_z_a(self, z=None, a=None):
        return self._za_map[(z, a)]


Elements = AllElements(isotopes_cfg)
ElementsList = list(Elements._za_list)
