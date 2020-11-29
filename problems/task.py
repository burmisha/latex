import library

import logging
log = logging.getLogger('task')

DEFAULT_SOLUTION_SPACE = 120

TASK_TEMPLATE = '''
\\{}{{%
{}
}}
'''


class Task(object):
    def __init__(self, text, answer=None, number=None, solutionSpace=None, test_answer=None):
        self.Text = text.strip('\n')
        self.Answer = answer
        self.Number = number
        self._solution_space = solutionSpace
        self._test_answer = test_answer

    def __Format(self, text, nodeType):
        try:
            value = library.formatter.formatText(text, addIndent=4)
            return TASK_TEMPLATE.format(nodeType, value).replace(r'\\u', r'\u').strip()
        except Exception:
            log.exception('Failed to get LaTeX for %s on %r', nodeType, self.Text)
            raise

    def GetTex(self, index=None, add_solution_space=False):
        lines = []

        if index:
            lines.append(f'\\tasknumber{{{index}}}%')

        lines.append(self.__Format(self.Text, 'task'))

        if self.Answer is not None:
            lines.append(self.__Format(self.Answer, 'answer'))

        if add_solution_space and self._solution_space:
            lines.append('\\solutionspace{%dpt}' % self._solution_space)

        return '\n'.join(lines)

    def GetFilename(self):
        filename = '%s.tex' % self.Number
        log.debug('Got filename %r from %r', filename, self.Number)
        return filename

    def GetTestAnswer(self):
        return self._test_answer


class TasksGenerator(object):
    def __call__(self):
        raise NotImplementedError()
