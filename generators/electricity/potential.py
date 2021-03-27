import generators.variant as variant


@variant.text('''
    В однородном электрическом поле напряжённостью {E:Task:e}
    переместили заряд {q:Task:e} в направлении силовой линии
    на {l:Task:e}. Определите работу поля, изменение потенциальной энергии заряда,
    напряжение между начальной и конечной точками перемещения.
''')
@variant.answer_short('''
    A   = {E:L}{q:L}{l:L}
        = {E:Value} * {q:Value} * {l:Value}
        = {A:.2f} * 10^{ -7 } \\units{ Дж }
''')
@variant.arg(q=['%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [-10, 10, -25, 25, -40, 40]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [2, 4, 5, 10]])
@variant.arg(E=['E = %d кВ / м' % ev for ev in [2, 4, 20]])
class Potential728(variant.VariantTask):  # 728(737) - Rymkevich
    def GetUpdate(self, l=None, q=None, E=None, **kws):
        return dict(
            A=1. * E.Value * q.Value * l.Value,
        )


@variant.text('''
    Напряжение между двумя точками, лежащими на одной линии напряжённости однородного электрического поля,
    равно {U:Task:e}. Расстояние между точками {l:Task:e}.
    Какова напряжённость этого поля?
''')
@variant.arg(U=['%s = %d кВ' % (ul, uv) for ul in ['U', 'V'] for uv in [2, 3, 4, 5, 6]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [10, 20, 30, 40]])
class Potential735(variant.VariantTask):  # 735(737) - Rymkevich
    pass


@variant.text('''
    Найти напряжение между точками $A$ и $B$ в однородном электрическом поле (см. рис. на доске), если
    $AB={l:Task}$,
    ${alpha:L}={alpha:Value}^\\circ$,
    {E:Task:e}.
    Потенциал какой из точек $A$ и $B$ больше?
''')
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [4, 6, 8, 10, 12]])
@variant.arg(alpha=['%s = %d' % (al, av) for al in ['\\alpha', '\\varphi'] for av in [30, 45, 60]])
@variant.arg(E=['E = %d В / м' % ev for ev in [30, 50, 60, 100, 120]])
class Potential737(variant.VariantTask):  # 737(739) - Rymkevich
    pass


@variant.text('''
    При какой скорости электрона его кинетическая энергия равна $E_\\text{ к } = {E:Value}?$
''')
@variant.arg(E=['E = %d эВ' % E for E in [4, 8, 20, 30, 40, 50, 200, 400, 600, 1000]])
class Potential2335(variant.VariantTask):  # 2335 Gendenshteyn
    pass


@variant.text('''
    Электрон $e^-$ вылетает из точки, потенциал которой {V:Task:e},
    со скоростью {v:Task:e} в направлении линий напряжённости поля.
    Будет поле ускорять или тормозить электрон?
    Каков потенциал точки, дойдя до которой электрон остановится?
''')
@variant.arg(v=['v = %d000000 м / с' % vv for vv in [3, 4, 6, 10, 12]])
@variant.arg(V=['\\varphi = %d В' % Vv for Vv in [200, 400, 600, 800, 1000]])
class Potential1621(variant.VariantTask):  # 1621 Goldfarb
    pass
