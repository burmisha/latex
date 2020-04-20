# -*- coding: utf-8 -*-

import problems
import variant

import logging
log = logging.getLogger(__name__)


class BK_52_01(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            При переходе электрона в атоме с одной стационарной орбиты на другую 
            излучается фотон с энергией ${E:Value}$. 
            Какова длина волны этой линии спектра? 
            Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=60)

    def GetArgs(self):
        return {
            'E': [u'E = %s 10^{-19} Дж' % E for E in [u'4.04', u'5.05', u'2.02', u'7.07', u'1.01', u'0.55']],
        }


class BK_52_02(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            Излучение какой длины волны поглотил атом водорода, если полная энергия в атоме увеличилась на ${E:Value}$?
            Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=60)

    def GetArgs(self):
        return {
            'E': [u'E = %d 10^{-19} Дж' % E for E in [2, 3, 4, 6]],
        }


class BK_52_07(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            Сделайте схематичный рисунок энергетических уровней атома водорода 
            и отметьте на нём первый (основной) уровень и последующие.
            Сколько различных длин волн может испустить атом водорода, 
            находящийся в {n}-м возбуждённом состоянии? 
            Отметьте все соответствующие переходы на рисунке и укажите, 
            при каком переходе (среди отмеченных) {what} излучённого фотона {minmax}.
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=100)

    def GetArgs(self):
        return {
            'n': [u'3', u'4', u'5'],
            'what': [u'энергия', u'частота', u'длина волны'],
            'minmax': [u'минимальна', u'максимальна'],
        }


class BK_53_01(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            Какая доля (от начального количества) радиоактивных ядер {what} через время,
            равное {when} периодам полураспада? Ответ выразить в процентах. 
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=100)

    def GetArgs(self):
        return {
            'what': [u'распадётся', u'останется'],
            'when': [u'двум', u'трём', u'четырём'],
        }


class BK_53_02(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            Сколько процентов ядер радиоактивного железа \ce{{^{{59}}Fe}}
            останется через ${t:Value}$, если период его полураспада составляет ${T:Value}$?
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=100)

    def GetArgs(self):
        return {
            't': [u't = %s суток' % t for t in [u'91.2', u'136.8', u'182.4']],
            'T': [u'T = 45.6 суток'],
        }


class BK_53_03(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            За ${t:Value}$ от начального количества ядер радиоизотопа осталась {how}. 
            Какая ещё доля (от начально количества) распадётся, если подождать ещё столько же?
            Каков период полураспада этого изотопа (ответ приведите в сутках)?
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=100)

    def GetArgs(self):
        return {
            'how': [u'четверть', u'одна восьмая', u'половина', u'одна шестнадцатая'],
            't': [u'%d суток' % t for t in [2, 3, 4, 5]],
        }


class BK_53_12(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            Энергия связи ядра {element} равна ${E:Value}$.
            Найти дефект массы этого ядра. Скорость света ${Consts.c:Task}$.
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=100)

    def GetArgs(self):
        # https://www.calc.ru/Energiya-Svyazi-Nekotorykh-Yader.html
        return {
            ('element', 'E'): [
                (u'дейтерия \\ce{^{2}_{1}H} (D)', u'E = 2.22 МэВ'),
                (u'трития \\ce{^{3}_{1}H} (T)', u'E = 8.48 МэВ'),
                (u'гелия \\ce{^{3}_{2}He}', u'E = 7.72 МэВ'),
                (u'гелия \\ce{^{3}_{2}He}', u'E = 28.29 МэВ'),
                (u'лития \\ce{^{6}_{3}Li}', u'E = 31.99 МэВ'),
                (u'лития \\ce{^{7}_{3}Li}', u'E = 39.2 МэВ'),
                (u'бериллия \\ce{^{9}_{4}Be}', u'E = 58.2 МэВ'),
                (u'бора \\ce{^{10}_{5}B}', u'E = 64.7 МэВ'),
                (u'бора \\ce{^{11}_{5}B}', u'E = 76.2 МэВ'),
                (u'углерода \\ce{^{12}_{6}C}', u'E = 92.2 МэВ'),
                (u'углерода \\ce{^{13}_{6}C}', u'E = 97.1 МэВ'),
                (u'азота \\ce{^{14}_{7}N}', u'E = 104.7 МэВ'),
                (u'азота \\ce{^{14}_{7}N}', u'E = 115.5 МэВ'),
                (u'кислорода \\ce{^{16}_{8}O}', u'E = 127.6 МэВ'),
                (u'кислорода \\ce{^{17}_{8}O}', u'E = 131.8 МэВ'),
                (u'кислорода \\ce{^{18}_{8}O}', u'E = 139.8 МэВ'),
            ],
        }



# class Waves01(variant.VariantTask):
#     def __call__(self, nu=None, alpha=None):
#         text = u'''
#             Частота собственных малых колебаний пружинного маятника равна ${nu:Task}$.
#             Чему станет равен период колебаний, если массу пружинного маятника увеличить в ${alpha}$ раз?
#         '''.format(nu=nu, alpha=alpha)
#         T1 = UnitValue(u'T\' = %.2f с' % (math.sqrt(int(alpha)) / int(nu.Value)))
#         answer = u'''$
#             T'  = 2\\pi\\sqrt{{\\frac {{m'}}k}}
#                 = 2\\pi\\sqrt{{\\frac {{\\alpha m}}k}}
#                 = \\sqrt{{\\alpha}} \\cdot 2\\pi\\sqrt{{\\frac mk}}
#                 = \\sqrt{{\\alpha}} \\cdot T
#                 = T\\sqrt{{\\alpha}}
#                 = \\frac 1\\nu \\cdot\\sqrt{{\\alpha}}
#                 = \\frac {{\\sqrt{{\\alpha}}}}\\nu
#                 = \\frac {{\\sqrt{{{alpha}}}}}{nu:Value:s}
#                 = {T1:Value}
#         $'''.format(alpha=alpha, nu=nu, T1=T1)
#         return problems.task.Task(text, answer=answer)

#     def All(self):
#         for nu, alpha in itertools.product(
#             [u'2', u'4', u'5', u'8'],
#             [u'4', u'16', u'25'],
#         ):
#             yield self.__call__(
#                 nu=UnitValue(u'\\nu = %s Гц' % nu),
#                 alpha=alpha,
#             )

