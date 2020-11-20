import collections


class Question(object):
    def __init__(self, index, text, polarity):
        self.Index = index
        self.Text = text
        assert polarity in ['+', '-']
        self.Polarity = polarity
        self.Reset()

        self.__AnswerMapping = {
            1: 'Неверно',
            2: 'Скорее неверно',
            3: 'Затрудняюсь ответить',
            4: 'Скорее вeрно',
            5: 'Beрно',
        }

    def AddAnswer(self, answerIndex):
        self.Answers[answerIndex] += 1

    def Reset(self):
        self.Answers = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    def GetTotalCount(self):
        return sum(self.Answers.values())

    def GetText(self):
        result = []
        totalCount = self.GetTotalCount()
        result.append('  * %s' % self.Text)
        for answerIndex in [5, 4, 3, 2, 1]:
            result.append('%30s: |%s%s| %3d%% %5d' % (
                self.__AnswerMapping[answerIndex],
                '=' * self.Answers[answerIndex], ' ' * (totalCount - self.Answers[answerIndex]),
                100. * self.Answers[answerIndex] / totalCount,
                self.Answers[answerIndex],
            ))
        result.append('%60s:   %3d%%' % ('Положительные ответы', self.GetRating()))
        result.append('%60s:   %.1f' % ('Средний балл', self.GetMean()))
        result.append('')
        return '\n'.join(result)

    def GetTex(self):
        totalCount = self.GetTotalCount()
        result = [
            r'{{\bfseries {}}}'.format(self.Text),
            '',
            '\\begin{tikzpicture}',
        ]
        y = 0
        dy = -0.500001
        colors = ['green', 'lime', 'orange', 'pink', 'red']
        if self.Polarity == '-':
            colors = colors[::-1]
        for answerIndex, color in zip([5, 4, 3, 2, 1], colors):
            rating = 100. * self.Answers[answerIndex] / totalCount
            result.extend([
                r'\node [left] at (0,%.1f) {%s};' % (y, self.__AnswerMapping[answerIndex]),
                r'\node [left] at (1,%.1f) {%d\%%};' % (y, rating),
                r'\draw [%s, line width=6] (1,%.1f) -- (%.2f,%.1f);' % (color, y, 1. + 2 * rating / 100, y),
                r'\node [right] at (3,%.1f) {%d};' % (y, self.Answers[answerIndex]),
            ])
            y += dy
        y += dy / 2
        result.extend([
            r'\node [left] at (2.5,%.1f) {Положительные ответы:};' % y,
            r'\node at (3,%.1f) {%d\%%};' % (y, self.GetRating()),
            r'\node [left] at (2.5,%.1f) {Средний балл:};' % (y + dy),
            r'\node at (3,%.1f) {%.1f};' % (y + dy, self.GetMean()),
        ])

        result.append('\\end{tikzpicture}')
        result.append('')
        return '\n'.join(result)

    def GetMean(self):
        valuesSum = 0.
        valuesTotal = 0.
        for key, value in self.Answers.items():
            valuesSum += key * value
            valuesTotal += value
        result = valuesSum / valuesTotal
        if self.Polarity == '-':
            result = 6. - result
        return result

    def GetRating(self):
        positiveSum = 0
        for key, value in self.Answers.items():
            if (self.Polarity == '+' and key >= 4) or (self.Polarity == '-' and key <= 2):
                positiveSum += value
        return int(100. * positiveSum / self.GetTotalCount())


def mean(items):
    items = list(items)
    return sum(items) / len(items)


class Dimension(object):
    def __init__(self, name, questions):
        self.Name = name
        self.Questions = questions
        self.Reset()

    def Reset(self):
        for question in self.Questions:
            question.Reset()

    def GetRating(self):
        return mean(question.GetRating() for question in self.Questions)

    def GetText(self):
        result = [
            '%-30s Среднее значение: %3d%%' % (self.Name, self.GetRating()),
        ]
        for question in self.Questions:
            result.append(question.GetText())
        result.append('\n')
        return '\n'.join(result)

    def GetTex(self):
        result = [
            r'\section{%s $\rightarrow$ %d\%%}' % (self.Name, self.GetRating()),
            ''
        ]
        for question in self.Questions:
            result.append(question.GetTex())
        result.append('\n\\columnbreak\n')
        return '\n'.join(result)


class Report(object):
    def __init__(self, className, dimensions):
        self.ClassName = className
        self.Dimensions = dimensions
        self.Indicies = {}
        for dimensionIndex, dimension in enumerate(self.Dimensions):
            for questionIndex, question in enumerate(dimension.Questions):
                self.Indicies[question.Index] = (dimensionIndex, questionIndex)

    def Reset(self):
        for dimension in self.Dimensions:
            dimension.Reset()

    def AddAnswer(self, questionIndex, answer):
        dimensionIndex, questionIndex = self.Indicies[questionIndex]
        self.Dimensions[dimensionIndex].Questions[questionIndex].AddAnswer(answer)

    def GetRating(self):
        return mean(dimension.GetRating() for dimension in self.Dimensions)

    def GetText(self):
        result = [
            'Класс: %s' % self.ClassName,
            'Общий результат: %3d%%' % self.GetRating(),
            '',
        ]
        for dimension in self.Dimensions:
            result.append(dimension.GetText())
        result.append('')
        return '\n'.join(result)

    def GetTex(self):
        return r'''
\newcommand\rootpath{{../..}}
\input{{\rootpath/school-554/main}}
\begin{{document}}

{{\bfseries Отчёт «Трипод» для класса {self.ClassName}}}

Общий результат: {rating}\%

\columnsep=30pt
\begin{{multicols*}}{{2}}
    {dimensions}
\end{{multicols*}}

\end{{document}}
        
        '''.strip().format(
            self=self,
            dimensions='\n\n'.join(dimension.GetTex() for dimension in self.Dimensions),
            rating=int(self.GetRating()),
        )


def getEmptyReport(className):
    report = Report(className, [
        Dimension('Поддержка', [
            Question(7, 'Мне кажется, что этому учителю действительно важны мои успехи', '+'),
            Question(20, 'Этот учитель искренне пытается понять, как мы относимся к тем или иным вещам.', '+'),
            Question(27, 'Мне кажется, что этот учитель замечает, если меня что-то беспокоит', '+'),
        ]),
        Dimension('Вовлечение', [
            Question(2, 'Мы можем выбирать, каким образом изучать материал на уроках этого учителя', '+'),
            Question(3, 'Этот учитель хочет, чтобы мы делились своими мыслями', '+'),
            Question(13, 'Учитель хочет, чтобы я объяснял свои ответы - почему я так думаю', '+'),
            Question(29, 'Этот учитель уважает мои идеи и предложения', '+'),
            Question(33, 'Этот учитель дает нам возможность объяснить свои мысли', '+'),
            Question(35, 'Мы открыто обсуждаем с учителем нашу работу в классе: что было интересно и понятно, а что не очень', '+'),
        ]),
        Dimension('Интерес', [
            Question(1, 'Мне нравится на уроках этого учителя', '+'),
            Question(10, 'С этим учителем приятно учиться', '+'),
            Question(22, 'Этот учитель делает уроки интересными', '+'),
            Question(24, 'На уроках этого учителя мое внимание рассеивается, и мне становится скучно', '-'),
        ]),
        Dimension('Объяснение', [
            Question(4, 'Во время урока учитель спрашивает, успеваем ли мы за ходом урока', '+'),
            Question(8, 'Этот учитель знает, когда наш класс его НЕ понимает', '+'),
            Question(9, 'Если мы чего-то НЕ понимаем, учитель объясняет по-другому', '+'),
            Question(14, 'Этот учитель может по-разному объяснить любую тему, которую мы проходим на уроке', '+'),
            Question(17, 'Когда учитель объясняет материал, он думает, что мы понимаем, хотя на самом деле мы НЕ понимаем', '-'),
            Question(28, 'Этот учитель проверяет, понимаем ли мы его объяснения', '+'),
            Question(31, 'Этот учитель понятно объясняет даже сложный материал', '+'),
            Question(34, 'На уроках этого учителя мы учимся исправлять собственные ошибки', '+'),
        ]),
        Dimension('Закрепление', [
            Question(15, 'Комментарии этого учителя к работе, которую я выполняю, помогают мне понять, как можно сделать эту работу лучше', '+'),
            Question(18, 'Учитель дает полезные пояснения, чтобы мы поняли, что сделали не так в задании', '+'),
            Question(25, 'Этот учитель каждый раз подводит итог тому, что мы прошли на уроке', '+'),
        ]),
        Dimension('Требовательность', [
            Question(5, 'Этот учитель просит наш класс подробнее и глубже объяснять свои ответы', '+'),
            Question(12, 'Когда мы изучаем сложный материл, учитель поддерживает нас и не дает нам сдаваться', '+'),
            Question(26, 'Мы узнаем много нового почти на каждом уроке этого учителя', '+'),
            Question(32, 'На уроках наш учитель требует полной самоотдачи', '+'),
        ]),
        Dimension('Управление классом', [
            Question(6, 'На уроках этого учителя наш класс все время работает и не теряет времени', '+'),
            Question(11, 'Наш класс относится к учителю с уважением', '+'),
            Question(16, 'На уроках этого учителя наш класс ведет себя плохо', '-'),
            Question(19, 'На уроках этого учителя наш класс ведет себя хорошо', '+'),
            Question(21, 'Мне НЕ нравится, как наш класс ведет себя на уроках этого учителя', '-'),
            Question(23, 'Наш класс слушается этого учителя', '+'),
            Question(30, 'Поведение нашего класса злит учителя', '-'),
        ]),
    ])
    report.Reset()
    return report
