class Node:
    def __mul__(self, count):
        return [self] * count

    def __add__(self, other):
        if isinstance(other, list):
            assert all(isinstance(item, Node) for item in other)
            return [self] + other
        elif isinstance(other, Node):
            return [self, other]
        else:
            raise RuntimeError(f'Invalid {other} while adding to {self}')

    def __radd__(self, other):
        if isinstance(other, list):
            assert all(isinstance(item, Node) for item in other)
            return other + [self]
        elif isinstance(other, Node):
            return [other, self]
        else:
            raise RuntimeError(f'Invalid {other} while radding to {self}')


class Choice(Node):
    def __init__(self, options):
        self._options = options


class TextTask(Node):
    pass


class Text(Node):
    def __init__(self, text):
        self._text = text


abv_choices = Choice('АБВ')
text_task = TextTask()


assert len(Text('QWE') * 7) == 7
assert len(Text('12') + Text('123')) == 2
assert len(Text('12') * 2 + Text('123') * 3) == 5
