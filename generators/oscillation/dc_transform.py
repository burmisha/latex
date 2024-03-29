import generators.variant as variant


@variant.text('''
    Напряжение на концах участка цепи, по которому течет переменный ток, изменяется со временем
    по закону: И = Изз(ё + 21/3). В момент времени ё = Т/12 мгновенное значение напряжения равно 9 В.
    Определите амплитуду напряжения.
''')
@variant.solution_space(100)
class Chernoutsan_12_53(variant.VariantTask):
    pass


@variant.text('''
    Напряжение, при котором зажигается или гаснет неоновая лампа, включенная в сеть переменного тока,
    соответствует действующему значению напряжения этой сети. В течение каждого полупериода лампа горит 2/3 мс.
    Найдите частоту переменного тока.
''')
@variant.solution_space(100)
class Chernoutsan_12_54(variant.VariantTask):
    pass


@variant.text('''
    Сила тока в первичной обмотке трансформатора {I_1:V:e}, напряжение на её концах {U_1:V:e}.
    Напряжение на концах вторичной обмотки {U_2:V:e}.
    Определите силу тока во вторичной обмотке. Потерями в трансформаторе пренебречь.
''')
@variant.solution_space(60)
@variant.arg(I_1='\\eli_1 = 2/3/4/5 А')
@variant.arg(U_1='U_1 = 120/220/320 В')
@variant.arg(U_2='U_2 = 20/40/60/80 В')
@variant.answer_short('{U_1:L}{I_1:L} = {U_2:L}{I_2:L} \\implies {I_2:L} = {I_1:L} * \\frac{U_1:L:s}{U_2:L:s} = {I_1:V} * \\frac{U_1:V:s}{U_2:V:s} \\approx {I_2:V}')
class Chernoutsan_12_55(variant.VariantTask):
    def GetUpdate(self, *, I_1=None, U_1=None, U_2=None):
        return dict(I_2=(I_1 * U_1 / U_2).SetLetter('\\eli_2'))


@variant.text('''
    Под каким напряжением находится первичная обмотка трансформатора, имеющая {N_1:V:e} витков,
    если во вторичной обмотке {N_2:V:e} витков и напряжение на ней {U_2:V:e}?
''')
@variant.solution_space(40)
@variant.arg(N_1='N_1 = 500/800/1200/1500')
@variant.arg(N_2='N_2 = 200/1000/2000')
@variant.arg(U_2='U_2 = 50/70/90/110/130/150 В')
@variant.answer_short('\\frac{U_2:L:s}{U_1:L:s}  = \\frac{N_2:L:s}{N_1:L:s} \\implies {U_1:L} = {U_2:L} * \\frac{N_1:L:s}{N_2:L:s} = {U_2:V} * \\frac{N_1:V:s}{N_2:V:s} \\approx {U_1:V}')
class Chernoutsan_12_56(variant.VariantTask):
    def GetUpdate(self, *, N_1=None, N_2=None, U_2=None):
        return dict(U_1=(U_2 * N_1 / N_2).SetLetter('U_1'))


@variant.text('''
    Сила тока в первичной обмотке трансформатора {I_1:V:e}, напряжение на её концах {U_1:V:e}.
    Сила тока во вторичной обмотке {I_2:V:e}, напряжение на её концах {U_2:V:e}.
    Определите {what} трансформатора.
''')
@variant.solution_space(60)
@variant.arg(I_1='\\eli_1 = 412/542/636/784/859/923 мА')
@variant.arg(U_1='U_1 = 200/250/300 В')
@variant.arg(I_2='\\eli_2 = 2.4/3.2/4.3/5.1 А')
@variant.arg(eta_base=[0.94, 0.95, 0.96, 0.97])
@variant.arg(what=['КПД', 'долю потерей'])
@variant.answer_short('\\eta = \\frac{ {U_2:L}{I_2:L} }{ {U_1:L}{I_1:L} } = \\frac{ {U_2:V} * {I_2:V} }{ {U_1:V} * {I_1:V} } \\approx {eta:V}, \\quad 1-\\eta \\approx {eta_minus:.3f}')
class Chernoutsan_12_57(variant.VariantTask):
    def GetUpdate(self, *, I_1=None, U_1=None, I_2=None, eta_base=None, what=None):
        U_2 = U_1 * I_1 / I_2 * eta_base
        eta = U_2 * I_2 / (U_1 * I_1)
        return dict(
            U_2=U_2.SetLetter('U_2'),
            eta=eta.IncPrecision(1),
            eta_minus=1 - eta.SI_Value,
        )


@variant.text('''
    Первичная обмотка силового трансформатора для накала радиолампы имеет 2200 витков
    и включена в сеть с напряжением 220 В. Какое количество витков должна иметь вторичная обмотка,
    если её активное сопротивление 0,5 Ом, а напряжение накала лампы 3,5 В при силе тока накала | А?
''')
@variant.solution_space(100)
class Chernoutsan_12_58(variant.VariantTask):
    pass


@variant.text('''
    К генератору переменного тока подключена электропечь, сопротивление которой 200 Ом.
    За 5 минут работы печи в ней выделяется 270 кДж теплоты.
    Какова при этом амплитуда силы тока, проходящего через печь?
''')
@variant.solution_space(100)
class Chernoutsan_12_59(variant.VariantTask):
    pass


@variant.text('''
    Во сколько раз уменьшится индуктивное сопротивление катушки,
    если её включить в цепь переменного тока с частотой 50 Гц вместо 10 кГц?
''')
@variant.solution_space(100)
class Chernoutsan_12_60(variant.VariantTask):
    pass


@variant.text('''
    При какой циклической частоте переменного тока наступит резонанс напряжений в замкнутой цепи,
    состоящей из катушки с индуктивностью 0,5 Гн и конденсатора емкостью 200 мкФ?
''')
@variant.solution_space(100)
class Chernoutsan_12_61(variant.VariantTask):
    pass
