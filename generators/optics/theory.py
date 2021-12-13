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
class Task03(variant.VariantTask):
    pass


@variant.text('''
    Cформулируйте принцип Гюйгенса-Френеля, запишите формулой закон {q}
    и выведите из принципа этот закон.
''')
@variant.solution_space(80)
@variant.arg(q='преломления/отражения')
class Task04(variant.VariantTask):
    pass
