import library
import logging

log = logging.getLogger('task')


class Task(object):
    def __init__(self, text, answer=None, number=None, solutionSpace=120):
        self.Text = text.strip('\n')
        self.Answer = answer
        self.Number = number
        self.SolutionSpace = solutionSpace

    def Format(self, text, nodeType):
        try:
            value = library.formatter.formatText(text, addIndent=4)
            return u'''\\{}{{\n{}\n}}\n'''.format(nodeType, value).replace(r'\\u', r'\u')
        except Exception:
            log.exception('Failed to get LaTeX for %s on %r', nodeType, self.Text)
            raise

    def GetTex(self):
        result = self.Format(self.Text, 'task')
        if self.Answer:
            result += self.Format(self.Answer, 'answer')
        return result        

    def GetFilename(self):
        filename = '%s.tex' % self.Number
        log.debug('Got filename %r from %r', filename, self.Number)
        return filename

    def GetSolutionSpace(self):
        return self.SolutionSpace


class TasksGenerator(object):
    def __call__(self):
        raise NotImplementedError()
