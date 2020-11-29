class color:
    Green = 'green'
    Red = 'red'
    Cyan = 'cyan'
    Yellow = 'yellow'
    Blue = 'blue'
    Magenta = 'magenta'
    Black = 'black'
    White = 'white'


class ColorMessage:
    # https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    ResetTemplate = "\033[0m"
    ColorTemplate = "\033[1;%dm"
    BoldTemplate = "\033[1m"

    def __init__(self, enable=True):
        self._enable = enable
        self._known_colors = dict(zip([
            color.Black,
            color.Red,
            color.Green,
            color.Yellow,
            color.Blue,
            color.Magenta,
            color.Cyan,
            color.White,
        ], range(8)))

    def __call__(self, line, color=None, bold=False, bg=None):
        if self._enable:
            message = ''
            if color:
                message += self.ColorTemplate % (30 + self._known_colors[color.lower()])
            if bg:
                message = self.ColorTemplate % (40 + self._known_colors[bg.lower()])
            if bold:
                message = self.BoldTemplate
            message += str(line)
            if color or bg or bold:
            	message += self.ResetTemplate
            return message
        else:
            return line


def log_list(items, tab=4):
    return ''.join('\n' + ' ' * tab + '- ' + item for item in items)


cm = ColorMessage()
