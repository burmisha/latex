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
    lower_a: int = attr.ib()
    upper_a: int = attr.ib()

    def GetOne(self, a: int):
        return Element(Z=self.Z, A=a, X=self.X, ru=self.ru, ru_roditelny=self.ru_roditelny, is_stable=a in self.stable_a)

    def GetAll(self):
        for a in range(self.lower_a, self.upper_a + 1):
            yield Element(Z=self.Z, A=a, X=self.X, ru=self.ru, ru_roditelny=self.ru_roditelny, is_stable=a in self.stable_a)

    def GetStable(self):
        for a in sorted(self.stable_a):
            yield Element(Z=self.Z, A=a, X=self.X, ru=self.ru, ru_roditelny=self.ru_roditelny, is_stable=True)


class FallType:
    Alpha = '\\alpha'
    Beta = '\\beta'
    BetaMinus = '\\beta^-'
    BetaPlus = '\\beta^+'


@attr.s
class Element:
    # TODO: add validators
    Z: int = attr.ib()
    A: int = attr.ib()
    X: str = attr.ib()
    ru: str = attr.ib()
    ru_roditelny: str = attr.ib()
    is_stable: bool = attr.ib()

    @property
    def e(self):
        return self.Z

    @property
    def p(self):
        return self.Z

    @property
    def n(self):
        return self.A - self.Z

    def get_ce(self):
        return f'\\ce{{^{{{self.A}}}_{{{self.Z}}}{{{self.X}}}}}'

    def get_ru(self):
        return f'\\text{{{self.ru}-{self.A}}}'

    def get_ru_name(self):
        return f'ядро {self.ru_roditel} ${self.get_ce()}$'

    def alpha(self):
        return ElementsByZA[(self.Z - 2, self.A - 4)]

    def beta_minus(self):
        return ElementsByZA[(self.Z + 1, self.A)]

    def beta_plus(self):
        return ElementsByZA[(self.Z - 1, self.A)]

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

# see urls and file to parse it
# https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2
# https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2
AllIsotopes = [Isotope(**kws) for kws in library.files.load_yaml_data('isotopes.yaml')]
ElementsByZA = {
    (element.Z, element.A): element
    for isotope in AllIsotopes
    for element in isotope.GetAll()
}

assert len(ElementsByZA) == 3338


class AllElementsClass:
    def __init__(self):
        self._rua_map = {}
        self._elements = []
        self._stable_elements = []

        for isotope in AllIsotopes:
            for element in isotope.GetAll():
                self._rua_map[(element.ru, element.A)] = element
                self._elements.append(element)
                if element.is_stable:
                    self._stable_elements.append(element)

    def get_by_z_a(self, z=None, a=None):
        return ElementsByZA[(z, a)]

    def get_by_ru_a(self, ru=None, a=None):
        return self._rua_map[(ru, a)]

    @property
    def all_elements(self):
        return self._elements

    @property
    def stable_elements(self):
        return self._stable_elements


AllElements = AllElementsClass()
