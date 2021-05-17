import generators.variant as variant


@variant.solution_space(80)
@variant.text('''
	Определите силу, действующую на {which} опору однородного горизонтального стержня длиной {l:Task:e}
	и массой {M:Task:e}, к которому подвешен груз массой {m:Task:e} на расстоянии {b:V:e} от правого конца (см. рис.).

    \\begin{ tikzpicture }[thick]
        \\draw 
            (-2, -0.1) rectangle (2, 0.1)
            (-0.5, -0.1) -- (-0.5, -1)
            (-0.7, -1) rectangle (-0.3, -1.3)
       		(-2, -0.1) -- +(0.15,-0.9) -- +(-0.15,-0.9) -- cycle
        	(2, -0.1) -- +(0.15,-0.9) -- +(-0.15,-0.9) -- cycle
        ;
        \\draw[pattern={ Lines[angle=51,distance=2pt] },pattern color=black,draw=none]
        	(-2.15, -1.15) rectangle +(0.3, 0.15)
        	(2.15, -1.15) rectangle +(-0.3, 0.15)
        ;
        \\node [right] (m_small) at (-0.3, -1.15) {m:L:e:s};
        \\node [above] (M_big) at (0, 0.1) {M:L:e:s};
    \\end{ tikzpicture }
''')
@variant.arg(which=['левую', 'правую'])
@variant.arg(m=('m = {} кг', [2, 3, 4]))
@variant.arg(M=('M = {} кг', [1, 5]))
@variant.arg(a=('a = {} м', [1, 3, 5]))
@variant.arg(b=('b = {} м', [2, 4]))
class Sterzhen(variant.VariantTask):
    def GetUpdate(self, which=None, m=None, M=None, a=None, b=None, **kws):
        return dict(
            l='l = %d м' % (a.Value + b.Value)
        )
