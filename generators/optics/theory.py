import generators.variant as variant


@variant.text('''
    Сформулируйте:
    \\begin{itemize}
        \\item принцип Гюйгенса-Френеля,
        \\item закон {q2} (в двух частях).
    \\end{itemize}
''')
@variant.solution_space(60)
@variant.arg(q2='преломления/отражения')
class HuygensFresnel_NoProof(variant.VariantTask):
    pass


@variant.text('''
    Cформулируйте принцип Гюйгенса-Френеля, запишите формулой закон {q}
    и выведите из принципа этот закон.
''')
@variant.solution_space(80)
@variant.arg(q='преломления/отражения')
class HuygensFresnel_WithProof(variant.VariantTask):
    pass


@variant.text('''
    Для закона {q}:
    \\begin{itemize}
        \\item сделайте рисунок,
        \\item отметьте все необходимые углы и подпишите их названия,
        \\item запишите этот закон формулой.
    \\end{itemize}
''')
@variant.solution_space(80)
@variant.arg(q='преломления/отражения')
class RefrReflLaws(variant.VariantTask):
    pass
