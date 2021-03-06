import problems.task as task


class Gendenshteyn8(task.TasksGenerator):
    def GetBookName(self):
        return 'gendenshteyn-8'

    def __call__(self):
        tasks = {
            '5-05': r'Сколько энергии выделится при полном сгорании керосина массой $1\\units{кг}$? ',
            '5-10': r'При полном сгорании природного газа выделилось количество теплоты $17{,}6\\units{МДж}$. Сколько газа было сожжено?',
            '5-12': r'Какое количество теплоты выделяется при полном сгорании смеси $2{,}5\\units{кг}$ бензина и $0{,}5\\units{кг}$ спирта?  ',
            '5-13': r'Сколько энергии выделится при полном сгорании керосина объёмом $2{,}5\\units{л}$? ',
            '5-17': r'Почему в качестве топлива выгоднее использовать бензин, а не порох, но порох нельзя заменить бензином в артиллерийских снарядах?',
            '5-18': r'Почему удельная теплота сгорания сырых дров меньше, чем удельная теплота сгорания тех же дров после просушки?',
            '5-22': r'Для нагревания воды объёмом $10\\units{л}$ сожгли керосин массой $50\\units{г}$. На сколько изменилась температура воды, если она получила $50\%$ теплоты сгорания керосина?',
            '5-24': r'До какой температуры можно нагреть $20\\units{л}$ воды, температура которой $20\celsius$, сжигая бензин массой $20\\units{г}$? Считайте, что всё количество теплоты, выделившееся при сгорании бензина, идёт на нагревание воды.',
            '5-25-my': r'Определите КПД нагревателя, если при сгорании вещества выделилось $12{,}4\\units{МДж}$, а внутренняя энергия нагреваемого тела увеличилась на $2{,}7\\units{МДж}$.',
            '5-25': r'Определите КПД спиртовки, если при нагревании на ней $150\\units{г}$ воды от $20\celsius$ до $80\celsius$ израсходован спирт массой $4\\units{г}$.',
            '5-36': r'В медной кастрюле нагрели $5\\units{л}$ воды от температуры $14\celsius$ до кипения, израсходовав керосин массой $100\\units{г}$. Определите массу кастрюли, если КПД нагревателя $40\%$.',
            '5-38-my': r'Отношение масс бензина и спирта в смеси равно $\alpha=3:2$. Чему равна удельная теплота сгорания этой смеси?',
            '5-38': r'Каково отношение масс бензина и спирта в смеси, удельная теплота сгорания которой $40\tfracunits{МДж}{}{кг}{}$?',
            '5-39': r'Гусеничиный трактор развивает мощность $60\\units{кВт}$, и при этой мощности средняя масса расходуемого за $1\\units{ч}$ дизельного топлива равна $18\\units{кг}$. Найдите КПД двигателя трактора.',
            '6-38': r'Cколько льда, температура которого $-5\celsius$, может расплавить стальной шар массой $5\\units{кг}$, охлаждаясь от $400\celsius$ до $0\celsius$? Считайте, что вся энергия передаётся льду.',
            '6-40': r'В снежный сугроб, имеющий температуру $0\celsius$, бросили раскалённый до температуры $300\celsius$ медный шар массой $2\\units{кг}$. Какова масса расстаявшего снега?',
            '10-01': r'С помощью каких опытов можно определить, обладает ли тело электрическим зарядом?',
            '10-02': r'Какие опыты доказывают, что существуют электрические заряды 2 видов?',
            '10-03': r'Какие способы электризации тел вам известны?',
            '10-04': r'Какое свойство тела характеризует электрический заряд?',
            '10-05': r'Как с помощью листочков бумаги обнаружить, наэлектризовано ли тело?',
            '10-06': r'Почему при расчёсывании сухих волос они прилипают к пластмассовой расчёске?',
            '10-07': r'''
                Притяжение или отталкивание наблюдается между
                \begin{itemize}
                    \item двумя положительно заряженными частицами;
                    \item двумя отрицательно заряженными частицами;
                    \item частицами, одна из которых заряжена положительно, а другая отрицательно?
                \end{itemize}
            ''',
            '10-08': r'В результате протирания сухого стекла тканью стекло и ткань электризовались. Как они будут взаимодействовать: притягиваться или отталкиваться?',
            '10-09': r'Какие вы знаете применения электризации тел?',
            '10-10': r'Чем опасна электризация тел?',
            '10-11': r'Какая частица обладает наименьшим отрицательным зарядом? наименьшим положительным? Как соотносятся их массы? Почему так «неудачно» был выбран знак положительно заряда?',
            '10-12': r'Какие физические характеристики электрона вам известны?',
            '10-13': r'Какой заряд приобретает нейтральное тело, когда оно теряет часть электронов?',
            '11-10': r'Как изменяется сила взаимодействия между двумя точечными зарядами при увеличении расстояния между ними?',
            '11-15': r'Какого знака заряд надо придать медному шару, чтобы его масса уменьшилась?',
            '11-15-my': r'Какого знака заряд надо придать алюминиевому шару, чтобы его масса увеличилась?',
            '11-20': r'Как изменится сила взаимодействия между двумя точечными зарядами, если увеличить расстояние в между ними в 2 раза? А если уменьшить в $1{,}3$ раза? ',
            '11-21': r'Как изменилось расстояние между двумя точечными зарядами, если сила взаимодействия между ними уменьшилась в 9 раз? А если выросла в $1{,}44$ раза?',
            '11-23': r'Заряд одного металлического шарика $5q$, а другого точно такого же — $-9q$. Шарики привели в соприкосновение и раздвинули. Какой будет заряд после этого у каждого из этих шариков?',
            '11-24': r'Заряды двух одинаковых металлических шариков равны соответственно $-8q$ и $-12q$. Шарики привели в соприкосновение и раздвинули. Какой будет заряд после этого у каждого из этих шариков?',
            '11-25': r'С какой силой будут взаимодействовать 2 точечных заряда по $100\\units{мкКл}$, если их расположить в вакууме на расстоянии $1\\units{м}$ друг от друга?',
            '11-26': r'Два точечных заряда по $2{,}3$ и $3{,}5\\units{нКл}$ расположены в вакууме на расстоянии $1{,}7\\units{см}$ друг от друга. Найдите силу взаимодействия между ними.',
            '11-27': r'Два одинаковых точечных заряда, расположенные на расстоянии $9\\units{см}$ в вакууме, отталкиваются с силами $1\\units{мН}$. Каковы модули этих зарядов? Можно ли определить их знаки?',
            '12-00-my-1': r'Какая сила будет действовать на заряд $Q$, если поместить его расстоянии $l$ от заряда $q$?',
            '12-00-my-2': r'$\triangle ABC$ — прямоугольный и равнобедренный, гипотенуза $AB=d$. В точки~$A$ и $B$ поместили по заряду~$q$, а в точку $C$~— $Q$. Какая сила действует на заряд $Q$?',
            '12-00-my-3': r'Как изменятся ответы в предыдущих задачах, если увеличить заряд $Q$ в $2$ раза? Как при этом изменится отношение силы к заряду?',
            '12-04': r'Передаётся ли действие заряженных тел друг на друга в вакууме?',
            '12-08': r'Как с помощью электрического поля описать взаимодействие электрических зарядов?',
            '12-10': r'Вокруг электрона существует электрическое поле? Вокруг нейтрона? А протона?',
            '12-00-my-4': r'Изобразите электрическое поле вокруг точечного заряда $q$. На отдельном рисунке изобразите поле вокруг заряда $2q$.',
            '12-00-my-5': r'Изобразите электрическое поле вокруг двух точечных зарядов по $q$ каждый, расположенных на расстоянии $d$. Как «выглядит» это поле на расстоянии $L\gg d$?',
            '12-00-my-6': r'Изобразите электрическое поле вокруг двух точечных зарядов: $q$ и $-q$, расположенных на расстоянии $d$.',
            '12-00-my-7': r'''
                Изобразите электрическое поле вокруг равномерно заряженной
                \begin{itemize}
                    \item сферы;
                    \item плоскости;
                    \item прямой.
                \end{itemize}
            ''',
            '12-00-my-8': r'На координатной плоскости в точке $(d, 0)$ находится заряд $Q$, а в точке $(-d, 0)$ — $-Q$. Сделайте рисунок и определите величину и направление напряжённости электрического поля в точках $(0, 0)$, $(0, -d)$, $(0, d)$, $(2d, 0)$, $(-3d, 0)$.',
            '12-00-my-9': r'$ABCD$ — квадрат со стороной $a$. В вершинах $A$ и $B$ находятся по заряду $q$, в вершинах $C$ и $D$ — по $-q$. $U$ — середина $AD$, $V$ — середина $CD$, $S$ — центр квадрата. Сделайте рисунок и определите величину и направление напряжённости электрического поля в точках $S$, $U$ и $V$.',
        }
        for number, text in tasks.items():
            yield task.Task(text, number=number)
