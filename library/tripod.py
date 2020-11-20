import library

import collections
import os


results = {
    '2019-05-7': [
        '2135313354135415 3513541452354533535',
        '4355424354345545 3514532455454232554',
        '4352412443234345 3414531555353433554',
        '2455313333144335 4314421543544423433',
        '5455515355344555 4413241354455344554',
        '3333333333333333 33333333333333_____',  # =(
        '5555555555555551 1555555155555153553',
        '4555134554345545 5415541554555443555',
        '5555455555555551 1555555155555254555',
        '5254222233222222 1212123454321234543',  # =(
        '5444414345144455 1414551145444244444',
        '4255434344334434 2422432344234333242',
        '4254234334334434 2523442344343332544',
        '45554_3454155435 3414_3_255141535543',
        '5335324555444543 3534353144334353545',
    ],
    '2019-05-8': [
        '5355314354145345 3515531355443133554',
        '3144514543144354 3412531342344_34443',
        '5255444555454552 154_5542_4345254542',
        '4444444444444442 2444244244444244444',
        '4245315355445434 2535544255543344543',
        '3243433234333233 4333432333333333333',
        '5455555455555552 1545255155555255555',
        '4455325455453554 2445553134435353555',
        '5444524234333434 4325552433333423325',
        '5355515555255555 1515552155555355555',
        '4444444444244444 4444442344444443442',
        '5555425445445554 2425552154445155554',
        '5454334454344344 352_441345444354455',
        '5553425555345554 1524354154444243555',
        '4355425455354355 1314442355345441545',
        '5555535355255544 45255_2455555355_55',
    ],
    '2019-05-11': [
        '5554534555455554 3544434424344132334',
        '5555555555554441 1555145145455154555',
        '4233343455433543 1535452234353152523',
        '3543214345554531 5445254534345345554',
        '5554443545544543 5444535344534533445',
        '4454343255545442 2444344224344243451',
        '5355423455555555 1534554145555253554',
        '5444345334445352 3443343233343243544',
        '255542455525535_ 2513551123454321234',  # =(
        '545542455525535_ 2513551123534143555',
        '4545545554255555 1515552145455453555',
        '4453433455535544 2424443234344342445',
        '5445514355444423 4425552352343334424',
        '455452414554_3_4 2553134352225322544',
        '4354324345544433 2435443343343332523',
        '5543234455443443 4544244223434142443',
        '5355335355335533 3535353355353355353',
    ],
    '2019-05-test': [
        '5435425142454452 333444553345__44553',
        '5445543542514242 454344455245__44552',
        '4354455435425351 55333444553345__445',
    ],
}


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


def getTripodReports():
    for className, personsResults in results.items():
        report = getEmptyReport(className)
        for personResult in personsResults:
            personResult = personResult.replace(' ', '').replace('-', '3').replace('_', '3')
            assert len(personResult) == 35
            for index, answer in enumerate(personResult, 1):
                report.AddAnswer(index, int(answer))
        yield className, report


def runTripod(args):
    fileWriter = library.files.FileWriter()
    tripodFormat = args.format
    getText, extension = {
        'tex': (lambda r: r.GetTex(), 'tex'),
        'txt': (lambda r: r.GetText(), 'txt'),
    }[tripodFormat]
    for className, report in library.tripod.getTripodReports():
        fileWriter.Write(os.path.join('school-554', 'tripod'), className + '-tripod.%s' % extension, text=getText(report))


def populate_parser(parser):
    parser.add_argument('--format', help='Format', choices=['tex', 'txt'])
    parser.set_defaults(func=runTripod)
