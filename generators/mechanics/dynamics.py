import generators.variant as variant


@variant.text('''
    {many} одинаковых брусков лежат на гладком горизонтальном столе. Масса каждого бруска равна {m:V:e},
    причём они пронумерованы от 1 до {N} и последовательно связаны между собой невесомыми 
    нерастяжимыми нитями: 1 со 2, 2 с 3 (ну и с 1) и т.д.
    Экспериментатор Глюк прикладывает постоянную горизонтальную силу {F:V:e} к бруску с {which} номером.
    С каким ускорением двигается система? Чему равна сила натяжения нити, связывающей бруски {i} и {j}?
''')
@variant.arg(many__N=[('Четыре', 4), ('Пять', 5), ('Шесть', 6)])
@variant.arg(which=['наибольшим', 'наименьшим'])
@variant.arg(i=[1, 2, 3])
@variant.arg(m=('m = {} кг', [2, 3]))
@variant.arg(F=('F = {} Н', [60, 90, 120]))
class Many_blocks(variant.VariantTask):
     def GetUpdate(self, many=None, N=None, which=None, i=None, **kws):
        return dict(
            j=i + 1,
        )


# \begin{tikzpicture}[x=0.65cm,y=0.65cm,semithick,decoration={
#   markings,   mark=between positions 0.07 and 0.9 step 11mm with {\arrow{stealth}}}
#   %,dash patern=on 5pt off 10pt
#   ]


@variant.text('''
    Два бруска связаны лёгкой нерастяжимой нитью и перекинуты через неподвижный блок (см. рис.).
    Определите силу натяжения нити и ускорения брусков. Силами трения пренебречь, массы брусков
    равны {m1:Task:e} и {m2:Task:e}.

    \\begin{ tikzpicture }[x=1.5cm,y=1.5cm,thick]
        \\draw 
            (-0.4, 0) rectangle (-0.2, 1.2)
            (0.15, 0.5) rectangle (0.45, 1)
            (0, 2) circle [radius=0.3] -- ++(up:0.5)
            (-0.3, 1.2) -- ++(up:0.8)
            (0.3, 1) -- ++(up:1)
            (-0.7, 2.5) -- (0.7, 2.5)
            ;
        \\draw[pattern={ Lines[angle=51,distance=3pt] },pattern color=black,draw=none] (-0.7, 2.5) rectangle (0.7, 2.75);
        \\node [left] (left) at (-0.4, 0.6) {m1:L:e:s};
        \\node [right] (right) at (0.4, 0.75) {m2:L:e:s};
    \\end{ tikzpicture }
''')
@variant.arg(m1=('m_1 = {} кг', [5, 8, 11]))
@variant.arg(m2=('m_2 = {} кг', [4, 6, 10, 14]))
class Two_blocks_on_block(variant.VariantTask):
    pass

