# -*- coding: utf-8 -*-

import task


class Gendenshteyn10(task.TasksGenerator):
    def GetBookName(self):
        return 'gendenshteyn-10'

    def __call__(self):
        tasks = {
            '08-11': ur'Брусок массой $2\\units{кг}$ лежит на столе. Коэффициент трения между бруском и поверзностью стола равен $0{,}25$. Какую горизонтальную силу надо приложить к бруску, чтобы сдвинуть его с места?',
            '08-12': ur'Чтобы сдвинуть с места лежищий на столе том энциклопедии массой $5\\units{кг}$, к нему надо приложить горизонтальную силу $15\\units{Н}$. Каков коэффициент трения между этим томом и столом?',
            '08-13': ur'На санки массой $8\\units{кг}$, скользящие равномерно по горизонтальной дороге, действует сила трения $8\\units{Н}$. Определите коэффициент трения между полозьями и дорогой.',
            '09-11': ur'С каким ускорением съезжает тележка по наклонной плоскости длиной $130\\units{см}$ и высотой $50\\units{см}$? Трение не учитывайте.',
            '09-12': ur'Тележка съезжает с наклонной плоскости длиной $4\\units{м}$ с ускорением $2\fracunits{м}{}{с}{2}$. Какова высота наклонной плоскости? Трением пренебречь.',
            '21-13': ur'С какой силой взаимодействуют 2 точечных заряда в 2 и 4 нКл, находящиеся на расстоянии $3\\units{см}$?', # 8 * 10 ** -5
            '21-17': ur'На каком расстоянии друг от друга два точечных заряда по 4 нКл отталкиваются с силой $0{,}36\\units{мН}$?',
            '21-27': ur'Две пылинки находятся на расстоянии $d=10\\units{см}$ друг от друга. Какой будет сила взаимодействия между ними, если $N=10\\units{миллиардов}$ электронов «перенести» с одной из них на другую?',
            '22-20': ur'С каким ускорением движется протон в электрическом поле напряжённостью $E=40\funits{кН}{Кл}$?',
            '22-31': ur'В какой точке напряжённость поля двух точечных зарядов 4 и 16 нКл равна нулю? Расстояние между зарядами равно $12\\units{см}$.',
            '22-35': ur'В вершинах квадрата со стороной $a$ расположены 3 положительных заряда $q$ и один отрицательный заряд $-q$. Найдите напряжённость электрического поля в центре квадрата.',
            '23-37': ur'Скорость электрона уменьшилась от $10\,000\tfracunits{км}{}{c}{}$ до 0. Какую разность потенциалов прошёл электрон?',
            '23-49': ur'Энергия заряженного конденсатора электроёмкостью $400\\units{мкФ}$ равна $200\\units{Дж}$. Определите разность потенциалов между его обкладками.',
            '23-53': ur'Металлическому шару радиусом $2\\units{см}$ передан заряд $40\\units{нКл}$. Каков потенциал точек на расстоянии $0\\units{см}$, $\frac\pi2\\units{см}$, $2\\units{см}$, $4\\units{см}$ от центра шара?',
            '23-57': ur'Чему равна напряжённость и потенциал поля в центре равномерно заряженного проволочного кольца? Заряд кольца $Q$, радиус $R$. А на расстоянии $d$ от плоскости кольца на его оси симметрии?',
        }
        for number, text in tasks.iteritems():
            yield task.Task(text, number=number)