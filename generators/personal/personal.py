import generators.variant as variant

from generators.helpers import Fraction, Consts

import math



@variant.text('''
    \\begin{itemize}
        \\item Как меня зовут? 
        \\item Как называется предмет? 
        \\item Какого цвета учебник? 
        \\item Чем заканчивается анекдот? 
    \\end{itemize}
''')
@variant.solution_space(0)
@variant.no_args
class Joke(variant.VariantTask):
    pass



@variant.text('''
    \\begin{itemize}
        \\item Как проведёте {what} перед экзаменом по {subj}? 
        \\item Куда съездите и как отдохнёте после? 
    \\end{itemize}
''')
@variant.solution_space(100)
@variant.arg(what=['вечер', 'утро'])
@variant.arg(subj=['математике', 'русскому языку'])
class BeforeExam(variant.VariantTask):
    pass


@variant.text('''
    О существовании какого населённого пункта вы узнали этой весной? Чем он вам запомнился? 
''')
@variant.solution_space(60)
@variant.no_args
class Bucha(variant.VariantTask):
    pass


@variant.text('''
    \\begin{itemize}
        \\item Какой ЕГЭ (кроме математики и русского) вы сдаете? 
        \\item Сколько времени у вас будет на финальную подготовку и повторение?
        \\item Как вы распределите время на экзамене? 
        \\item Как искать ошибки и проверять себя? 
    \\end{itemize}
''')
@variant.solution_space(120)
@variant.arg(what=['вечер', 'утро'])
@variant.arg(subj=['математике', 'русскому языку'])
class ExtraExam(variant.VariantTask):
    pass



@variant.text('''
    Выберите и запишите из всего курса физики 2 формулы:
    \\begin{itemize}
        \\item наиболее {good},
        \\item и наименее {bad}.
    \\end{itemize}
''')
@variant.solution_space(120)
@variant.arg(good='смешную/запомнившуюсю/полезную/удивительную')
@variant.arg(bad='важную/интересную')
class Formula(variant.VariantTask):
    pass


@variant.text('''
    \\begin{itemize}
        \\item Какие физические открытия или достижения были сделаны на веку вас и ваших родителей?
        \\item Как это повлияло на нашу жизнь? 
    \\end{itemize}
''')
@variant.solution_space(80)
@variant.no_args
class Advances(variant.VariantTask):
    pass



@variant.text('''
    Назовите 6 знаменитых деятелей и деятельниц физики и области науки, в которых они работали. 
    Обеспечьте представительство различных групп. 
''')
@variant.solution_space(100)
@variant.no_args
class Who(variant.VariantTask):
    pass



@variant.text('''
    Назовите 3 возможные причины для вас лично вернуться в школу.
''')
@variant.solution_space(60)
@variant.no_args
class Why(variant.VariantTask):
    pass


@variant.text('''
    Где бы вы хотели поработать, но ТЕПЕРЬ не получится?
    Какие новые возможности открылись за последние месяцы? 
''')
@variant.solution_space(60)
@variant.no_args
class JobFuture(variant.VariantTask):
    pass


@variant.text('''
    Расскажите на какой работе вы уже поработали? 
    Сколько часов в неделю и сколько недель или месяцев опыта? Норм по деньгам?
''')
@variant.solution_space(120)
@variant.no_args
class JobPresent(variant.VariantTask):
    pass


@variant.text('''
    Что нового вы попробуете в июле-августе?
    Куда надо съездить и где побывать?
    Укажите не менее 3 активностей и 7 мест.
''')
@variant.solution_space(80)
@variant.no_args
class Where(variant.VariantTask):
    pass



@variant.text('''
    По какому принципу зарубежные университеты сохраняют партнёрство с российскими?
''')
@variant.solution_space(80)
@variant.no_args
class Uni(variant.VariantTask):
    pass

 

@variant.text('''
    Посоветуйте свой (или не свой) Тг/TT/YT/Ig.
    Точным названием или ссылкой, не более двух ответов.
''')
@variant.solution_space(80)
@variant.no_args
class Contact(variant.VariantTask):
    pass


# Подпишите все физические величины в формуле. 

# Дополните ответ на задание 7?

