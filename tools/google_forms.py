from library.google_forms import GoogleForm

import subprocess
import logging
log = logging.getLogger(__name__)


def get_example_form():
    form = GoogleForm(
        title='2020.10.22 10АБ - тест',
        description='Отправить до 8:50',
        confirmationMessage='Спасибо, ты молодчина!',
    )
    form.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке', required=True)
    form.AddMultipleChoiceItem(title='Класс', choices=[9, 10], showOtherOption=True)
    form.AddMultipleChoiceItem(title='Школа', choices=['554, Москва'], showOtherOption=True)
    form.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    form.AddTextItem(title='Задание 2', required=False)
    form.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')
    return form

def get_all_forms():
    confirmation = 'Спасибо, ты молодчина!'
    upTo = lambda time: 'Отправить до {} (напомню, что Гугл-формы сохраняют время отправки). И пожалуйста, проверьте, что выше верно указана дата и ваш класс (если нет — как можно быстрее дайте знать)'.format(time)

    form_2020_10_22_10 = GoogleForm(title='2020.10.22 10АБ - тест по динамике - 1', description=upTo('8:50'), confirmationMessage=confirmation)
    form_2020_10_22_10.AddSectionHeaderItem(title='''Возможно, стоит сначала посмотреть эту форму, потом всё решить у себя в тетради или черновике, а лишь после вписать ответы, чтобы не переключаться между приложениями или экранами''')
    form_2020_10_22_10.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке, пожалуйста', required=True)
    for task_index in range(1, 5, 1):
        form_2020_10_22_10.AddMultipleChoiceItem(title=f'Задание {task_index}', choices=['Верно', 'Неверно', 'Недостаточно данных в условии'])
    for task_index in range(5, 11, 1):
        form_2020_10_22_10.AddTextItem(title=f'Задание {task_index}')
    form_2020_10_22_10.AddTextItem(title='Сколько задач на уроке сегодня было понятно?')
    form_2020_10_22_10.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    form_2020_10_22_10.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')

    form_2020_10_22_9 = GoogleForm(title='2020.10.22 9М - тест по динамике - 1', description=upTo('10:50'), confirmationMessage=confirmation)
    form_2020_10_22_9.AddSectionHeaderItem(title='''Возможно, стоит сначала посмотреть эту форму, потом всё решить у себя в тетради или черновике, а лишь после вписать ответы, чтобы не переключаться между приложениями или экранами''')
    form_2020_10_22_9.AddTextItem(title='Фамилия Имя', helpText='Именно в таком порядке, пожалуйста', required=True)
    for task_index in range(1, 11, 1):
        form_2020_10_22_9.AddMultipleChoiceItem(title=f'Задание {task_index}', choices=['А', 'Б', 'В'])
    form_2020_10_22_9.AddTextItem(title='Сколько задач (из 20) на уроке сегодня было понятно?')
    form_2020_10_22_9.AddSectionHeaderItem(title='Это конец формы, пора всё проверить и отправлять')
    form_2020_10_22_9.AddImageItem(url='https://media.giphy.com/media/WxxsVAJLSBsFa/giphy.gif', title='Всё!', helpText='Пора проверить и отправлять')

    return {
        'example': get_example_form(),
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
            log.info('Go to https://script.google.com/home and enter code above')
            last_name = name

    if last_query:
        subprocess.run('pbcopy', universal_newlines=True, input=last_query)
        log.info(f'Copied query for {last_name} to clipboard (it was last one)')
    else:
        log.info(f'No forms to match {form_filter}')

    log.info('See all forms at: https://docs.google.com/forms/u/0/')



def populate_parser(parser):
    parser.add_argument('--filter', help='Find forms containg this substring')
    parser.set_defaults(func=run)
