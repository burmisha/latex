import re

class ProperAnswer:
    EN_TO_RU_MAPPING = {
        'A': 'А', 'a': 'а',
        'B': 'В',
        'C': 'С', 'c': 'с',
        'E': 'Е', 'e': 'е',
        'H': 'Н',
        'K': 'К',
        'M': 'М',
        'O': 'O', 'o': 'о',
        'P': 'Р', 'p': 'р',
        'T': 'Т',
        'X': 'Х', 'x': 'х',
    }

    def __init__(self, answer, value=None):
        assert isinstance(value, (int, float)), f'Invalid value: {value}'
        assert isinstance(answer, (int, str))
        self._value = value
        self.__re = str(answer)

    def _format_re(self, canonic_re):
        result = str(canonic_re).strip()
        result = result.replace(' ', r'\s*')
        result = re.sub(r'([0-9][\.,][0-9])0+\b', r'\1', result)
        result = re.sub(r'([0-9])[,\.]([0-9])', r'\1[,\.]\2', result)
        assert not result.startswith(r'^[\s.;,]*')
        assert not result.endswith(r'[\s.;,]*$')
        result = f'^{result}$'
        return result

    def Printable(self):
        return str(self.__re)

    def Value(self):
        return self._value

    def _en_to_ru(self, value):
        res = str(value)
        for eng, rus in self.EN_TO_RU_MAPPING.items():
            res = res.replace(eng, rus)
        return res

    def IsOk(self, value):
        value = re.sub(r'([0-9][\.,][0-9])0+\b', r'\1', value)
        regexp = self._format_re(self.__re)
        if re.match(self._en_to_ru(regexp), self._en_to_ru(value)):
            return True

        return False


assert ProperAnswer('0.20', 1).IsOk('0.2')
# assert ProperAnswer('0.20', 1).__re == '0.20'
assert ProperAnswer('0.20', 1).IsOk('0,2')
assert ProperAnswer('20', 1).IsOk('20')
assert not ProperAnswer('20', 1).IsOk('200')
assert not ProperAnswer('200', 1).IsOk('20')
assert not ProperAnswer('0.20', 1).IsOk('0,21')
assert ProperAnswer('0.20', 1).IsOk('0,20')

