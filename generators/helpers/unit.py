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


class OneUnit:
    def __init__(self, line, is_numenator):
        si_unit, si_power, human_unit, human_power = self._parse_line(line)
        self.SiUnit = si_unit
        self.SiPower = si_power
        self.HumanUnit = human_unit
        self.HumanPower = human_power
        self.IsNumerator = is_numenator
        assert isinstance(self.SiUnit, str)
        assert isinstance(self.SiPower, int)
        assert isinstance(self.HumanUnit, str)
        assert isinstance(self.HumanPower, int)

    def get_tex(self):
        res = f'\\text{{{self.HumanUnit}}}'
        if self.HumanPower != 1:
            res += f'^{{{self.HumanPower}}}'
        return res

    def _parse_line(self, line):
        try:
            if '^' in line:
                line, power = line.split('^')
                power = int(power)
            else:
                power = 1

            prefix = ''
            main = line
            for suffix in [
                'час',
                'сут',
                'атм',
                'эВ',  # электрон-вольт
                'В',   # вольт
                'Дж',  # джоуль
                'Н',   # ньютон
                'Вт',  # ватт
                'Ом',  # ом
                'Ф',   # фарад
                'А',   # ампер
                'Кл',  # кулон
                'кг',  # килограм
                'г',   # грам
                'с',   # секунда
                'м',   # метр
                'Тл',  # тесла
                'т',   # тонна
                'С',   # цельсий
                'C',   # celsium
                'К',   # кельвин
                'K',   # kelvin
                'моль',
            ]:
                if line.endswith(suffix):
                    main = suffix
                    prefix = line[:-len(suffix)]
                    break

            exponent = SI_PREFIXES[prefix]

            if main == 'г':
                main = 'кг'
                exponent -= 3
            # TODO: час, сутки

            return main, exponent * power, line, power
        except:
            log.error('Error in ParseItem on %r', line)
            raise


class BaseUnit:
    def __init__(self, name, full_name):
        self._name = name
        self._full_name = full_name


class BaseUnits:
    kg = BaseUnit('кг', 'килограм'),
    s = BaseUnit('с', 'секунда'),
    m = BaseUnit('м', 'метр'),
    mol = BaseUnit('моль', 'моль'),
    A = BaseUnit('А', 'ампер'),
    K = BaseUnit('К', 'кельвин'),
    cd = BaseUnit('кд', 'кандела'),


class SimpleUnit:
    def __init__(self, full_name, short_name, en_name, basic_units):
        self._full_name = full_name
        self._short_name = short_name
        self._en_name = en_name
        self._basic_units = basic_units


class SimpleUnits:
    # base units
    kg = SimpleUnit('килограм', 'кг', 'kg', {BaseUnits.kg: 1})
    s = SimpleUnit('секунда', 'с', 's', {BaseUnits.s: 1})
    m = SimpleUnit('метр', 'м', 'm', {BaseUnits.m: 1})
    mol = SimpleUnit('моль', 'моль', 'mol', {BaseUnits.mol: 1})
    A = SimpleUnit('ампер', 'А', 'A', {BaseUnits.A: 1})
    K = SimpleUnit('кельвин', 'К', 'K', {BaseUnits.K: 1})
    cd = SimpleUnit('кандела', 'кд', 'cd', {BaseUnits.cd: 1})

    # see https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5_%D0%B5%D0%B4%D0%B8%D0%BD%D0%B8%D1%86%D1%8B_%D0%A1%D0%98
    radian = SimpleUnit('радиан', 'рад', 'rad', [])
    steradian = SimpleUnit('стерадиан', 'ср', 'sr', [])
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


# TODO: desirable
def test_value():
    Value('10 г') + Value('5 см^3') * Value('2000 кг / м^3') == Value('20 г')
