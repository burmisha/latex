import logging
log = logging.getLogger(__name__)


# see https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2
# https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2
isotopes_cfg = {
    1: ('H', 'водород', 'водорода', [1, 2, 3]),
    2: ('He', 'гелий', 'гелия', [3, 4, 6, 8]),
    3: ('Li', 'литий', 'лития', [6, 7]),
    4: ('Be', 'бериллий', 'бериллия', [7, 9, 10]),
    5: ('B', 'бор', 'бора', [10, 10]),
    6: ('C', 'углерод', 'углерода', [12, 13, 14]),
    7: ('N', 'азот', 'азота', [14, 15]),
    8: ('O', 'кислород', 'кислорода', [16, 17, 18]),
    9: ('F', 'фтор', 'фтора', [19]),
    10: ('Ne', 'неон', 'неона', [20, 21, 22]),
    11: ('Na', 'натрий', 'натрия', [22, 23]),
    12: ('Mg', 'магний', 'магния', [24, 25]),
    13: ('Al', 'алюминий', 'алюминия', []),
    14: ('Si', 'кремний', 'кремния', []),
    15: ('P', 'фосфор', 'фосфора', [30, 31, 32, 33]),  # TODO: does 30 exist
    16: ('S', 'сера', 'серы', []),
    17: ('Cl', 'хлор', 'хлора', []),
    18: ('Ar', 'аргон', 'аргона', [36, 37, 38, 39, 42]),
    19: ('K', 'калий', 'калия', [39, 40, 41]),
    20: ('Ca', 'кальций', 'кальция', [40, 41, 42, 43, 44, 45, 46, 47, 48]),
    21: ('Sc', 'скандий', 'скандия', []),
    22: ('Ti', 'титан', 'титана', []),
    23: ('V', 'ванадий', 'ванадия', []),
    24: ('Cr', 'хром', 'хрома', []),
    25: ('Mn', 'марганец', 'марганца', []),
    26: ('Fe', 'железо', 'железа', []),
    27: ('Co', 'кобальт', 'кобальта', []),
    28: ('Ni', 'никель', 'никеля', []),
    29: ('Cu', 'медь', 'меди', [63, 65, 67]),
    30: ('Zn', 'цинк', 'цинка', []),
    31: ('Ga', 'галлий', 'галлия', []),
    32: ('Ge', 'германий', 'германия', []),
    33: ('As', 'мышьяк', 'мышьяка', [71, 72, 73, 74, 75, 76, 77]),
    34: ('Se', 'селен', 'селена', [72, 74, 75, 76, 77, 78, 79, 80, 82]),
    35: ('Br', 'бром', 'брома', []),
    36: ('Kr', 'криптон', 'криптона', []),
    37: ('Rb', 'рубидий', 'рубидия', []),
    38: ('Sr', 'стронций', 'стронция', []),
    39: ('Y', 'иттрий', 'иттрия', []),
    40: ('Zr', 'цирконий', 'циркония', []),
    41: ('Nb', 'ниобий', 'ниобия', []),
    42: ('Mo', 'молибден', 'молибдена', []),
    43: ('Tc', 'технеций', 'технеция', []),
    44: ('Ru', 'рутений', 'рутения', []),
    45: ('Rh', 'родий', 'родия', []),
    46: ('Pd', 'палладий', 'палладия', []),
    47: ('Ag', 'серебро', 'серебра', [105, 107, 108, 109, 111]),  # 108 is instable
    48: ('Cd', 'кадмий', 'кадмия', []),
    49: ('In', 'индий', 'индия', [111, 113, 115]),
    50: ('Sn', 'олово', 'олова', []),
    51: ('Sb', 'сурьма', 'сурьмы', [119, 121, 122, 123, 124, 125, 126, 128, 130]),
    52: ('Te', 'теллур', 'теллура', []),
    54: ('Xe', 'ксенон', 'ксенона', []),
    53: ('I', 'йод', 'йода', [124, 125, 126, 127, 129, 131]),
    55: ('Cs', 'цезий', 'цезия', [137]),
    56: ('Ba', 'барий', 'бария', []),
    57: ('La', 'лантан', 'лантана', []),
    58: ('Ce', 'церий', 'церия', []),
    59: ('Pr', 'празеодим', 'празеодима', []),
    60: ('Nd', 'неодим', 'неодима', [142, 143, 144, 145, 146, 148, 150]),
    61: ('Pm', 'прометий', 'прометия', []),
    62: ('Sm', 'самарий', 'самария', [147, 148]),
    63: ('Eu', 'европий', 'европия', [153, 151]),
    64: ('Gd', 'гадолиний', 'гадолиния', []),
    65: ('Tb', 'тербий', 'тербия', []),
    66: ('Dy', 'диспрозий', 'диспрозия', []),
    67: ('Ho', 'гольмий', 'гольмия', []),
    68: ('Er', 'эрбий', 'эрбия', []),
    69: ('Tm', 'тулий', 'тулия', []),
    70: ('Yb', 'иттербий', 'иттербия', []),
    71: ('Lu', 'лютеций', 'лютеция', []),
    72: ('Hf', 'гафний', 'гафния', []),
    73: ('Ta', 'тантал', 'тантала', []),
    74: ('W', 'вольфрам', 'вольфрама', [180]),
    75: ('Re', 'рений', 'рения', []),
    76: ('Os', 'осмий', 'осмия', []),
    77: ('Ir', 'иридий', 'иридия', []),
    78: ('Pt', 'платина', 'платины', [188, 190, 191, 192, 193, 194, 195, 196, 198, 202]),
    79: ('Au', 'золото', 'золота', []),
    80: ('Hg', 'ртуть', 'ртути', []),
    81: ('Tl', 'таллий', 'таллия', []),
    82: ('Pb', 'свинец', 'свинца', [202, 203, 204, 205, 206, 207, 208, 209, 210, 214]),    # TODO: doeas 209, 214 exist
    83: ('Bi', 'висмут', 'висмута', [205, 206, 207, 209, 210, 214]), # TODO: does 214 exist
    84: ('Po', 'полоний', 'полония', [206, 208, 209, 210, 214, 218]),  # TODO: does 214 and 218 exist
    85: ('At', 'астат', 'астата', []),
    86: ('Rn', 'радон', 'радона', [222]),
    87: ('Fr', 'франций', 'франция', []),
    88: ('Ra', 'радий', 'радия', [223, 224, 225, 226, 228]),
    89: ('Ac', 'актиний', 'актиния', []),
    90: ('Th', 'торий', 'тория', [227, 228, 229, 230, 231, 232, 234]),
    91: ('Pa', 'протактиний', 'протактиния', [229, 230, 231, 232, 233, 234]),  # does 234 exist?
    92: ('U', 'уран', 'урана', [234, 235, 238]),
    95: ('Am', 'амерций', 'амерция', [240, 241, 243]),
    97: ('Bk', 'берклий', 'берклия', [245, 246, 247, 248, 249]),
    93: ('Np', 'нептуний', 'нептуния', []),
    94: ('Pu', 'плутоний', 'плутония', [236, 237, 238, 239, 240, 241, 242, 244, 246, 247]),
    96: ('Cm', 'кюрий', 'кюрия', []),
    98: ('Cf', 'калифорний', 'калифорния', []),
    99: ('Es', 'эйнштейний', 'эйнштейния', []),
    100: ('Fm', 'фермий', 'фермия', []),
    101: ('Md', 'менделевий', 'менделевия', []),
    102: ('No', 'нобелий', 'нобелия', []),
    103: ('Lr', 'лоуренсий', 'лоуренсия', []),
    104: ('Rf', 'резерфордий', 'резерфордия', []),
    105: ('Db', 'дубний', 'дубния', []),
    106: ('Sg', 'сиборгий', 'сиборгия', []),
    107: ('Bh', 'борий', 'бория', []),
    108: ('Hs', 'хассий', 'хассия', []),
    109: ('Mt', 'мейтнерий', 'мейтнерия', []),
    110: ('Ds', 'дармштадтий', 'дармштадтия', []),
    111: ('Rg', 'рентгений', 'рентгения', []),
    112: ('Cn', 'коперниций', 'коперниция', []),
    113: ('Nh', 'нихоний', 'нихония', []),
    114: ('Fl', 'флеровий', 'флеровия', []),
    115: ('Mc', 'московий', 'московия', []),
    116: ('Lv', 'ливерморий', 'ливермория', []),
    117: ('Ts', 'теннессин', 'теннессина', []),
    118: ('Og', 'оганесон', 'оганесона', []),
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
            self._ru_roditel = 'дейтерия'
            self._X = 'D'
        elif Z == 1 and A == 3:
            self._ru = 'тритий'
            self._ru_roditel = 'трития'
            self._X = 'T'
        else:
            self._ru = isotopes_cfg[Z][1]
            self._ru_roditel = isotopes_cfg[Z][2]
            self._X = isotopes_cfg[Z][0]

        self.e = int(self._Z)
        self.p = int(self._Z)
        self.n = self._A - self._Z

    def get_ce(self):
        return f'\\ce{{^{{{self._A}}}_{{{self._Z}}}{{{self._X}}}}}'

    def get_ru(self):
        return f'\\text{{{self._ru}-{self._A}}}'

    def get_ru_name(self):
        return f'ядро {self._ru_roditel} ${self.get_ce()}$'

    def alpha(self):
        return Element(Z=self._Z - 2, A=self._A - 4)

    def beta_minus(self):
        return Element(Z=self._Z + 1, A=self._A)

    def beta_plus(self):
        return Element(Z=self._Z - 1, A=self._A)

    def beta(self):
        return self.beta_minus()

    def fall(self, fall):
        if fall == '\\beta^-' or fall == '\\beta':
            return self.beta_minus()
        elif fall == '\\beta^+':
            return self.beta_plus()
        elif fall == '\\alpha':
            return self.alpha()
        else:
            raise RuntimeError(f'Invalid fall: {fall}')

    def get_reaction(self, fall):
        if fall == '\\beta^-' or fall == '\\beta':
            addenda = 'e^- + \\tilde\\nu_e'
        elif fall == '\\beta^+':
            addenda = 'e^+ + \\nu_e'
        elif fall == '\\alpha':
            addenda = '\\ce{^4_2{He}}'
        else:
            raise RuntimeError(f'Invalid fall: {fall}')

        return f'{self.get_ce()} \\to {self.fall(fall).get_ce()} + {addenda}'

    def __format__(self, fmt):
        try:
            fmt_parts = fmt.replace(':', '|').split('|')
            if len(fmt_parts) == 1:
                main_format = fmt_parts[0]
                if main_format == 'LaTeX':
                    return self.get_ce()
                elif main_format == 'RuText':
                    return self.get_ru()
                elif main_format == 'RuName':
                    return self.get_ru_name()
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
        self._rua_map = {}
        self._za_list = []
        for Z, (_, _, _, A_list) in sorted(isotopes_cfg.items()):
            isotope = Isotope(Z, A=A_list)
            for element in isotope.GetAll():
                self._za_map[(element._Z, element._A)] = element
                self._rua_map[(element._ru, element._A)] = element
                self._za_list.append(element)

    def get_by_z_a(self, z=None, a=None):
        return self._za_map[(z, a)]

    def get_by_ru_a(self, ru=None, a=None):
        return self._rua_map[(ru, a)]

Elements = AllElements(isotopes_cfg)
ElementsList = list(Elements._za_list)
