import random

from library.gform.node import Choice, TextTask, Text
from library.gform.form import GoogleForm



def get_ss_link(title):
    ss_link = None
    if ' 10АБ ' in title:
        ss_link = '1Ba2UNTV3T3Rtzh3yraxJfVGvnVgbs_Y-IklyWUjebyg'
    elif ' 9М ' in title:
        ss_link = '1cpTrWurYvugcLdbrmiNuFxKoMRml4qxt_a0kqdLHg7c'
    else:
        raise RuntimeError(f'Could not link spreadsheet for {title}')
    return ss_link



class TestFormGenerator:
    def __init__(self, title=None, upTo=None, count=None, image=None):
        confirmation = random.choice([
            'Спасибо, ты молодчина!',
            'Готово, всё сохранили!',
            'Принято, ответы записаны!',
        ]) + ' Закрой вкладку, а то иногда отправляются дубли.'
        instruction = 'Рекомендуется сначала просмотреть форму ответов на этой странице, ' \
            'потом открыть задание и всё решить у себя в тетради, а лишь после заполнять форму. ' \
            'Так ответы не потеряются и не нужно переключаться между приложениями и экранами.'
        upToStr = f'Отправить до {upTo} (напомню, что Гугл-формы сохраняют время отправки). ' \
            'И пожалуйста, проверьте, что выше верно указаны дата и класс ' \
            '(если нет — дайте знать как можно раньше). ' \
            '554 школа, Москва, 2020–2021 учебный год.'
        self._count = count
        self._task_number = 0
        self._form = GoogleForm(
            title=title,
            description=upToStr,
            confirmationMessage=confirmation,
            link_existing=get_ss_link(title),
        )
        self._form.AddSectionHeaderItem(title=instruction)
        self._form.AddTextItem(title='Фамилия Имя', required=True)
        self._image = image

    def NewTask(self):
        self._task_number += 1
        return int(self._task_number)

    def Generate(self):
        image = self._image or 'minions'
        assert self._count == self._task_number or self._count is None
        images = {
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
            url=images[image],
            title='Всё, это конец формы, пора всё проверить (числа, лишние символы в формах, порядок заданий) и отправлять!',
            helpText='Пора проверить и отправлять',
        )

        return self._form

    def AddNode(self, node):
        if isinstance(node, Choice):
            self._form.AddMultipleChoiceItem(title=f'Задание {self.NewTask()}', choices=node._options)
        elif isinstance(node, TextTask):
            self._form.AddTextItem(title=f'Задание {self.NewTask()}', required=False)
        elif isinstance(node, Text):
            self._form.AddTextItem(title=node._text, required=False)
        else:
            raise RuntimeError(f'Invalid node {node} at {title}, {node.__class__.__name__}')
