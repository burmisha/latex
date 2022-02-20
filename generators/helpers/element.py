import library.files
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
Isotopes = [Isotope(**kws) for kws in library.files.load_yaml_data('isotopes.yaml')]
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
