import random

from library.gform.node import Choice, TextTask, Text
from library.gform.form import GoogleForm


IMAGES = {
    'minions': 'https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif',
    'incredibles': 'https://media.giphy.com/media/G2fKgPMXJ40WA/giphy.gif',
    'insideout': 'https://media.giphy.com/media/dU6Ec1svWeWCk/giphy.gif',
    'tenet': 'https://media.giphy.com/media/jV0IaIdzPy7L1vqv5T/giphy.gif',
    'up': 'https://media.giphy.com/media/3sB5CjvsDbA6A/giphy.gif',
    'monsters': 'https://media.giphy.com/media/19ZCKSoEvSquk/giphy.gif',
    'zootopia': 'https://media.giphy.com/media/139Lo3rANXYt9K/giphy.gif',
    'minion-up': 'https://media.giphy.com/media/oobNzX5ICcRZC/giphy.gif',
    'ratatouille': 'https://media.giphy.com/media/5Wyv8urxxclm8/giphy.gif',
    'keanureeves': 'https://media.giphy.com/media/TJrS7r0f6SOthGTiPe/giphy.gif',
}

DEFAULT_GIF = 'minions'

UP_TO_STR_FMT = (
    'Отправить до {upTo} (напомню, что Гугл-формы сохраняют время отправки). '
    'И пожалуйста, проверьте, что выше верно указаны дата и класс '
    '(если нет — дайте знать как можно раньше). '
    '554 школа, Москва, 2020–2021 учебный год.'
)

THUMBS_UP_CHOICES = [
    'Спасибо, ты молодчина!',
    'Готово, всё сохранили!',
    'Принято, ответы записаны!',
]

CLOSE_TAB = 'Закрой вкладку, а то иногда отправляются дубли.'

INSTRUCTION = (
    'Рекомендуется сначала просмотреть форму ответов на этой странице, '
    'потом открыть задание и всё решить у себя в тетради, а лишь после заполнять форму. '
    'Так ответы не потеряются и не нужно переключаться между приложениями и экранами.'
)

def get_ss_link(title):
    ss_link = None
    if ' 10АБ ' in title:
        ss_link = '1Ba2UNTV3T3Rtzh3yraxJfVGvnVgbs_Y-IklyWUjebyg'
    elif ' 9М ' in title:
        ss_link = '1cpTrWurYvugcLdbrmiNuFxKoMRml4qxt_a0kqdLHg7c'
    else:
        raise RuntimeError(f'Could not link spreadsheet for {title}')
    return ss_link


class Generator:
    def __init__(self, title=None, questions=None):
        self._tasks_count = 0
        self._title = title
        self._questions = questions

    def NewTask(self):
        self._tasks_count += 1
        return int(self._tasks_count)

    def Generate(self, up_to=None, image=None):
        self._form = GoogleForm(
            title=self._title,
            description=UP_TO_STR_FMT.format(upTo=up_to),
            confirmationMessage=random.choice(THUMBS_UP_CHOICES) + ' ' + CLOSE_TAB,
            link_existing=get_ss_link(self._title),
        )
        self._form.AddSectionHeaderItem(title=INSTRUCTION)
        self._form.AddTextItem(title='Фамилия Имя', required=True)

        for questions in self._questions:
            self.AddNode(questions)

        self._form.AddTextItem(
            title='Если сдаёшь сильно позже, пожалуйста, кратко напиши причину',
            helpText='Если опоздание до пары минут — точно не надо, 3 минуты — скорее не надо, а больше 15 минут — точно надо.',
        )
        # self._form.AddTextItem(
        #     title='Мне было бы понятно больше заданий на уроке, если бы ...',
        #     helpText='Например, если было больше похожих задач (чтобы понять принцип), ' \
        #         'если было больше времени на самостоятельное решение, ' \
        #         'если бы мы делали больше (и так всё понятно), ' \
        #         'если записи были бы чётче. ' \
        #         'Сюда же можно вписать вообще любой комментарий к уроку. '
        # )
        self._form.AddImageItem(
            url=IMAGES[image or DEFAULT_GIF],
            title='Всё, это конец формы, пора всё проверить (числа, лишние символы в формах, порядок заданий) и отправлять!',
            helpText='Пора проверить и отправлять',
        )

        return self._form

    def AddNode(self, question):
        if isinstance(question, Choice):
            self._form.AddMultipleChoiceItem(title=f'Задание {self.NewTask()}', choices=question._options)
        elif isinstance(question, TextTask):
            self._form.AddTextItem(title=f'Задание {self.NewTask()}', required=False)
        elif isinstance(question, Text):
            self._form.AddTextItem(title=question._text, required=False)
        else:
            raise RuntimeError(f'Invalid question {question} at {title}, {question.__class__.__name__}')
