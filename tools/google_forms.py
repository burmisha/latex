import classes.variants

import library.process
from library.gform.form import GoogleForm
from library.gform.generator import Generator
from library.gform.node import Choice, Text, TextTask, text_task, abv_choices

import logging
log = logging.getLogger(__name__)


def get_all_forms():
    example = GoogleForm(title='Пример', description='Отправить до полуночи', confirmationMessage='Спасибо, ты молодчина!')
    example.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке', required=True)
    example.AddMultipleChoiceItem(title='Класс', choices=[9, 10], showOtherOption=True)
    example.AddMultipleChoiceItem(title='Школа', choices=['554, Москва'], showOtherOption=True)
    example.AddTextItem(title='Задание 2', required=False)
    example.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    example.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')
    yield 'example', example

    email = lambda desc: Text(f'Электронная почта {desc}'.strip())
    forms_config = [
        ('2020.10.22 10АБ - Тест по динамике - 1', '8:50', None,
            Choice(['Верно', 'Неверно', 'Недостаточно данных в условии']) * 4 +
            text_task * 6 +
            Text('Сколько задач на уроке сегодня было понятно?')
        ),
        ('2020.10.22 9М - Тест по динамике - 1', '10:50', None,
            abv_choices * 10 + Text('Сколько задач на уроке сегодня было понятно?'),
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
        ('2020.12.04 10АБ - Статика и гидростатика - 1', '12:05', 'ratatouille',
            text_task * 7 + Text('Ссылка на гифку') + Text('Какой вопрос добавить в опрос?'),
        ),
        ('2020.12.08 9М - Колебания и волны - 1', '11:05', 'ratatouille', abv_choices * 8),
        ('2020.12.10 9М - Колебания и волны - 2', '11:05', 'incredibles', abv_choices * 8),
        ('2020.12.17 9М - Колебания и волны - 3', '11:05', 'keanureeves', abv_choices * 10),
        ('2020.12.22 9М - Колебания и волны - 4', '11:05', 'zootopia', abv_choices * 10),
    ]
    for title, up_to, image, questions in forms_config:
        form_generator = Generator(title=title, questions=questions)
        yield title, form_generator.Generate(up_to=up_to, image=image)

    for work in classes.variants.get_all_variants():
        if work._up_to is not None:
            form_generator = Generator(title=work._human_name, questions=work._questions)
            yield work._human_name, form_generator.Generate(up_to=work._up_to, image=work._image)


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

        library.process.pbcopy(query, name='query')

        tab_opener = library.process.TabOpener(args.browser)
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
