import problems.task as task


class Gendenshteyn7(task.TasksGenerator):
    def GetBookName(self):
        return 'gendenshteyn-7'

    def __call__(self):
        tasks = {
            '18-01': r'Какие известные вам наблюдения и опыты показывают, что существует сила трения?',
            '18-02': r'Приведите примеры, показывающие, что трение может быть полезным.',
            '18-03': r'Приведите примеры, показывающие, что трение может быть вредным.',
            '18-04': r'Какие способы увеличения и уменьшения трения вы знаете?',
            '18-05': r'Почему нельзя переходить дорогу перед близко едущим автомобилем? Как изменяется ответ при гололёде и почему?',
            '18-06': r'Приведите примеры практического использования силы трения покоя.',
            '18-07': r'Чтобы представить, какую роль играют силы трения покоя, вообразим будто они исчезли. Какие вы могли бы заметить последствия?',
            '18-08': r'Что общего между гвоздём, вбитым в доску, и завязанными шнурками?',
            '18-09': r'Брусок скользит по горизонтальной плоскости вправо. Сделайте рисунок и изобразите силу трения. Что изменится, если брусок скользит влево?',
            '18-10': r'Брусок скользит вверх по наклонной плоскости. Сделайте рисунок и изобразите силу трения. Как изменится ответ при движении бруска вниз?',
            '18-11': r'Парашютист, масса которого $80\\units{кг}$, равномерно движется вниз. Чему равна сила сопротивления воздуха, действующая на парашют? Изобразите силы, действующие на парашютиста.',
            '18-12': r'Брусок массой $5\\units{кг}$ перемещают вдоль поверхности стола, прикладывая к нему горизонтальную силу. Какая сила трения действует на брусок, если коэффициент трения равен $0{,}4$?',
            '18-13': r'Когда брусок тянут вдоль поверхности стола, прикладывая силу $5\\units{Н}$, он равномерно скользит по столу. Чему равна сила трения, действующая при этом на брусок? Изобразите действующие на брусок силы.',
            '18-14': r'К телу, лежащему на горизонтальной поверхности стола, приложили силу $2\\units{Н}$, направленную горизонтально. Тело осталось в покое. В каком случае это возможно? Чему равна сила трения покоя в этом случае?',
            '18-15': r'Парашютист массой $70\\units{кг}$ опускается с раскрытым парашютом. Какова сила сопротивления воздуха при равномерном движении? Чему равна при этом равнодействующая приложенных к парашютисту сил? Чему равен вес парашютиста?',
            '18-16': r'Чтобы передвинуть шкаф, надо приложить к нему горизонтальную силу $300\\units{Н}$. Чему равен коэффициент трения между шкафом и полом, если масса шкафа равна $120\\units{кг}$?',
            '18-17': r'Ящик массой $40\\units{кг}$ стоит на полу. Коэффициент трения между дном ящика и полом равен $0{,}3$. Какую горизонтальную силу надо приложить к ящику, чтобы сдвинуть его с места?',
            '18-20': r'Когда трение вредно, его стремятся уменьшить, а когда полезно — увеличить. А вам приходилось это делать? Когда и как?',
            '18-24': r'К ножкам многих приборов (телевизоров, колонок, компьютеров) приклеены резиновые кружки. Зачем это сделано?',
            '18-25': r'Почему опасно ездить на автомобиле со старыми «лысыми» шинами?',
            '18-29': r'Передние или задние колёса автомобиля будут буксовать на скользкой дороге, если ведущими являются передние колёса?',
            '18-30': r'На стол положили книгу и шарик для настольного тенниса. Книга осталась неподвижной, а шарик покатился. Почему?',
            '18-31': r'Действует ли сила трения на стоящий в комнате шкаф? Если да, то какая именно, если нет, то почему?',
            '18-35': r'Деревянная лестница приставлена к стене. Укажите на рисунке все силы, действующие на лестницу.',
            '18-35-my': r'Может ли на тело действовать 2 силы трения? Могут ли они быть направлены при этом в разные стороны? А в одну?',
            '18-36': r'Два одинаковых набора одинаковых брусков сложены 2 разными способами: сцеплены или же лежат друг на друге. Одинаковую ли силу надо прикладывать в каждому набору, для равномерного движения грузов по поверхности стола?',
            '18-37': r'Какая горизонтальная сила нужна для равномерного перемещения саней по льду, если вес саней $4\\units{кН}$, а коэффициент трения саней о лёд равен $0{,}03$?',
            '18-39': r'Брусок массой $10\\units{кг}$ движется с постоянной скоростью по горизонтальной поверхности под действием горизонтальной силы $15\\units{Н}$. Определите коэффициент трения между бруском и поверхностью.',
            '18-40': r'Когда брусок тянут вдоль поверхности стола, прикладывая горизонтальную силу $5\\units{Н}$, он прямолинейно и равномерно скользит по столу. Какая сила трения при этом действует на брусок? Какой будет сила трения если к покоящемуся бруску приложить горизонтальную силу $3\\units{Н}$? А если $10\\units{Н}$?',
            '18-41': r'Брусок массой $2\\units{кг}$ лежит на столе, коэффициент трения между бруском и столом равен $0{,}3$. Какая сила трения действует на брусок, если к нему прикладывают горизонтальную силу $4\\units{Н}$? А если $8\\units{Н}$? А если $12\\units{Н}$?',
            '20-01-my': r'Зависит ли действие силы от площади опоры, на которую действует сила, или нет? Если да — приведите примеры, если нет — объясните почему?',
            '20-04': r'Почему человек, идущий на лыжах, не проваливается в снег?',
            '20-06': r'Зачем нужен напёрсток при шитье иголкой?',
            '20-08': r'По какой причине железнодородные рельсы укладывают на шпалы?',
            '20-09': r'Два человека одинаковой массы лежат: один на полу, другой на диване. Одинаковы ли силы давления этих людей на опоры? Одинаковы ли давления? Почему диван кажется более мягким чем пол?',
            '20-11': r'Выразите в паскалях давление: $0{,}05\tfracunits{Н}{}{см}{2}$, $2\\units{ГПа}$, $3\\units{кПа}$, $20\tfracunits{Н}{}{см}{2}$, $50\tfracunits{кН}{}{м}{2}$, $120\tfracunits{мН}{}{см}{2}$.',
            '20-12': r'Выразите в гектопаскалях и килопаскалях давление: $100000\\units{ГПа}$, $20000\\units{ГПа}$, $3200\\units{ГПа}$, $1400\\units{ГПа}$.',
            '20-13': r'Как силой в $5\\units{кН}$ оказать давление в $1\\units{кПа}$?',
            '20-14': r'Какое давление оказывает на пол стоящий человек, если его вес равен $600\\units{Н}$, а площадь двух подошв $300\dunits{см}2$?',
            '20-15': r'Каток, работающий на укладке шоссе, оказывает на него давление $400\\units{кПа}$. Площадь соприкосновения катка с шоссе $0{,}12\dunits{м}2$. Чему равен вес катка?',
            '20-16': r'Болотистый грунт выдерживает давление до $20\\units{кПа}$. Какую площадь опоры должна иметь гусеничная машина весом $15\\units{кН}$, чтобы пройти по такому грунту?',
            '20-17': r'Трактор массой $6000\\units{кг}$ имеет площадь опоры $2000\dunits{см}2$. Какое давление оказывает он на почву?',
            '20-18': r'При проигрывании грампластинки игла давит на неё с силой $0{,}27\\units{Н}$. Какое давление оказывает игла, если площадь её острия равна $0{,}0003\dunits{см}2$',
            '20-27': r'Какое давление оказывает на лёд конькобежец массой $60\\units{кг}$, если длина одного конька $40\\units{см}$, а ширина лезвия $3\\units{мм}$?',
            '20-30': r'Какова длина лыж, если стоящий лыжник массой $80\\units{кг}$ оказывает на снег давление $2{,}5\\units{кПа}$? Ширина одной лыжи $8\\units{см}$.',
            '20-30-my': r'Изменяется (и как и почему, если да) шанс провалиться в снег у стоящего на снегу человека при начале движения?',
            '20-33': r'Каким будет давление на грунт мраморной колонны объёмом $6\dunits{м}3$, если площадь её основания $1{,}5\dunits{м}2$?',
            '20-34': r'На полу лежит плита из бетона толщиной $25\\units{cм}$. Определите давление плиты на пол.',
            '20-36': r'Какой из двух одинаковых по объёму кубиков — медный или алюминиевый — оказывает на опору большее давление?',
            '20-37': r'Может ли тело, имеющее больший вес, чем другое тело, оказать на опору меньшее давление?',
            '20-38': r'Почему боксёры ведут бой в перчатках?',
            '20-39': r'На чашке пружинных весов лежит кирпич. Изменится ли показание весов, если его поставить на ребро?',
            '20-41': r'Каким было бы давление давление колёс вагонов на рельсы, если бы колёса и рельсы не деформировались при соприкосновении? Какой это вид деформации?',
            '20-42': r'Почему при постройке дома стараются одновременно довести все его стены до примерно одинаковой высоты?',
            '20-43': r'На столе стоит сплошной алюминиевый куб. Какова масса куба, если он оказывает на стол давление $2\\units{кПа}$?',
            '20-45': r'Высота алюминиевого цилиндра равна $10\\units{см}$. Какова высота медного цилиндра, если он оказывает на стол такое же давление?',
            '20-46': r'Металлический куб массой $54\\units{кг}$ оказывает на стол давление $19\\units{кПа}$. Из какого металла может быть изготовлен куб?',
            '20-47': r'Полый алюминиевый куб с длиной ребра $10\\units{см}$ оказывает на стол давление $1{,}3\\units{кПа}$. Какова толщина стенок куба?',
            '20-48': r'На столе одна на другой лежат 2 книги. Если меньшая лежит сверху, давление на стол равно $300\\units{Па}$, а если меньшая книга внизу, давление равно $1\\units{кПа}$. Размеры меньшей книги $15\\units{см} \times 20\\units{см}$. Ширина большей книги $25\\units{см}$. Какова длина большей книги?',
            '20-49': r'На столе стоят один на другом два однородных куба, длины рёбер которых отличаются в 2 раза. Каково отношение плотностей материалов, из которых сделаны кубы, если верхний куб оказывает такое же давление на нижний, как нижний на стол?',
            '13-01': r'Плотность свинца равна $11\,300\tfracunits{кг}{}{м}{3}$. Что это означает?',
            '13-02': r'Плотность какого вещества больше — чугуна или меди? бетона или стали? масла или воды?',
            '13-04': r'Три кубика — из алюминия, льда и меди — имеют одинаковый объём. Какой из них имеет самую большую массу, а какой — самую маленькую?',
            '13-06': r'Найдите ошибку в рассуждениях: плотность $1\dunits{м}3$ нефти равна $800\tfracunits{кг}{}{м}{3}$, поэтому плотность $2\dunits{м}3$ нефти равна $1600\tfracunits{кг}{}{м}{3}$.',
            '13-09': r'Какое вещество у вас дома имеет наибольшую (наименьшую) плотность?',
            '13-14': r'Вместимость цистерны $60\dunits{м}3$. Сколько тонн нефти можно в ней хранить?',
            '13-15': r'Чему равна плотность жидкости, $125\\units{л}$ которой имеют массу $100\\units{кг}$?',
            '13-17': r'Чугунная деталь имеет объём $1{,}8\dunits{см}3$. Какой объём будет иметь алюминиевая деталь той же массы?',
            '13-18': r'Какова плотность металла, $15\\units{г}$ которого имеют объём $2\dunits{см}3$?',
            '13-19': r'Действительно ли обручальное кольцо $0{,}5\dunits{см}3$ и массой $8\\units{г}$ может быть золотым?',
            '13-24': r'В каком случае кусок пробки и кусок стали будут иметь одинаковую массу?',
            '13-27': r'Одна бочка заполнена водой, а другая керосином. Диаметр какой бочки больше, если уровень и масса обеих жидкостей одинаковы?',
            '13-38': r'Чтобы принести $10\\units{кг}$ воды, необходимо ведро. Для какой жидкости при той же массе хватило бы литровой бутылки?',
            '15-02': r'Приведите примеры изменения скорости тела вследствие действия на него другого тела.',
            '15-03': r'Как будет двигаться тело под действием двух равных по модулю противоположно направленных сил?',
            '15-04': r'Что можно сказать о скорости тела, к которому не приложена никакая сила ($F = 0$)?',
            '15-05': r'Взяв масштаб $1\\units{см}$ — $40\\units{Н}$, изобразите графически силу $200\\units{Н}$, направленную на север.',
            '15-06-my': r'Взяв масштаб $1\\units{см}$ — $80\\units{Н}$, изобразите графически силу $400\\units{Н}$, направленную на запад.',
            '15-06': r'Взяв масштаб $1\\units{см}$ — $60\\units{Н}$, изобразите графически силу $240\\units{Н}$, направленную на юг.',
            '15-09': r'Может ли равнодействующая двух сил $2\\units{Н}$ и $10\\units{Н}$, действующих на тело быть равной $5\\units{Н}$, $12\\units{Н}$, $8\\units{Н}$, $20\\units{Н}$?',
            '15-11': r'''
                Что вы можете скахать о равнодействующей сил, действующих на автобус:
                \begin{itemize}
                    \item отходящий от остановки;
                    \item равномерно движущийся на прямолинейном участке дороги;
                    \item подходящий к остановке?
                \end{itemize}
            ''',
            '15-14': r'На шайбу во время игры постоянно действуют то лёд, то клюшка, то перчатки вратаря, то борт, то сетка ворот... В какие моменты действует наибольшая сила, а в какие наименьшая?',
            '15-15': r'''
                Изобразите и сравните силы, действующие на шарик в следующих случаях:
                \begin{itemize}
                    \item шарик лежит на горизонтальном столе;
                    \item шарик получает толчок от руки;
                    \item шарик катится по полу;
                    \item шарик падает со стола.
                \end{itemize}
            ''',
            '15-17': r'Какие две силы, направленные вдоль одной прямой, могут дать равнодействующую, модуль которой равен $10\\units{Н}$? Сделайте рисунки для 4 возможных случаев.',
            '15-19': r'Капля дождя движется вертикально вниз с постоянной скоростью. Изобразите все силы, действующие на каплю.',
            '15-20': r'''
                Два одинаковых автомобиля увеличили свою скорость каждый на $10\cfracunits{м}{}{c}{}$,
                но один за~—\ounits{20}{с}, а другой — за~—\ounits{40}{с}.
                На какой из автомобилей действовала большая сила во время разгона?
                Обоснуйте свой ответ. Важно ли, что автомобили были одинаковые?
            ''',
            '15-23': r'Может ли тело двигаться вверх, если равнодействующая всех сил, приложенных к нему, направлена вниз? Если да, приведите пример.',
            '15-24': r'Равнодействующая всех сил, приложенных к телу, направлена вертикально вниз. Можно ли указать направление движения тела? Приведите пример, подтверждающий ваш ответ.',
            '15-25-my': r'''
                К телу приложены 4 силы по $15\\units{Н}$ каждая, направленные вдоль одной прямой.
                Какой может быть по модулю равнодействующая этих сил?
                Изобразите на рисунке все возможные случаи.
            ''',
            '15-25': r'''
                К телу приложены 3 силы по $10\\units{Н}$ каждая, направленные вдоль одной прямой.
                Какой может быть по модулю равнодействующая этих сил?
                Изобразите на рисунке все возможные случаи.
            ''',
            '15-26': r'К телу приложены 3 силы, направленные вдоль одной прямой: $3\\units{Н}$, $12\\units{Н}$, $6\\units{Н}$. Какой может быть равнодействующая этих сил? Сделайте рисунки для каждого из возможных случаев.',
            '15-27': r'''
                На тело действуют три силы $\vec F_1$, $\vec F_2$ и $\vec F_3$,
                направленные вдоль одной прямой, причём $F_1 = 3\\units{H}$, $F_2 = 5\\units{H}$.
                Чему равна $F_3$, если равнодействующая всех трёх сил равна  $10\\units{Н}$.
                Сколько решений имеет эта задача?
                Сделайте в тетради схематические рисунки, соответствующие каждому из решений.
            ''',
            '16-06': r'Какие силы взимодействия молекул воды в глубинах океана больше: силы притяжения или отталкивания? А на поверхности океана? А у полекул воздуха на высоте \ounits{8000}{м}?',
            '21-01': r'Как передают давление жидкости и газы? Почему это происходит?',
            '21-02': r'Изменится ли давление на дно кастрюли, если перелить воду из узкого стакана в широкую кастрюлю?',
            '21-03': r'В сосуде с водой растворили поваренную соль. Изменится ли давление на дно сосуда?',
            '21-05': r'Почему воздушные шарики и мыльные пузыри круглые?',
            '21-09': r'Используя закон Паскаля, объясните, почему зубную пасту легко выдавить из тюбика?',
            '21-10': r'Мяч, вынесенный зимой из комнаты на улицу, становится слабо надутым. Почему?',
            '21-13': r'Какое давление на дно сосуда оказывает слой керосина высотой $40\\units{см}?$',
            '21-14': r'Водолаз в жёстком скафандре может погружаться на глубину $250\\units{м}$, а опытный ныряльщик — на $20\\units{м}$. Определите давление воды на этих глубинах.',
            '21-15': r'На какой глубине давление воды в море $824\\units{кПа}$?',
            '21-16': r'Давление столба жидкости высотой $12\\units{см}$ равно $852\\units{Па}$. Определите плотность жидкости.',
            '21-17': r'Какое давление должен создавать насос, чтобы поднимать воду на $60\\units{м}$?',
            '21-18': r'Какова глубина бассейна, если давление воды на его дно равно $80\\units{кПа}$?',
            '21-19': r'Длина аквариума, полностью заполненного водой, $40\\units{см}$, ширина $20\\units{см}$, глубина $30\\units{см}$. С какой силой вода давит на дно аквариума? Чему равно давление воды на дно? Как изменился бы ответ, если бы аквариум был заполнен лишь на треть?',
            '21-20': r'В мензурке находятся три слоя жидкостей (машинное масло, вода и ртуть) толщиной по $10\\units{см}$. Каково давление на дно?',
            '21-25': r'Каким образом с помощью небольшого количества воды можно создать большое давление?',
            '21-28': r'Опишите поведение молекул газа в закрытом сосуде. Что происходит с молекулами, когда они подлетают к стенкам сосуда?',
            '21-29': r'''
                Изменится ли давление воды на дно ведра, если в воду опустить мяч? Рассмотрите 2 случая:
                \begin{itemize}
                    \item ведро заполнено доверху,
                    \item ведро заполнено наполовину.
                \end{itemize}
            ''',
            '21-30': r'Масса одного и того же газа в двух одинаковых закрытых сосудах одинакова. Один из этих сосудов находится в тёплом помещении, а другой — в холодном. В каком из сосудов давление газа больше? Почему?',
            '21-32': r'Число молекул газа, находящего в закрытом сосуде, при нагревании не увеличивается. Почему же тогда давление газа в сосуде растёт?',
            '21-34': r'Когда на открытой площадке стало слишком жарко, волейболисты першли в прохладный зал. Придётся подкачивать мяч или выпускать из него часть воздуха? Если придётся то почему?',
            '21-36': r'Определите силу давления нефти на пробку площадью $10\dunits{см}2$ на дне цистерны, если высота нефти $1{,}5\\units{м}$.',
            '21-39': r'В циллиндрическую мензурку высотой $45\\units{см}$ налиты ртуть, вода и керосин. Объёмы всех жидкостей одинаковы, жидкости не смешиваются между собой и полностью заполняют мензурку. Найдите давление на дно.',
            '21-41': r'Каково давление воды на дно в точках $A, B, C$ (см. рис на доске)?',
            '22-24': r'Ополосните горячей водой пластиковую бутылку и плотно закройте её крышкой. Как изменится формы бутылки?',
            '22-25': r'Ополосните горячей водой пластиковую бутылку, переверните её и опустите горловиной в сосуд с водой. Почему вода поднимается в бутылку?',
            '22-27': r'На какой глубине давление в озере равно $300\\units{кПа}$?',
            '22-28': r'Каково давление в море на глубине $800\\units{м}$?',
            '22-29': r'Какова высота небоскрёба, если у его входа барометр показывает $760\\units{мм рт. ст.}$, а на крыше — $745\\units{мм рт. ст.}$. Температура воздуха $0\celsius$.',
            '22-29-1': r'Какое давление соответствует $1\\units{мм рт. ст.}$?',
            '22-29-2': r'Переведите в мм рт. ст. следующие давления: $760\\units{кПа}$, $3800\\units{Па}$, $285\\units{Па}$, $190\\units{кПа}$.',
        }
        for number, text in tasks.items():
            yield task.Task(text, number=number)

        yield task.Task(r'Какая жидкость имеет плотность $0{,}79\tfracunits{г}{}{см}{3}$?', number='13-03', answer=r'Ацетон (в учебнике ошибка)')
        yield task.Task(r'Масса медного чайника равна $1{,}32\\units{кг}$. Определите массу такого же по форме и размерам чайника из алюминия.', answer=r'$0{,}40045\\units{кг}$', number='13-16')
        yield task.Task(r'Найдите массу бензина в бутылке объёмом $2\\units{л}$.', number='13-21', answer=r'$1{,}5\\units{кг}$')
        yield task.Task(r'Найдите массу ртути, налитой доверху во флакон ёмкостью $50\\units{мл}$.', number='13-22', answer=r'$677{,}3\\units{г}$')
        yield task.Task(r'Стальной и алюминиевый стержни имеют одинаковые диаметр и массу. Какой из них длиннее?', number='13-26', answer=r'Алюминиевый')
        yield task.Task(r'Определите массу оконного стекла длиной $60\\units{см}$, высотой $50\\units{см}$ и толщиной $0{,}5\\units{см}$.', number='13-33', answer=r'$3{,}75\\units{кг}$')
        yield task.Task(r'Определите массу рулона алюминевой фольги толщиной $0{,}15\\units{мм}$. Если размотать рулон, то получим ленту размером $0{,}2\\units{м} \times 15\\units{м}$.', number='13-34', answer=r'$1{,}215\\units{кг}$')
        yield task.Task(r'Грузовая машина привезла $1{,}5\\units{т}$ сухого песка. Какую площадь двора можно засыпать этим песком, если толщина слоя будет равна $5\\units{см}$?', number='13-41', answer=r'$20\dunits{м}2$')
        yield task.Task(r'Для получения латуни сплавили кусок цинка массой $178\\units{кг}$ и кусок меди массой $357\\units{кг}$. Определите плотность латуни.', number='13-57', answer=r'$8{,}207\tfracunits{кг}{}{м}{3}$')  # неправильное условие в задачнике
        yield task.Task(r'В кусок льда вмёрз стальной шарик. Объём образовашегося тела $50\dunits{см}3$, масса $114\\units{г}$. Найдите объём и массу шарика.', number='13-61', answer=r'$78{,}0\\units{г}$')
        yield task.Task(r'Плотность пластмассы $2000\tfracunits{кг}{}{м}{3}$.Какова плотность вспененного материала, изготовленного из этой пластмассы, если объём воздушных полостей в материале в три раза превышает объём самой пластмассы?', number='13-62', answer=r'$500\tfracunits{кг}{}{м}{3}$')
        yield task.Task(r'Три силы направлены вдоль одной прямой. В зависимости от направления этих сил их равнодействующая может быть равна $1\\units{Н}$, $2\\units{Н}$, $3\\units{Н}$, $4\\units{Н}$. Чему равна каждая из этих сил?', number='15-28', answer=r'0,5, 1, 2,5')
