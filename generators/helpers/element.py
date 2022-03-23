import library.files
from typing import List

import logging
log = logging.getLogger(__name__)

import attr


@attr.s
class Isotope:
    Z: int = attr.ib()
    X: str = attr.ib()
    ru: str = attr.ib()
    ru_roditelny: str = attr.ib()
    lower_a: int = attr.ib()
    upper_a: int = attr.ib()
    stable_a: List[int] = attr.ib()


@attr.s
class Element:
    Z: int = attr.ib()
    A: int = attr.ib()
    X: str = attr.ib()
    ru: str = attr.ib()
    ru_roditelny: str = attr.ib()
    is_stable: bool = attr.ib()

    @property
    def e(self) -> int:
        return self.Z

    @property
    def p(self) -> int:
        return self.Z

    @property
    def n(self) -> int:
        return self.A - self.Z

    def _get_ce(self) -> str:
        return f'\\ce{{^{{{self.A}}}_{{{self.Z}}}{{{self.X}}}}}'

    def _get_ru(self) -> str:
        return f'\\text{{{self.ru}-{self.A}}}'

    def _get_ru_name(self) -> str:
        return f'ядро {self.ru_roditelny} ${self._get_ce()}$'

    def __format__(self, fmt: str):
        try:
            fmt_parts = fmt.replace(':', '|').split('|')
            if len(fmt_parts) == 1:
                main_format = fmt_parts[0]
                if main_format == 'LaTeX':
                    return self._get_ce()
                elif main_format == 'RuText':
                    return self._get_ru()
                elif main_format == 'RuName':
                    return self._get_ru_name()
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


class AllElementsClass:
    def __init__(self, isotopes_cfg_file: str):
        self._z_a_map = {}
        for kws in isotopes_cfg_file:
            isotope = Isotope(**kws)
            for a in range(isotope.lower_a, isotope.upper_a + 1):
                element = Element(
                    Z=isotope.Z,
                    A=a,
                    X=isotope.X,
                    ru=isotope.ru,
                    ru_roditelny=isotope.ru_roditelny,
                    is_stable=a in isotope.stable_a,
                )
                assert 1 <= element.Z <= element.A
                # D and T will overwrite H-2 and H-3 here
                self._z_a_map[(element.Z, element.A)] = element

        self._elements = []
        self._stable_elements = []
        self._rua_map = {}
        for (z, a), element in sorted(self._z_a_map.items()):
            self._rua_map[(element.ru, element.A)] = element
            self._elements.append(element)
            if element.is_stable:
                self._stable_elements.append(element)

    def get_by_z_a(self, z: int=None, a: int=None) -> Element:
        return self._z_a_map[(z, a)]

    def get_by_ru_a(self, ru: str=None, a: int=None) -> Element:
        return self._rua_map[(ru, a)]

    @property
    def all_elements(self) -> List[Element]:
        return self._elements

    @property
    def stable_elements(self) -> List[Element]:
        return self._stable_elements


# config generated from url
# https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2
# https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2

AllElements = AllElementsClass(library.files.load_yaml_data('isotopes.yaml'))

assert len(AllElements.all_elements) == 3338, len(AllElements.all_elements)
assert AllElements.get_by_z_a(1, 3) == Element(Z=1, A=3, X='T', ru='тритий', ru_roditelny='трития', is_stable=True)


class FallHandler:
    Alpha = '\\alpha'
    Beta = '\\beta'
    BetaMinus = '\\beta^-'
    BetaPlus = '\\beta^+'

    def fall(self, element: Element, fall: str) -> Element:
        if fall == self.BetaMinus or fall == self.Beta:
            dZ, dA = 1, 0
        elif fall == self.BetaPlus:
            dZ, dA = -1, 0
        elif fall == self.Alpha:
            dZ, dA = -2, -4
        else:
            raise RuntimeError(f'Invalid fall: {fall}')

        return AllElements.get_by_z_a(element.Z + dZ, element.A + dA)

    def get_reaction(self, element: Element, fall: str) -> str:
        if fall == self.BetaMinus or fall == self.Beta:
            addenda = 'e^- + \\tilde\\nu_e'
        elif fall == self.BetaPlus:
            addenda = 'e^+ + \\nu_e'
        elif fall == self.Alpha:
            addenda = '\\ce{^4_2{He}}'
        else:
            raise RuntimeError(f'Invalid fall: {fall}')

        result = self.fall(element, fall)
        return f'{element:LaTeX} \\to {result:LaTeX} + {addenda}'


FallType = FallHandler()
