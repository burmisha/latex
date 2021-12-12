import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts

import math

    # \\begin{tikzpicture}[use optics]
    #     \\node[lens] at (0,0) {};
    #     \\node[mirror] at (1cm,0) {};
    # \\end{tikzpicture}


@variant.text('''
    Постройте изображения $A'B'$ и $C'D'$ стрелок $AB$ и $CD$ в зеркале.


    \\begin{tikzpicture}[rotate={rotate}, circuit ee IEC, thick]
        \\node [contact]  (contact1) at (-1.5, 0) {};
        \\draw  (0, 0) to [resistor={info=$R_1$}] ++(left:1.5);
        \\draw  (0, 0) -- ++(up:1.5) to [resistor={near start, info=$R_2$}, resistor={near end, info=$R_3$}] ++(right:3);
        \\draw  (0, 0) to [resistor={info=$R_4$}] ++(right:3) -- ++(up:1.5);
        {appendix}
    \\end{tikzpicture}
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Reflection01(variant.VariantTask):
    pass


@variant.text('''
    Плоское зеркало вращается с угловой скоростью {omega:V:e}.
    Ось вращения лежит в плоскости зеркала. На зеркало падает луч перпендикулярно оси вращения.
    Определите угловую скорость вращения отражённого луча.
''')
@variant.solution_space(80)
@variant.arg(omega='0.1/0.2 рад/с')
@variant.answer_short('\\omega\' = 2 \\omega = {omega2:V}')
class ReflectionRotate(variant.VariantTask):
    def GetUpdate(self, *, omega=None):
        return dict(
            omega2 = 2 * omega,
        )


@variant.text('''
    Плоское зеркало приближается к стационарному предмету размером {d:V:e}
    со скоростью {v:V:e}. Определите размер изображения предмета через {t:V:e} после начала движения,
    если изначальное расстояние мужду зеркалом и предметом было равно {h:V:e}.
''')
@variant.solution_space(80)
@variant.arg(d='5/6/7 см')
@variant.arg(v='10/20/30 см/с')
@variant.arg(h='50/60/70 см')
@variant.arg(t='2/3/4/5 с')
@variant.answer_short('{d:V}')
class ReflectionSize(variant.VariantTask):
    pass


@variant.text('''
    Предмет {what} со скоростью {v:V:e}. Определите скорость изображения.
''')
@variant.solution_space(80)
@variant.arg(v='2/3/4 см/с')
@variant.arg(what=['приближается к плоскому зеркалу', 'отдаляется от плоского зеркала'])
@variant.answer_align([
])
class ReflectionSpeed(variant.VariantTask):
    pass


@variant.text('''
    Запишите своё имя (не фамилию) печатными буквами
    и постройте их изображение в 2 зеркалах: вертикальном и горизонтальном.
''')
@variant.solution_space(80)
@variant.no_args
class ReflectionName(variant.VariantTask):
    pass
