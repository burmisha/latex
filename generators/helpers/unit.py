import logging
log = logging.getLogger(__name__)


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

            exponent = {
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
            }[prefix]

            if main == 'г':
                main = 'кг'
                exponent -= 3
            # TODO: час, сутки

            return main, exponent * power, line, power
        except:
            log.error('Error in ParseItem on %r', line)
            raise
