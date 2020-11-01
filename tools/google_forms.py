import library.google_forms

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

    def Generate(self, image=None):
        if not image:
            image = 'minions'
        assert self._count == self._task_number or self._count is None
        images = {
            'minions': 'https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif',
            'incredibles': 'https://media.giphy.com/media/G2fKgPMXJ40WA/giphy.gif',
            'insideout': 'https://media.giphy.com/media/dU6Ec1svWeWCk/giphy.gif',
        }
        self._form.AddTextItem(title='Если сдаёшь сильно позже, напиши, пожалуйста, причину', helpText='Если опоздание до 1–2 минут — писать точно не надо, 3 — скорее не надо, если больше 15 минут — точно надо.')
        self._form.AddImageItem(
            url=images[image],
            title='Всё, это конец формы, пора всё проверить и отправлять!',
            helpText='Пора проверить и отправлять',
        )
        return self._form


def get_all_forms():
    forms = {}
    example = library.google_forms.GoogleForm(title='Пример', description='Отправить до полуночи', confirmationMessage='Спасибо, ты молодчина!')
    example.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке', required=True)
    example.AddMultipleChoiceItem(title='Класс', choices=[9, 10], showOtherOption=True)
    example.AddMultipleChoiceItem(title='Школа', choices=['554, Москва'], showOtherOption=True)
    example.AddTextItem(title='Задание 2', required=False)
    example.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    example.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')
    forms['example'] = example

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

        forms[key] = form_generator.Generate(image=config.get('image'))

    return forms


def log_list(items):
    return ''.join('\n    - ' + item for item in items)


def run(args):
    form_filter = args.filter
    all_forms = get_all_forms()
    if form_filter:
        matched_names = sorted([name for name in all_forms if form_filter in name])
        if len(matched_names) > 1:
            log.warning('Too many matches for \'%s\':%s', form_filter, log_list(sorted(matched_names)))
        elif len(matched_names) == 1:
            name = matched_names[0]
            query = all_forms[name].FormQuery()
            library.process.pbcopy(query)
            log.info(f'Script for {name}: \n{query}\n')
            log.info(f'Copied query for {name} to clipboard')
            log.info('Paste and run JS-code at https://script.google.com/home')
            log.info('See all ready forms at: https://docs.google.com/forms/u/0/')
        else:
            log.warning('No forms to match \'%s\'\nAvailable forms:%s', form_filter, log_list(sorted(all_forms)))
    else:
        log.info('Available forms:%s', log_list(sorted(all_forms)))



def populate_parser(parser):
    parser.add_argument('--filter', help='Find forms containg this substring')
    parser.set_defaults(func=run)
