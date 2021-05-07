import classes.variants

import library.process
from library.gform.form import GoogleForm

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

    for work in classes.variants.get_all_variants():
        gform = work.get_gform()
        if gform:
            yield work._human_name, gform


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

        library.process.pbcopy(query, name=f'query for {form._title!r}')

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
