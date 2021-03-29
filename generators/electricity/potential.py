import generators.variant as variant


@variant.solution_space(80)
@variant.text('''
    В однородном электрическом поле напряжённостью {E:Task:e}
    переместили заряд {q:Task:e} в направлении силовой линии
    на {l:Task:e}. Определите 
    \\begin{{itemize}}
        \\item работу поля,
        \\item изменение потенциальной энергии заряда.
        % \\item напряжение между начальной и конечной точками перемещения.
    \\end{{itemize}}
''')
@variant.answer_short('''
    A   = {E:L}{q:L}{l:L}
        = {E:Value} * {q:Value} * {l:Value}
        = {A:.2f} * 10^{ -7 } \\units{ Дж }
''')
@variant.arg(q=['%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [-10, 10, -25, 25, -40, 40]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [2, 4, 5, 10]])
@variant.arg(E=['E = %d кВ / м' % ev for ev in [2, 4, 20]])
class A_from_Q_E_l(variant.VariantTask):  # Рымкевич 728(737)
    def GetUpdate(self, l=None, q=None, E=None, **kws):
        return dict(
            A=1. * E.Value * q.Value * l.Value,
        )


@variant.solution_space(40)
@variant.text('''
    Напряжение между двумя точками, лежащими на одной линии напряжённости 
    однородного электрического поля, равно {U:Task:e}. 
    Расстояние между точками {l:Task:e}. Какова напряжённость этого поля?
''')
@variant.arg(U=['%s = %d кВ' % (ul, uv) for ul in ['U', 'V'] for uv in [2, 3, 4, 5, 6]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [10, 20, 30, 40]])
class E_from_U_l(variant.VariantTask):  # Рымкевич 735(737)
    pass


@variant.text('''
    Найти напряжение между точками $A$ и $B$ в однородном электрическом поле 
    (см. рис. на доске), если $AB={l:Task}$, ${alpha:L}={alpha:Value}^\\circ$,
    {E:Task:e}. Потенциал какой из точек $A$ и $B$ больше?
''')
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [4, 6, 8, 10, 12]])
@variant.arg(alpha=['%s = %d' % (al, av) for al in ['\\alpha', '\\varphi'] for av in [30, 45, 60]])
@variant.arg(E=['E = %d В / м' % ev for ev in [30, 50, 60, 100, 120]])
class Potential737(variant.VariantTask):  # Рымкевич 737(739)
    pass


@variant.solution_space(40)
@variant.text('При какой скорости {what} его кинетическая энергия равна {E:Task:e}?')
@variant.arg(E=('E_\\text{{ к }} = {} эВ', [4, 8, 20, 30, 40, 50, 200, 400, 600, 1000]))
@variant.arg(what=['электрона', 'позитрона'])
class v_from_Ev_m(variant.VariantTask):  # 2335 Gendenshteyn
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
