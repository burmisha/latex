class Node:
    def __mul__(self, count):
        return [self] * count


class Choice(Node):
    def __init__(self, options):
        self._options = options


class TextTask(Node):
    pass


class Text(Node):
    def __init__(self, text):
        self._text = text


assert len(Text('QWE') * 7) == 7
