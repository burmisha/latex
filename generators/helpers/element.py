from typing import List, Optional

import logging
log = logging.getLogger(__name__)

import attr


@attr.s
class Isotope:
    X: str = attr.ib()
    Z: int = attr.ib()
    ru: str = attr.ib()
    ru_roditelny: str = attr.ib()
    stable_a: List[int] = attr.ib()
    lower_a: Optional[int] = attr.ib(default=0)
    upper_a: Optional[int] = attr.ib(default=0)

    def GetOne(self, a: int):
        return Element(Z=self.Z, A=a, X=self.X, ru=self.ru, ru_roditelny=self.ru_roditelny)

    def GetAll(self):
        lower_bound = self.lower_a or (min(self.stable_a) if self.stable_a else None)
        upper_bound = self.upper_a or (max(self.stable_a) if self.stable_a else None)
        if lower_bound and upper_bound:
            a_values = range(lower_bound, upper_bound + 1)
        else:
            a_values = []

        for a in a_values:
            yield Element(Z=self.Z, A=a, X=self.X, ru=self.ru, ru_roditelny=self.ru_roditelny)

    def GetStable(self):
        for a in sorted(self.stable_a):
            yield Element(Z=self.Z, A=a, X=self.X, ru=self.ru, ru_roditelny=self.ru_roditelny)


# see https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2
# https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2
Isotopes = [
    Isotope(X='H',  Z=1, ru='водород',       ru_roditelny='водорода',    stable_a=[1, 2, 3]),
    Isotope(X='He', Z=2, ru='гелий',         ru_roditelny='гелия',       stable_a=[3, 4, 6, 8]),
    Isotope(X='Li', Z=3, ru='литий',         ru_roditelny='лития',       stable_a=[6, 7]),
    Isotope(X='Be', Z=4, ru='бериллий',      ru_roditelny='бериллия',    stable_a=[7, 9, 10]),
    Isotope(X='B',  Z=5, ru='бор',           ru_roditelny='бора',        stable_a=[10, 10]),
    Isotope(X='C',  Z=6, ru='углерод',       ru_roditelny='углерода',    stable_a=[12, 13, 14]),
    Isotope(X='N',  Z=7, ru='азот',          ru_roditelny='азота',       stable_a=[14, 15]),
    Isotope(X='O',  Z=8, ru='кислород',      ru_roditelny='кислорода',   stable_a=[16, 17, 18]),
    Isotope(X='F',  Z=9, ru='фтор',          ru_roditelny='фтора',       stable_a=[19]),
    Isotope(X='Ne', Z=10, ru='неон',         ru_roditelny='неона',       stable_a=[20, 21, 22]),
    Isotope(X='Na', Z=11, ru='натрий',       ru_roditelny='натрия',      stable_a=[22, 23]),
    Isotope(X='Mg', Z=12, ru='магний',       ru_roditelny='магния',      stable_a=[24, 25]),
    Isotope(X='Al', Z=13, ru='алюминий',     ru_roditelny='алюминия',    stable_a=[]),
    Isotope(X='Si', Z=14, ru='кремний',      ru_roditelny='кремния',     stable_a=[]),
    Isotope(X='P',  Z=15, ru='фосфор',       ru_roditelny='фосфора',     stable_a=[31, 32, 33], lower_a=30),
    Isotope(X='S',  Z=16, ru='сера',         ru_roditelny='серы',        stable_a=[]),
    Isotope(X='Cl', Z=17, ru='хлор',         ru_roditelny='хлора',       stable_a=[]),
    Isotope(X='Ar', Z=18, ru='аргон',        ru_roditelny='аргона',      stable_a=[36, 37, 38, 39, 42]),
    Isotope(X='K',  Z=19, ru='калий',        ru_roditelny='калия',       stable_a=[39, 40, 41]),
    Isotope(X='Ca', Z=20, ru='кальций',      ru_roditelny='кальция',     stable_a=[40, 41, 42, 43, 44, 45, 46, 47, 48]),
    Isotope(X='Sc', Z=21, ru='скандий',      ru_roditelny='скандия',     stable_a=[]),
    Isotope(X='Ti', Z=22, ru='титан',        ru_roditelny='титана',      stable_a=[]),
    Isotope(X='V',  Z=23, ru='ванадий',      ru_roditelny='ванадия',     stable_a=[]),
    Isotope(X='Cr', Z=24, ru='хром',         ru_roditelny='хрома',       stable_a=[]),
    Isotope(X='Mn', Z=25, ru='марганец',     ru_roditelny='марганца',    stable_a=[]),
    Isotope(X='Fe', Z=26, ru='железо',       ru_roditelny='железа',      stable_a=[]),
    Isotope(X='Co', Z=27, ru='кобальт',      ru_roditelny='кобальта',    stable_a=[]),
    Isotope(X='Ni', Z=28, ru='никель',       ru_roditelny='никеля',      stable_a=[]),
    Isotope(X='Cu', Z=29, ru='медь',         ru_roditelny='меди',        stable_a=[63, 65, 67]),
    Isotope(X='Zn', Z=30, ru='цинк',         ru_roditelny='цинка',       stable_a=[]),
    Isotope(X='Ga', Z=31, ru='галлий',       ru_roditelny='галлия',      stable_a=[]),
    Isotope(X='Ge', Z=32, ru='германий',     ru_roditelny='германия',    stable_a=[]),
    Isotope(X='As', Z=33, ru='мышьяк',       ru_roditelny='мышьяка',     stable_a=[71, 72, 73, 74, 75, 76, 77]),
    Isotope(X='Se', Z=34, ru='селен',        ru_roditelny='селена',      stable_a=[72, 74, 75, 76, 77, 78, 79, 80, 82]),
    Isotope(X='Br', Z=35, ru='бром',         ru_roditelny='брома',       stable_a=[]),
    Isotope(X='Kr', Z=36, ru='криптон',      ru_roditelny='криптона',    stable_a=[]),
    Isotope(X='Rb', Z=37, ru='рубидий',      ru_roditelny='рубидия',     stable_a=[]),
    Isotope(X='Sr', Z=38, ru='стронций',     ru_roditelny='стронция',    stable_a=[]),
    Isotope(X='Y',  Z=39, ru='иттрий',       ru_roditelny='иттрия',      stable_a=[]),
    Isotope(X='Zr', Z=40, ru='цирконий',     ru_roditelny='циркония',    stable_a=[]),
    Isotope(X='Nb', Z=41, ru='ниобий',       ru_roditelny='ниобия',      stable_a=[]),
    Isotope(X='Mo', Z=42, ru='молибден',     ru_roditelny='молибдена',   stable_a=[]),
    Isotope(X='Tc', Z=43, ru='технеций',     ru_roditelny='технеция',    stable_a=[]),
    Isotope(X='Ru', Z=44, ru='рутений',      ru_roditelny='рутения',     stable_a=[]),
    Isotope(X='Rh', Z=45, ru='родий',        ru_roditelny='родия',       stable_a=[]),
    Isotope(X='Pd', Z=46, ru='палладий',     ru_roditelny='палладия',    stable_a=[]),
    Isotope(X='Ag', Z=47, ru='серебро',      ru_roditelny='серебра',     stable_a=[105, 107, 109, 111]),
    Isotope(X='Cd', Z=48, ru='кадмий',       ru_roditelny='кадмия',      stable_a=[]),
    Isotope(X='In', Z=49, ru='индий',        ru_roditelny='индия',       stable_a=[111, 113, 115]),
    Isotope(X='Sn', Z=50, ru='олово',        ru_roditelny='олова',       stable_a=[]),
    Isotope(X='Sb', Z=51, ru='сурьма',       ru_roditelny='сурьмы',      stable_a=[119, 121, 122, 123, 124, 125, 126, 128, 130]),
    Isotope(X='Te', Z=52, ru='теллур',       ru_roditelny='теллура',     stable_a=[]),
    Isotope(X='Xe', Z=54, ru='ксенон',       ru_roditelny='ксенона',     stable_a=[]),
    Isotope(X='I',  Z=53, ru='йод',          ru_roditelny='йода',        stable_a=[124, 125, 126, 127, 129, 131]),
    Isotope(X='Cs', Z=55, ru='цезий',        ru_roditelny='цезия',       stable_a=[137]),
    Isotope(X='Ba', Z=56, ru='барий',        ru_roditelny='бария',       stable_a=[]),
    Isotope(X='La', Z=57, ru='лантан',       ru_roditelny='лантана',     stable_a=[]),
    Isotope(X='Ce', Z=58, ru='церий',        ru_roditelny='церия',       stable_a=[]),
    Isotope(X='Pr', Z=59, ru='празеодим',    ru_roditelny='празеодима',  stable_a=[]),
    Isotope(X='Nd', Z=60, ru='неодим',       ru_roditelny='неодима',     stable_a=[142, 143, 144, 145, 146, 148, 150]),
    Isotope(X='Pm', Z=61, ru='прометий',     ru_roditelny='прометия',    stable_a=[]),
    Isotope(X='Sm', Z=62, ru='самарий',      ru_roditelny='самария',     stable_a=[147, 148]),
    Isotope(X='Eu', Z=63, ru='европий',      ru_roditelny='европия',     stable_a=[153, 151]),
    Isotope(X='Gd', Z=64, ru='гадолиний',    ru_roditelny='гадолиния',   stable_a=[]),
    Isotope(X='Tb', Z=65, ru='тербий',       ru_roditelny='тербия',      stable_a=[]),
    Isotope(X='Dy', Z=66, ru='диспрозий',    ru_roditelny='диспрозия',   stable_a=[]),
    Isotope(X='Ho', Z=67, ru='гольмий',      ru_roditelny='гольмия',     stable_a=[]),
    Isotope(X='Er', Z=68, ru='эрбий',        ru_roditelny='эрбия',       stable_a=[]),
    Isotope(X='Tm', Z=69, ru='тулий',        ru_roditelny='тулия',       stable_a=[]),
    Isotope(X='Yb', Z=70, ru='иттербий',     ru_roditelny='иттербия',    stable_a=[]),
    Isotope(X='Lu', Z=71, ru='лютеций',      ru_roditelny='лютеция',     stable_a=[]),
    Isotope(X='Hf', Z=72, ru='гафний',       ru_roditelny='гафния',      stable_a=[]),
    Isotope(X='Ta', Z=73, ru='тантал',       ru_roditelny='тантала',     stable_a=[]),
    Isotope(X='W',  Z=74, ru='вольфрам',     ru_roditelny='вольфрама',   stable_a=[180]),
    Isotope(X='Re', Z=75, ru='рений',        ru_roditelny='рения',       stable_a=[]),
    Isotope(X='Os', Z=76, ru='осмий',        ru_roditelny='осмия',       stable_a=[]),
    Isotope(X='Ir', Z=77, ru='иридий',       ru_roditelny='иридия',      stable_a=[]),
    Isotope(X='Pt', Z=78, ru='платина',      ru_roditelny='платины',     stable_a=[188, 190, 191, 192, 193, 194, 195, 196, 198, 202]),
    Isotope(X='Au', Z=79, ru='золото',       ru_roditelny='золота',      stable_a=[]),
    Isotope(X='Hg', Z=80, ru='ртуть',        ru_roditelny='ртути',       stable_a=[]),
    Isotope(X='Tl', Z=81, ru='таллий',       ru_roditelny='таллия',      stable_a=[]),
    Isotope(X='Pb', Z=82, ru='свинец',       ru_roditelny='свинца',      stable_a=[202, 203, 204, 205, 206, 207, 208, 210], upper_a=214),
    Isotope(X='Bi', Z=83, ru='висмут',       ru_roditelny='висмута',     stable_a=[205, 206, 207, 209, 210], upper_a=214),
    Isotope(X='Po', Z=84, ru='полоний',      ru_roditelny='полония',     stable_a=[206, 208, 209, 210], upper_a=218),
    Isotope(X='At', Z=85, ru='астат',        ru_roditelny='астата',      stable_a=[]),
    Isotope(X='Rn', Z=86, ru='радон',        ru_roditelny='радона',      stable_a=[222]),
    Isotope(X='Fr', Z=87, ru='франций',      ru_roditelny='франция',     stable_a=[]),
    Isotope(X='Ra', Z=88, ru='радий',        ru_roditelny='радия',       stable_a=[223, 224, 225, 226, 228]),
    Isotope(X='Ac', Z=89, ru='актиний',      ru_roditelny='актиния',     stable_a=[]),
    Isotope(X='Th', Z=90, ru='торий',        ru_roditelny='тория',       stable_a=[227, 228, 229, 230, 231, 232, 234]),
    Isotope(X='Pa', Z=91, ru='протактиний',  ru_roditelny='протактиния', stable_a=[229, 230, 231, 232, 233], upper_a=234),
    Isotope(X='U',  Z=92, ru='уран',         ru_roditelny='урана',       stable_a=[234, 235, 238]),
    Isotope(X='Am', Z=95, ru='амерций',      ru_roditelny='амерция',     stable_a=[240, 241, 243]),
    Isotope(X='Bk', Z=97, ru='берклий',      ru_roditelny='берклия',     stable_a=[245, 246, 247, 248, 249]),
    Isotope(X='Np', Z=93, ru='нептуний',     ru_roditelny='нептуния',    stable_a=[]),
    Isotope(X='Pu', Z=94, ru='плутоний',     ru_roditelny='плутония',    stable_a=[236, 237, 238, 239, 240, 241, 242, 244, 246, 247]),
    Isotope(X='Cm', Z=96, ru='кюрий',        ru_roditelny='кюрия',       stable_a=[]),
    Isotope(X='Cf', Z=98, ru='калифорний',   ru_roditelny='калифорния',  stable_a=[]),
    Isotope(X='Es', Z=99, ru='эйнштейний',   ru_roditelny='эйнштейния',  stable_a=[]),
    Isotope(X='Fm', Z=100, ru='фермий',      ru_roditelny='фермия',      stable_a=[]),
    Isotope(X='Md', Z=101, ru='менделевий',  ru_roditelny='менделевия',  stable_a=[]),
    Isotope(X='No', Z=102, ru='нобелий',     ru_roditelny='нобелия',     stable_a=[]),
    Isotope(X='Lr', Z=103, ru='лоуренсий',   ru_roditelny='лоуренсия',   stable_a=[]),
    Isotope(X='Rf', Z=104, ru='резерфордий', ru_roditelny='резерфордия', stable_a=[]),
    Isotope(X='Db', Z=105, ru='дубний',      ru_roditelny='дубния',      stable_a=[]),
    Isotope(X='Sg', Z=106, ru='сиборгий',    ru_roditelny='сиборгия',    stable_a=[]),
    Isotope(X='Bh', Z=107, ru='борий',       ru_roditelny='бория',       stable_a=[]),
    Isotope(X='Hs', Z=108, ru='хассий',      ru_roditelny='хассия',      stable_a=[]),
    Isotope(X='Mt', Z=109, ru='мейтнерий',   ru_roditelny='мейтнерия',   stable_a=[]),
    Isotope(X='Ds', Z=110, ru='дармштадтий', ru_roditelny='дармштадтия', stable_a=[]),
    Isotope(X='Rg', Z=111, ru='рентгений',   ru_roditelny='рентгения',   stable_a=[]),
    Isotope(X='Cn', Z=112, ru='коперниций',  ru_roditelny='коперниция',  stable_a=[]),
    Isotope(X='Nh', Z=113, ru='нихоний',     ru_roditelny='нихония',     stable_a=[]),
    Isotope(X='Fl', Z=114, ru='флеровий',    ru_roditelny='флеровия',    stable_a=[]),
    Isotope(X='Mc', Z=115, ru='московий',    ru_roditelny='московия',    stable_a=[]),
    Isotope(X='Lv', Z=116, ru='ливерморий',  ru_roditelny='ливермория',  stable_a=[]),
    Isotope(X='Ts', Z=117, ru='теннессин',   ru_roditelny='теннессина',  stable_a=[]),
    Isotope(X='Og', Z=118, ru='оганесон',    ru_roditelny='оганесона',   stable_a=[]),
]


IsotopeByZ = {isotope.Z: isotope for isotope in Isotopes}


class FallType:
    Alpha = '\\alpha'
    Beta = '\\beta'
    BetaMinus = '\\beta^-'
    BetaPlus = '\\beta^+'


class Element:
    def __init__(self, Z=None, A=None, X=None, ru=None, ru_roditelny=None):
        assert isinstance(A, int)
        assert isinstance(Z, int)
        assert isinstance(X, str)
        assert isinstance(ru, str)
        assert isinstance(ru_roditelny, str)

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
            self._ru = ru
            self._ru_roditel = ru_roditelny
            self._X = X

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
        return IsotopeByZ[self._Z - 2].GetOne(self._A - 4)

    def beta_minus(self):
        return IsotopeByZ[self._Z + 1].GetOne(self._A)

    def beta_plus(self):
        return IsotopeByZ[self._Z - 1].GetOne(self._A)

    def beta(self):
        return self.beta_minus()

    def fall(self, fall):
        if fall == FallType.BetaMinus or fall == FallType.Beta:
            return self.beta_minus()
        elif fall == FallType.BetaPlus:
            return self.beta_plus()
        elif fall == FallType.Alpha:
            return self.alpha()
        else:
            raise RuntimeError(f'Invalid fall: {fall}')

    def get_reaction(self, fall):
        if fall == FallType.BetaMinus or fall == FallType.Beta:
            addenda = 'e^- + \\tilde\\nu_e'
        elif fall == FallType.BetaPlus:
            addenda = 'e^+ + \\nu_e'
        elif fall == FallType.Alpha:
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


class LoadedElements:
    def __init__(self, isotopes: List[Isotope], only_stable: bool):
        self._za_map = {}
        self._rua_map = {}
        self._list = []

        for isotope in isotopes:
            if only_stable:
                elements = isotope.GetStable()
            else:
                elements = isotope.GetAll()

            for element in elements:
                self._za_map[(element._Z, element._A)] = element
                self._rua_map[(element._ru, element._A)] = element
                self._list.append(element)

    def get_by_z_a(self, z=None, a=None):
        return self._za_map[(z, a)]

    def get_by_ru_a(self, ru=None, a=None):
        return self._rua_map[(ru, a)]


AllElements = LoadedElements(isotopes=Isotopes, only_stable=False)
AllElementsList = list(AllElements._list)

StableElements = LoadedElements(isotopes=Isotopes, only_stable=True)
StableElementsList = list(StableElements._list)
