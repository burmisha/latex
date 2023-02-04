# 📚 LaTeX

[https://tex.stackexchange.com/questions/303917/replicating-geometry-drawing-in-tikz](https://tex.stackexchange.com/questions/303917/replicating-geometry-drawing-in-tikz)

[https://www.overleaf.com/learn/latex/LaTeX_Graphics_using_TikZ:_A_Tutorial_for_Beginners_(Part_2)—Generating_TikZ_Code_from_GeoGebra](https://www.overleaf.com/learn/latex/LaTeX_Graphics_using_TikZ:_A_Tutorial_for_Beginners_(Part_2)%E2%80%94Generating_TikZ_Code_from_GeoGebra)

[https://www.overleaf.com/learn/latex/LaTeX_Graphics_using_TikZ:_A_Tutorial_for_Beginners_(Part_4)—Circuit_Diagrams_Using_Circuitikz](https://www.overleaf.com/learn/latex/LaTeX_Graphics_using_TikZ:_A_Tutorial_for_Beginners_(Part_4)%E2%80%94Circuit_Diagrams_Using_Circuitikz)

[Электрические схемы средствами LaTeX и TikZ](https://habr.com/ru/post/250541/)

[Всякие штуки в MetaPost](https://habr.com/ru/post/423571/)

[Оформление задач по физике, математике (рисование схем) : Околонаучный софт](https://dxdy.ru/post832675.html)

[I want to make a picture in physics with TikZ. Can you help me?](https://tex.stackexchange.com/questions/482206/i-want-to-make-a-picture-in-physics-with-tikz-can-you-help-me)

[What graphics packages are there for creating graphics in LaTeX documents?](https://tex.stackexchange.com/questions/205/what-graphics-packages-are-there-for-creating-graphics-in-latex-documents)

[Physics](https://ru.overleaf.com/learn/latex/Physics)

# Установка

0. Предполагаем, что у тебя Windows

1. Скачиваем MiKTeX с [http://www.miktex.org/download](http://www.miktex.org/download) (32/64-bit версию, в зависимости от системы). Запускаем и выбираем самую полную установку, какую только можно (никакой не basic). Ставим, это самый долгий процесс из всего: может занять минут 40-120, емнип.

2. [http://www.ghostscript.com/download/gsdnld.html](http://www.ghostscript.com/download/gsdnld.html) выбираем установщик из первой колонки (GNU лицензии) и ставим его.

3. [http://pages.cs.wisc.edu/~ghost/gsview/get49.htm](http://pages.cs.wisc.edu/~ghost/gsview/get49.htm) - не уверен, что нужно, но поставь.

4.1. [http://www.texniccenter.org/download/](http://www.texniccenter.org/download/) маленькая и кривенькая прога, но у меня работает. Качаем, ставим, запускаешь TexnicCenter и настраиваешь его:

— не пропускай ни один шаг настройки (кроме одного, вроде =) )

— попросит указать, где tex - проведи его во что-типа C:\Program Files\MiKTeX 2.9\miktex\bin

— попросит настроить профили экспорта в PDF - настрой (если AdobeReader X (т.е. 10), то надо прописать во вкладке профилей Viewer acroviewr10 вместо чего-то ).

4.2. Либо же [http://www.sublimetext.com/3](http://www.sublimetext.com/3) и [https://github.com/SublimeText/LaTeXTools](https://github.com/SublimeText/LaTeXTools) + установаить пакет к MikTeX cm-super!

Теперь интересное. Самые частые косяки, но и самые меня бесящие — с русскими буквами. Они либо без сглаживания,либо поиск по русским словам по результирующей pdf не работает. Для этого я использую профиль компиляции LaTeX -> PS -> PDF. У этого способа есть недостатки:

- проблемы с jpeg-ами, если ты их будешь вставлять себе в файл

- чуть более медленная сборка, но многим будет не критично.

Везде рекомендую использовать UTF-8 в качестве кодировки. Единственная причина использовать win-cp-1251 - автоматическая библиография. Увы, стандартный модуль для библиографии в LaTeX был написан до утверждения utf-8 и не поддерживает его. Есть более хорошие и современные средства, но мне так и не удалось их прикрутить к моему процессу работы. В результате, библиографию я всегда делал вручную.

## Ещё ссылки

[https://stackoverflow.com/questions/4998678/dde-control-texniccenter](https://stackoverflow.com/questions/4998678/dde-control-texniccenter)

[https://latex.org/forum/viewtopic.php?f=45&t=19420](https://latex.org/forum/viewtopic.php?f=45&t=19420)

[https://www.sumatrapdfreader.org/download-free-pdf-viewer.html](https://www.sumatrapdfreader.org/download-free-pdf-viewer.html)

[http://s.arboreus.com/2007/07/pdf-latex.html](http://s.arboreus.com/2007/07/pdf-latex.html) - cmap

[https://alvinalexander.com/blog/post/latex/two-simple-examples-using-latex-ifthen-package](https://alvinalexander.com/blog/post/latex/two-simple-examples-using-latex-ifthen-package)

### OS X

[http://www.tug.org/mactex/mactex-download.html](http://www.tug.org/mactex/mactex-download.html)

## Moar

[https://physics.stackexchange.com/questions/401/what-software-programs-are-used-to-draw-physics-diagrams-and-what-are-their-rel](https://physics.stackexchange.com/questions/401/what-software-programs-are-used-to-draw-physics-diagrams-and-what-are-their-rel)

[https://tex.stackexchange.com/questions/158668/nice-scientific-pictures-show-off](https://tex.stackexchange.com/questions/158668/nice-scientific-pictures-show-off)

[https://tex.stackexchange.com/questions/185744/how-do-i-include-postscript-graphics-in-a-latex-file](https://tex.stackexchange.com/questions/185744/how-do-i-include-postscript-graphics-in-a-latex-file)

[https://www.physicsoverflow.org/12471/software-programs-physics-diagrams-their-relative-merits](https://www.physicsoverflow.org/12471/software-programs-physics-diagrams-their-relative-merits)

[https://mccme.ru/~akopyan/](https://mccme.ru/~akopyan/)

[https://www.ibm.com/developerworks/ru/library/latex_styles_05/](https://www.ibm.com/developerworks/ru/library/latex_styles_05/)

[https://habr.com/ru/post/445066/](https://habr.com/ru/post/445066/)

[https://habr.com/ru/post/450088](https://habr.com/ru/post/450088)

[https://github.com/search?p=1&q=%D0%9F%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D1%8C+%D0%BE%D0%B1%D0%BA%D0%BB%D0%B0%D0%B4%D0%BE%D0%BA+%D0%BF%D0%BB%D0%BE%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%BA%D0%BE%D0%BD%D0%B4%D0%B5%D0%BD%D1%81%D0%B0%D1%82%D0%BE%D1%80%D0%B0&type=Code](https://github.com/search?p=1&q=%D0%9F%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D1%8C+%D0%BE%D0%B1%D0%BA%D0%BB%D0%B0%D0%B4%D0%BE%D0%BA+%D0%BF%D0%BB%D0%BE%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D0%BA%D0%BE%D0%BD%D0%B4%D0%B5%D0%BD%D1%81%D0%B0%D1%82%D0%BE%D1%80%D0%B0&type=Code)

[https://habr.com/ru/post/120401/](https://habr.com/ru/post/120401/)