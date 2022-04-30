import fnmatch


class FnFilter:
    def __init__(self, fn_filter: str):
        assert fn_filter, f'No filter provided: {fn_filter}'
        self.fn_filter = fn_filter

    def match(self, value):
        return fnmatch.fnmatch(value, self.fn_filter)
