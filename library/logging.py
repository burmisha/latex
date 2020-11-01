class ColorMessage:
    # https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    ResetTemplate = "\033[0m"
    ColorTemplate = "\033[1;%dm"
    BoldTemplate = "\033[1m"
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    def __init__(self, enable=True):
        self._enable = enable
        self._known_colors = {
            'green': self.GREEN,
            'red': self.RED,
            'cyan': self.CYAN,
            'yellow': self.YELLOW,
            'blue': self.BLUE,
            'magenta': self.MAGENTA,
            'black': self.BLACK,
            'white': self.WHITE,
        }

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


def log_list(items):
    return ''.join('\n    - ' + item for item in items)
