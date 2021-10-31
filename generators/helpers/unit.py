from decimal import Decimal
import logging
log = logging.getLogger(__name__)


SI_PREFIXES = [
    ('к', 3),
    ('М', 6),
    ('Г', 9),
    ('м', -3),
    ('мк', -6),
    ('н', -9),
    ('п', -12),
    ('с', -2),
    ('д', -1),
]


class BaseUnit:
    def __init__(self, name, full_name, order):
        assert isinstance(name, str)
        assert isinstance(full_name, str)
        assert isinstance(order, int)
        self._name = name
        self._full_name = full_name
        self._order = order

    def __str__(self):
        return self._full_name

    def __repr__(self):
        return self._full_name

    def __lt__(self, other):
        return self._order < other._order



class BaseUnits:
    kg = BaseUnit('кг', 'килограмм', 1)
    s = BaseUnit('с', 'секунда', 2)
    m = BaseUnit('м', 'метр', 3)
    mol = BaseUnit('моль', 'моль', 4)
    A = BaseUnit('А', 'ампер', 5)
    K = BaseUnit('К', 'кельвин', 6)
    cd = BaseUnit('кд', 'кандела', 7)


ALL_SIMPLE_UNITS = []


class SimpleUnit:
    def __init__(self, full_name, short_name, en_name, base_units):
        assert isinstance(full_name, str)
        assert isinstance(short_name, str)
        assert isinstance(en_name, str)
        assert isinstance(base_units, dict)
        self._full_name = full_name
        self._short_name = short_name
        self._en_name = en_name
        self._base_units = base_units
        ALL_SIMPLE_UNITS.append(self)

    def __str__(self):
        return self._full_name

    def __repr__(self):
        return self._full_name


class SimpleUnits:
    # base units
    kg = SimpleUnit('килограмм', 'кг', 'kg', {BaseUnits.kg: 1})
    s = SimpleUnit('секунда', 'с', 's', {BaseUnits.s: 1})
    m = SimpleUnit('метр', 'м', 'm', {BaseUnits.m: 1})
    mol = SimpleUnit('моль', 'моль', 'mol', {BaseUnits.mol: 1})
    A = SimpleUnit('ампер', 'А', 'A', {BaseUnits.A: 1})
    K = SimpleUnit('кельвин', 'К', 'K', {BaseUnits.K: 1})
    cd = SimpleUnit('кандела', 'кд', 'cd', {BaseUnits.cd: 1})

    # for numbers without units in SI
    no_units = SimpleUnit('', '', '', {})

    # see https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5_%D0%B5%D0%B4%D0%B8%D0%BD%D0%B8%D1%86%D1%8B_%D0%A1%D0%98
    radian = SimpleUnit('радиан', 'рад', 'rad', {})
    steradian = SimpleUnit('стерадиан', 'ср', 'sr', {})
    degree_celsius = SimpleUnit('градус Цельсия', '°C', '°C', {BaseUnits.K: 1})
    hertz = SimpleUnit('герц', 'Гц', 'Hz', {BaseUnits.s: -1})
    newton = SimpleUnit('ньютон', 'Н', 'N', {BaseUnits.kg: 1, BaseUnits.m: 1, BaseUnits.s: -2})
    joule = SimpleUnit('джоуль', 'Дж', 'J', {BaseUnits.kg: 1, BaseUnits.m: 2, BaseUnits.s: -2})
    watt = SimpleUnit('ватт', 'Вт', 'W', {BaseUnits.kg: 1, BaseUnits.m: 2, BaseUnits.s: -3})
    pascal = SimpleUnit('паскаль', 'Па', 'Pa', {BaseUnits.kg: 1, BaseUnits.m: -1, BaseUnits.s: -2})
    lumen = SimpleUnit('люмен', 'лм', 'lm', {BaseUnits.cd: 1})
    lux = SimpleUnit('люкс', 'лк', 'lx', {BaseUnits.cd: 1, BaseUnits.m: -2})
    coulomb = SimpleUnit('кулон', 'Кл', 'C', {BaseUnits.A: 1, BaseUnits.s: 1})
    volt = SimpleUnit('вольт', 'В', 'V', {BaseUnits.kg: 1, BaseUnits.m: 2, BaseUnits.s: -3, BaseUnits.A: -1})
    ohm = SimpleUnit('ом', 'Ом', 'Ω', {BaseUnits.kg: 1, BaseUnits.m: 2, BaseUnits.s: -3, BaseUnits.A: -2})
    farad = SimpleUnit('фарад', 'Ф', 'F', {BaseUnits.s: 4, BaseUnits.A: 2, BaseUnits.kg: -1, BaseUnits.m: -2})
    weber = SimpleUnit('вебер', 'Вб', 'Wb', {BaseUnits.kg: 1, BaseUnits.m: 2, BaseUnits.s: -2, BaseUnits.A: -2})
    tesla = SimpleUnit('тесла', 'Тл', 'T', {BaseUnits.kg: 1, BaseUnits.s: -2, BaseUnits.A: -1})
    henry = SimpleUnit('генри', 'Гн', 'H', {BaseUnits.kg: 1, BaseUnits.m: 2, BaseUnits.s: -2, BaseUnits.A: -2})
    siemens = SimpleUnit('сименс', 'См', 'S', {BaseUnits.kg: -1, BaseUnits.m: -2, BaseUnits.s: 3, BaseUnits.A: 2})

    becquerel = SimpleUnit('беккерель', 'Бк', 'Bq', {BaseUnits.s: -1})
    gray = SimpleUnit('грей', 'Гр', 'Gy', {BaseUnits.m: 2, BaseUnits.s: -2})
    sievert = SimpleUnit('зиверт', 'Зв', 'Sv', {BaseUnits.m: 2, BaseUnits.s: -2})


def get_simple_unit(base_units):
    assert isinstance(base_units, dict)
    search = {key: value for key, value in base_units.items() if value != 0}
    for simple_unit in ALL_SIMPLE_UNITS:
        if simple_unit._base_units == search:
            return simple_unit
    return None


# TODO: desirable
def test_value():
    Value('10 г') + Value('5 см^3') * Value('2000 кг / м^3') == Value('20 г')


def get_known_units():
    units = ALL_SIMPLE_UNITS + [
        ('минут', 60, SimpleUnits.s),
        ('мин', 60, SimpleUnits.s),

        ('час', 3600, SimpleUnits.s),
        ('часов', 3600, SimpleUnits.s),
        ('часа', 3600, SimpleUnits.s),

        ('сут', 86400, SimpleUnits.s),
        ('суток', 86400, SimpleUnits.s),
        ('дня', 86400, SimpleUnits.s),
        ('дней', 86400, SimpleUnits.s),
        ('день', 86400, SimpleUnits.s),

        ('атм', 100000, SimpleUnits.pascal),
        ('эВ', Decimal('1.60e-19'), SimpleUnits.joule),  # электронвольт
        ('С', 1, SimpleUnits.degree_celsius),   # цельсий
        ('C', 1, SimpleUnits.degree_celsius),   # celsium
        ('K', 1, SimpleUnits.K),   # kelvin
        ('г', Decimal('0.001'), SimpleUnits.kg),   # грам
        ('т', 1000, SimpleUnits.kg),   # тонна
        ('ц', 100, SimpleUnits.kg),   # центнер
        ('а.е.м.', Decimal('1.66054e-27'), SimpleUnits.kg)
    ]

    known_units = {}
    for row in units:
        if isinstance(row, SimpleUnit):
            unit, multiplier, simple_unit = row._short_name, 1, row
        else:
            unit, multiplier, simple_unit = row[0], row[1], row[2]


        prefixes = [('', 0)]
        if unit == 'эВ':
            prefixes.extend(SI_PREFIXES)
        elif unit == 'г':
            prefixes.extend([p for p in SI_PREFIXES if p[1] <= -3])
        elif isinstance(row, SimpleUnit) and unit != 'кг':
            prefixes.extend(SI_PREFIXES)

        for si_prefix, si_power in prefixes:
            if unit:
                if unit == 'кг' and si_prefix != '':
                    pass
                elif unit == 'г' and si_prefix == 'к':
                    pass
                else:
                    if (si_prefix + unit) in known_units:
                        raise RuntimeError(f'Already found {si_prefix} {unit}: {known_units[si_prefix + unit]}')
                    known_units[si_prefix + unit] = (multiplier, simple_unit, si_prefix, si_power)

    return known_units


KNOWN_UNITS = get_known_units()


class OneUnit:
    def __init__(self, line, is_numenator):
        self._line = line
        self.IsNumerator = is_numenator

        self._exponent = 0
        self.simple_unit = SimpleUnits.no_units
        self._Multiplier = 1

        try:
            self._load_from_str(line)
        except:
            log.error(f'Error in _load_from_str on {line}')
            raise

        assert isinstance(self.HumanUnit, str)
        assert isinstance(self.HumanPower, int)
        assert isinstance(self.IsNumerator, bool)
        assert isinstance(self.simple_unit, SimpleUnit)

    def __str__(self):
        return f'unit: {self._line} is_num: {self.IsNumerator}'

    def get_tex(self, human=True):
        if self._Multiplier == 1 or human:
            res = '\\text{%s}' % self.HumanUnit
            if self.HumanPower != 1:
                res += '^{%d}' % self.HumanPower
        else:
            res = '%d \\cdot \\text{%s}' % (self._Multiplier, self.HumanUnit)
            if self.HumanPower != 1:
                res = '\\cbr{%s}^{%d}' % (res, self.HumanPower)
        return res

    @property
    def SiPower(self):
        return self.HumanPower * self._exponent

    @property
    def SiMultiplier(self):
        return self.Multiplier * Decimal(10) ** self.SiPower

    @property
    def Multiplier(self):
        return Decimal(self._Multiplier) ** self.HumanPower

    def _load_from_str(self, line):
        if '^' in line:
            line, power = line.split('^')
            self.HumanPower = int(power)
        else:
            self.HumanPower = 1

        self.HumanUnit = line

        if line in KNOWN_UNITS:
            multiplier, simple_unit, si_prefix, si_power = KNOWN_UNITS[line]
            self._exponent = si_power
            self.simple_unit = simple_unit
            self._Multiplier = multiplier


def test_one_unit():
    data = [
        ('г', 0, 'г', 1, SimpleUnits.kg),
        ('мг', -3, 'мг', 1, SimpleUnits.kg),
        ('кг', 0, 'кг', 1, SimpleUnits.kg),
        ('а.е.м.', 0, 'а.е.м.', 1, SimpleUnits.kg),
        ('мВ', -3, 'мВ', 1, SimpleUnits.volt),
        ('мВт', -3, 'мВт', 1, SimpleUnits.watt),
        ('МэВ', 6, 'МэВ', 1, SimpleUnits.joule),
        ('мс^2', -6, 'мс', 2, SimpleUnits.s),
        ('кг^2', 0, 'кг', 2, SimpleUnits.kg),
        ('мг^2', -6, 'мг', 2, SimpleUnits.kg),
        ('т', 0, 'т', 1, SimpleUnits.kg),
        ('сут', 0, 'сут', 1, SimpleUnits.s),
        ('ц^2', 0, 'ц', 2, SimpleUnits.kg),
        ('Гр', 0, 'Гр', 1, SimpleUnits.gray),
    ]
    for unit_text, si_power, human_unit, human_power, simple_unit in data:
        unit = OneUnit(unit_text, True)
        assert unit.SiPower == si_power, f'Expected SiPower {si_power}, got {unit.SiPower} for {unit!s}'
        assert unit.HumanUnit == human_unit, f'Expected HumanUnit {human_unit}, got {unit.HumanUnit} for {unit!s}'
        assert unit.HumanPower == human_power, f'Expected HumanPower {human_power}, got {unit.HumanPower} for {unit!s}'
        assert unit.simple_unit == simple_unit, f'Expected simple_unit {simple_unit}, got {unit.simple_unit} for {unit!s}'

    unit = OneUnit('мин^2', True)
    assert unit.Multiplier == 3600, f'Expected {3600}, got {unit.Multiplier}'
    assert unit.get_tex(human=True) == '\\text{мин}^{2}', f'Got {unit.get_tex(human=True)}'
    assert unit.get_tex(human=False) == '\\cbr{60 \\cdot \\text{мин}}^{2}', f'Got {unit.get_tex(human=False)}'

    assert 'ммг' not in KNOWN_UNITS
    assert 'кмг' not in KNOWN_UNITS
    assert 'мкг' in KNOWN_UNITS
    assert 'кц' not in KNOWN_UNITS


test_one_unit()
