import logging
log = logging.getLogger(__name__)


SI_PREFIXES = {
    '': 0,
    'к': 3,
    'М': 6,
    'Г': 9,
    'м': -3,
    'мк': -6,
    'н': -9,
    'п': -12,
    'с': -2,
    'д': -1,
}


class BaseUnit:
    def __init__(self, name, full_name):
        assert isinstance(name, str)
        assert isinstance(full_name, str)
        self._name = name
        self._full_name = full_name

    def __str__(self):
        return self._full_name

    def __repr__(self):
        return self._full_name


class BaseUnits:
    kg = BaseUnit('кг', 'килограм'),
    s = BaseUnit('с', 'секунда'),
    m = BaseUnit('м', 'метр'),
    mol = BaseUnit('моль', 'моль'),
    A = BaseUnit('А', 'ампер'),
    K = BaseUnit('К', 'кельвин'),
    cd = BaseUnit('кд', 'кандела'),


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

    def __str__(self):
        return self._full_name

    def __repr__(self):
        return self._full_name


class SimpleUnits:
    # base units
    kg = SimpleUnit('килограм', 'кг', 'kg', {BaseUnits.kg: 1})
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
    hertz = SimpleUnit('герц', 'Гц', 'Hz', {BaseUnits.s: 1})
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


ALL_SIMPLE_UNITS = [
    SimpleUnits.kg,
    SimpleUnits.s,
    SimpleUnits.m,
    SimpleUnits.mol,
    SimpleUnits.A,
    SimpleUnits.K,
    SimpleUnits.cd,
    SimpleUnits.no_units,
    SimpleUnits.radian,
    SimpleUnits.steradian,
    SimpleUnits.degree_celsius,
    SimpleUnits.hertz,
    SimpleUnits.newton,
    SimpleUnits.joule,
    SimpleUnits.watt,
    SimpleUnits.pascal,
    SimpleUnits.lumen,
    SimpleUnits.lux,
    SimpleUnits.coulomb,
    SimpleUnits.volt,
    SimpleUnits.ohm,
    SimpleUnits.farad,
    SimpleUnits.weber,
    SimpleUnits.tesla,
    SimpleUnits.henry,
    SimpleUnits.siemens,
    SimpleUnits.becquerel,
    SimpleUnits.gray,
    SimpleUnits.sievert,
]


def get_simple_unit(base_units):
    assert isinstance(base_units, dict)
    for simple_unit in ALL_SIMPLE_UNITS:
        if simple_unit._base_units == base_units:
            return simple_unit
    raise RuntimeError(f'No simple units for {base_units}')


# TODO: desirable
def test_value():
    Value('10 г') + Value('5 см^3') * Value('2000 кг / м^3') == Value('20 г')




def get_known_units():
    units = [
        ('час', 3600, SimpleUnits.s),
        ('сут', 86400, SimpleUnits.s),
        ('атм', 100000, SimpleUnits.pascal),
        ('эВ', 1.6 * 10 ** -19, SimpleUnits.joule),  # электрон-вольт
        ('С', 1, SimpleUnits.degree_celsius),   # цельсий
        ('C', 1, SimpleUnits.degree_celsius),   # celsium
        ('К', 1, SimpleUnits.K),   # кельвин
        ('K', 1, SimpleUnits.K),   # kelvin
        SimpleUnits.volt,
        SimpleUnits.joule,
        SimpleUnits.newton,
        SimpleUnits.watt,
        SimpleUnits.ohm,
        SimpleUnits.farad,
        SimpleUnits.A,
        SimpleUnits.coulomb,
        SimpleUnits.kg,
        SimpleUnits.s,
        SimpleUnits.m,
        SimpleUnits.tesla,
        SimpleUnits.mol,
        SimpleUnits.henry,
        SimpleUnits.hertz,
        ('г', 1 / 1000, SimpleUnits.kg),   # грам
        ('т', 1000, SimpleUnits.kg),   # тонна
    ]
    for row in units:
        if isinstance(row, SimpleUnit):
            yield row._short_name, 1, row
        else:
            yield row


KNOWN_UNITS = list(get_known_units())


class OneUnit:
    def __init__(self, line, is_numenator):
        self._line = line
        try:
            self._load_from_str(line)
        except:
            log.error(f'Error in _load_from_str on {line}')
            raise
        self.IsNumerator = is_numenator
        assert isinstance(self.SiPower, int)
        assert isinstance(self.HumanUnit, str)
        assert isinstance(self.HumanPower, int)
        assert isinstance(self.IsNumerator, bool)
        assert isinstance(self.simple_unit, SimpleUnit)

    def get_tex(self):
        res = '\\text{%s}' % self.HumanUnit
        if self.HumanPower != 1:
            res += '^{%d}' % self.HumanPower
        return res

    def _load_from_str(self, line):
        if '^' in line:
            line, power = line.split('^')
            self.HumanPower = int(power)
        else:
            self.HumanPower = 1
        self.HumanUnit = line

        self.simple_unit = SimpleUnits.no_units
        exponent = 0
        main = line
        for unit, multiplier, simple_unit in KNOWN_UNITS:
            if line.endswith(unit):
                main = unit
                prefix = line[:-len(unit)]
                exponent = SI_PREFIXES[prefix]
                self.simple_unit = simple_unit
                break

        if main == 'г':
            main = 'кг'
            exponent -= 3
        # TODO: час, сутки

        self.SiPower = exponent * self.HumanPower


def test_one_unit():
    data = [
        ('мВ', -3, 'мВ', 1),
        ('мВт', -3, 'мВт', 1),
        ('МэВ', 6, 'МэВ', 1),
        ('мс^2', -6, 'мс', 2),
        ('кг^2', 0, 'кг', 2),
        ('мг^2', -12, 'мг', 2),
        ('т', 0, 'т', 1),
    ]
    for unit_text, si_power, human_unit, human_power in data:
        unit = OneUnit(unit_text, True)
        assert unit.SiPower == si_power, f'Expected {si_power}, got {unit.SiPower}'
        assert unit.HumanUnit == human_unit, f'Expected {human_unit}, got {unit.HumanUnit}'
        assert unit.HumanPower == human_power, f'Expected {human_power}, got {unit.HumanPower}'


test_one_unit()
