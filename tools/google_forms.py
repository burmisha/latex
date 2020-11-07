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


class TestFormGenerator:
    def __init__(self, title=None, upTo=None, count=None):
        confirmation = random.choice([
            'Спасибо, ты молодчина!',
            'Готово, всё сохранили!',
            'Принято, ответы записаны!',
        ]) + ' Закрывай вкладку, а то иногда отправляются дубли.'
        instruction = 'Рекомендуется сначала просмотреть форму ответов на этой странице, ' \
            'потом всё решить у себя в тетради, а лишь после заполнить форму. ' \
            'Так ответы не потеряются и не нужно переключаться между приложениями и экранами.'
        upToStr = f'Отправить до {upTo} (напомню, что Гугл-формы сохраняют время отправки). ' \
            'И пожалуйста, проверьте, что выше верно указана дата и ваш класс ' \
            '(если нет — дайте знать как можно раньше). ' \
            '554 школа, Москва, 2020–2021 учебный год.'
        self._count = count
        self._task_number = 0
        self._form = library.google_forms.GoogleForm(
            title=title,
            description=upToStr,
            confirmationMessage=confirmation,
        )
        self._form.AddSectionHeaderItem(title=instruction)
        self._form.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке, пожалуйста', required=True)

    def NewTask(self):
        self._task_number += 1
        return int(self._task_number)

    def AddTextTask(self, count=1):
        for i in range(count):
            task_number = self.NewTask()
            title = f'Задание {task_number}'
            self._form.AddTextItem(title=title, required=False)

    def AddText(self, title=None, required=False):
        self._form.AddTextItem(title=title, required=required)

    def AddMultipleChoiceTask(self, choices=None, count=1):
        for i in range(count):
            task_number = self.NewTask()
            self._form.AddMultipleChoiceItem(title=f'Задание {task_number}', choices=choices)

    def Generate(self, image='minions'):
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
        }
        self._form.AddTextItem(
            title='Если сдаёшь сильно позже, пожалуйста, кратко напиши причину',
            helpText='Если опоздание до пары минут — точно не надо, 3 минуты — скорее не надо, а больше 15 минут — точно надо.',
        )
        self._form.AddTextItem(
            title='Мне было бы понятно больше заданий на уроке, если бы ...',
            helpText='Например, если было больше похожих (чтобы понять принцип), ' \
                'если было больше времени на самостоятельное решение,' \
                'если бы мы делали больше (и так всё понятно),' \
                'если записи были бы чётче. ' \
                'Сюда же можно вписать вообще любой комментарий к уроку. '
        )
        self._form.AddImageItem(
            url=images[image],
            title='Всё, это конец формы, пора всё проверить (числа, лишние символы в формах, порядок заданий) и отправлять!',
            helpText='Пора проверить и отправлять',
        )
        return self._form


def get_all_forms():
    example = library.google_forms.GoogleForm(title='Пример', description='Отправить до полуночи', confirmationMessage='Спасибо, ты молодчина!')
    example.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке', required=True)
    example.AddMultipleChoiceItem(title='Класс', choices=[9, 10], showOtherOption=True)
    example.AddMultipleChoiceItem(title='Школа', choices=['554, Москва'], showOtherOption=True)
    example.AddTextItem(title='Задание 2', required=False)
    example.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    example.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')
    yield 'example', example

    test_forms_config = {
        '2020-10-22-10АБ': {
            'title': 'Тест по динамике - 1',
            'upTo': '8:50',
            'tasks': [
                ('choices', 4, ['Верно', 'Неверно', 'Недостаточно данных в условии']),
                ('any', 6),
                ('text', 'Сколько задач на уроке сегодня было понятно?'),
            ],
        },
        '2020-10-22-9М': {
            'title': 'Тест по динамике - 1',
            'upTo': '10:50',
            'tasks': [
                ('choices', 10, ['А', 'Б', 'В']),
                ('text', 'Сколько задач на уроке сегодня было понятно?'),
            ],
        },
        '2020-10-27-9М': {
            'title': 'Тест по динамике - 2',
            'upTo': '10:50',
            'image': 'incredibles',
            'tasks': [
                ('choices', 8, ['А', 'Б', 'В']),
                ('any', 4),
            ],
        },
        '2020-10-27-10АБ': {
            'title': 'Тест по динамике - 2',
            'upTo': '10:05',
            'image': 'incredibles',
            'tasks': [
                ('any', 7),
            ],
        },
        '2020-10-29-10АБ': {
            'title': 'Тест по динамике - 3',
            'upTo': '12:05',
            'image': 'insideout',
            'tasks': [
                ('choices', 6, ['А', 'Б', 'В']),
                ('any', 11),
            ],
        },
        '2020-10-30-10АБ': {
            'title': 'Тест по динамике - 4',
            'upTo': '10:05',
            'image': 'minions',
            'tasks': [
                ('choices', 9, ['А', 'Б', 'В']),
                ('any', 3),
            ],
        },
        '2020-11-03-10АБ': {
            'title': 'Тест по динамике - 5',
            'upTo': '9:05',
            'image': 'insideout',
            'tasks': [
                ('text', 'Электронная почта (только для 10«Б», 10«А» уже присылал)'),
                ('choices', 2, ['А', 'Б', 'В']),
                ('any', 5),
            ],
        },
        '2020-11-03-9М': {
            'title': 'Тест по динамике - 3',
            'upTo': '11:05',
            'image': 'insideout',
            'tasks': [
                ('text', 'Электронная почта'),
                ('choices', 10, ['А', 'Б', 'В']),
            ],
        },
        '2020-11-06-10АБ': {
            'title': 'Тест по динамике - 6',
            'upTo': '10:05',
            'image': 'up',
            'tasks': [
                ('any', 8),
            ],
        },
    }
    for key, config in test_forms_config.items():
        title = '{} - {}'.format(
            key.replace('-', '.', 2).replace('-', ' ', 1),
            config['title'],
        )
        form_generator = TestFormGenerator(title=title, upTo=config['upTo'])
        for task_config in config['tasks']:
            if task_config[0] == 'choices':
                form_generator.AddMultipleChoiceTask(choices=task_config[2], count=task_config[1])
            elif task_config[0] == 'any':
                form_generator.AddTextTask(count=task_config[1])
            elif task_config[0] == 'text':
                form_generator.AddText(title=task_config[1])

        yield key, form_generator.Generate(image=config.get('image'))


def run(args):
    form_filter = args.filter

    key_picker = library.picker.KeyPicker(key=lambda x: x.replace('.', '').replace('-', ''))
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
            tab_opener.open(script_url)
            tab_opener.open(forms_url)


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='Find forms containg this substring')
    parser.add_argument('--log-query', help='Log query')
    parser.add_argument('--browser', help='Default browser', default='Firefox')
    parser.add_argument('-o', '--open', help='Open browser', action='store_true')
    parser.set_defaults(func=run)
