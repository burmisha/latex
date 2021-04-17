import library.google_forms

import random
import subprocess
import webbrowser

import logging
log = logging.getLogger(__name__)


class TabOpener:
    def __init__(self, browser):
        self._controller = webbrowser.get(browser)

    def open(self, url):
        self._controller.open_new_tab(url)


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
        self._form = library.google_forms.GoogleForm(
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



def get_all_forms():
    example = library.google_forms.GoogleForm(title='Пример', description='Отправить до полуночи', confirmationMessage='Спасибо, ты молодчина!')
    example.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке', required=True)
    example.AddMultipleChoiceItem(title='Класс', choices=[9, 10], showOtherOption=True)
    example.AddMultipleChoiceItem(title='Школа', choices=['554, Москва'], showOtherOption=True)
    example.AddTextItem(title='Задание 2', required=False)
    example.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    example.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')
    yield 'example', example

    choices = lambda count, variants: ('choices', count, variants)
    alpha = list('АБВГД')
    email = lambda desc: [Text(f'Электронная почта {desc}'.strip())]
    abv_choices = Choice(alpha[:3])
    text_task = TextTask()

    forms_config = [
        ('2020.10.22 10АБ - Тест по динамике - 1', '8:50', None,
            Choice(['Верно', 'Неверно', 'Недостаточно данных в условии']) * 4 +
            text_task * 6 +
            [Text('Сколько задач на уроке сегодня было понятно?')]
        ),
        ('2020.10.22 9М - Тест по динамике - 1', '10:50', None,
            abv_choices * 10 + [Text('Сколько задач на уроке сегодня было понятно?')],
        ),
        ('2020.10.27 9М - Тест по динамике - 2', '10:50', 'incredibles', abv_choices * 8 + text_task * 4),
        ('2020.10.27 10АБ - Тест по динамике - 2', '10:05', 'incredibles', text_task * 7),
        ('2020.10.29 10АБ - Тест по динамике - 3', '12:05', 'insideout', abv_choices * 6 + text_task * 11),
        ('2020.10.30 10АБ - Тест по динамике - 4', '10:05', 'minions', abv_choices * 9 + text_task * 3),
        ('2020.11.03 10АБ - Тест по динамике - 5', '9:05', 'insideout',
            email('(только для 10«Б», 10«А» уже присылал)') + abv_choices * 2 + text_task * 5,
        ),
        ('2020.11.03 9М - Тест по динамике - 3', '11:05', 'insideout', email('') + abv_choices * 10),
        ('2020.11.06 10АБ - Тест по динамике - 6', '10:05', 'up', text_task * 8),
        ('2020.11.12 9М - Динамика - 6', '10:15', 'zootopia', abv_choices * 5 + text_task * 4),
        ('2020.11.13 10АБ - Законы сохранения - 1', '10:05', 'zootopia',
            email('(если не присылали на прошлой неделе)') + abv_choices * 6 + text_task * 4,
        ),
        ('2020.11.19 9М - Законы сохранения - 1', '10:05', 'up', abv_choices * 6 + text_task * 4),
        ('2020.11.26 10АБ - Законы сохранения - 2', '12:05', 'incredibles', text_task * 10),
        ('2020.12.04 10АБ - Статика и гидростатика - 1', '12:05', 'ratatouille',
            text_task * 7 + [Text('Ссылка на гифку'), Text('Какой вопрос добавить в опрос?')],
        ),
        ('2020.12.08 9М - Колебания и волны - 1', '11:05', 'ratatouille', abv_choices * 8),
        ('2020.12.10 9М - Колебания и волны - 2', '11:05', 'incredibles', abv_choices * 8),
        ('2020.12.11 10АБ - Статика и гидростатика - 2', '11:05', 'minions', text_task * 5),
        ('2020.12.17 9М - Колебания и волны - 3', '11:05', 'keanureeves', abv_choices * 10),
        ('2020.12.22 9М - Колебания и волны - 4', '11:05', 'zootopia', abv_choices * 10),
        ('2021.04.15 10АБ - Электростатика - 1', '9:02', 'zootopia', text_task * 7),
        ('2021.04.16 9М - Строение атома - 1', '11:02', 'zootopia', text_task * 7),
    ]
    for title, up_to, image, questions in forms_config:
        form_generator = TestFormGenerator(title=title, upTo=up_to, image=image)
        for node in questions:
            form_generator.AddNode(node)
        yield title, form_generator.Generate()


def run(args):
    form_filter = args.filter

    key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
    for key, value in get_all_forms():
        key_picker.add(key, value)

    form = key_picker.get(form_filter)
    if form:
        query = form.FormQuery()

        if args.log_query:
            log.info(f'Script: \n{query}\n')

        library.process.pbcopy(query)
        log.info('Copied query to clipboard')

        tab_opener = TabOpener(args.browser)
        script_url = 'https://script.google.com/home'
        forms_url = 'https://docs.google.com/forms/u/0/'
        log.info(f'Paste and run JS-code at {script_url}')
        log.info(f'See all ready forms at {forms_url}')
        if args.open:
            tab_opener.open(forms_url)
            tab_opener.open(script_url)
        else:
            log.info('Add --open or -o option to open browser')


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='Find forms containg this substring')
    parser.add_argument('--log-query', help='Log query')
    parser.add_argument('--browser', help='Default browser', default='Firefox')
    parser.add_argument('-o', '--open', help='Open browser', action='store_true')
    parser.set_defaults(func=run)
