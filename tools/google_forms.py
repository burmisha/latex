from library.google_forms import GoogleForm

import subprocess

import logging
log = logging.getLogger(__name__)


class TestFormGenerator:
    def __init__(self, title=None, upTo=None, count=None):
        confirmation = 'Спасибо, ты молодчина!'
        instruction = 'Возможно, стоит сначала посмотреть эту форму, ' \
            'потом всё решить у себя в тетради или черновике, а лишь после вписать ответы, ' \
            'чтобы не переключаться между приложениями или экранами.'
        upToStr = f'Отправить до {upTo} (напомню, что Гугл-формы сохраняют время отправки). ' \
            'И пожалуйста, проверьте, что выше верно указана дата и ваш класс ' \
            '(если нет — дайте знать как можно раньше). ' \
            '554 школа, Москва, 2020–2021 учебный год.'
        self._count = count
        self._task_number = 0
        self._form = GoogleForm(
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
        assert self._count == self._task_number
        images = {
            'minions': 'https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif',
            'incredibles': 'https://media.giphy.com/media/G2fKgPMXJ40WA/giphy.gif',
            'insideout': 'https://media.giphy.com/media/dU6Ec1svWeWCk/giphy.gif',
        }
        self._form.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
        self._form.AddImageItem(url=images[image], title='Всё!', helpText='Пора проверить и отправлять')
        return self._form


def get_all_forms():
    example = GoogleForm(title='Пример', description='Отправить до полуночи', confirmationMessage='Спасибо, ты молодчина!')
    example.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке', required=True)
    example.AddMultipleChoiceItem(title='Класс', choices=[9, 10], showOtherOption=True)
    example.AddMultipleChoiceItem(title='Школа', choices=['554, Москва'], showOtherOption=True)
    example.AddTextItem(title='Задание 2', required=False)
    example.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    example.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')

    form_generator = TestFormGenerator(title='2020.10.22 10АБ - тест по динамике - 1', upTo='8:50', count=10)
    form_generator.AddMultipleChoiceTask(choices=['Верно', 'Неверно', 'Недостаточно данных в условии'], count=4)
    form_generator.AddTextTask(count=6)
    form_generator.AddText(title='Сколько задач на уроке сегодня было понятно?')
    form_2020_10_22_10 = form_generator.Generate()

    form_generator = TestFormGenerator(title='2020.10.22 9М - тест по динамике - 1', upTo='10:50', count=10)
    form_generator.AddMultipleChoiceTask(choices=['А', 'Б', 'В'], count=10)
    form_generator.AddText(title='Сколько задач (из 20) на уроке сегодня было понятно?')
    form_2020_10_22_9 = form_generator.Generate()

    return {
        'example': example,
        '2020-10-22-9': form_2020_10_22_9,
        '2020-10-22-10': form_2020_10_22_10,
    }


def run(args):
    form_filter = args.filter
    last_query = None
    last_name = None
    for name, form in sorted(get_all_forms().items()):
        if form_filter is None or form_filter in name:
            log.info(f'Script for {name}')
            last_query = form.FormQuery()
            log.info(f'\n\n{last_query}\n\n')
            log.info('Paste and run code above at https://script.google.com/home')
            last_name = name

    if last_query:
        subprocess.run('pbcopy', universal_newlines=True, input=last_query)
        log.info(f'Copied query for {last_name} to clipboard (it was last one)')
    else:
        log.warning(f'No forms to match {form_filter}')

    log.info('See all forms at: https://docs.google.com/forms/u/0/')



def populate_parser(parser):
    parser.add_argument('--filter', help='Find forms containg this substring')
    parser.set_defaults(func=run)
