a = '''
\begin{tikzpicture}[circuit ee IEC, x=1.8cm,y=1.8cm,semithick]

    \node [contact] (left) at (1,1) {};
    \node [contact] (top) at (2,1.5) {};
    \node [contact] (bottom) at (2,0.5) {};
    \node [contact] (right) at (3,1) {};

  \draw (left) to [resistor={info sloped={$\mathsf{R_1}$}}] (top)
                     to [resistor={info sloped={$\mathsf{R_2}$}}] (right) ;
  \draw (left) to [resistor={info' sloped={$\mathsf{R_3}$}}] (bottom)
                         to [resistor={info' sloped={$\mathsf{R_4}$}}] (right) ;
    \draw (bottom) to [make contact={info'={$\mathsf{K}$}}] (top);
    \draw (right) to ++(down:0.7) to ++(left:2.5) to ++(up:0.7)
                             to [battery={rotate=-180,info={$\mathscr{E},r$}}] (left);

  \node [right,text width = 10cm, align=justify]    at (3.3,1) {
  После замыкания ключа $\mathsf{K}$ суммарная мощность, выделяемая на резисторах $\mathsf{R_1, R_2, R_3, R_4}$, не изменилась. Сопротивления резисторов: $R_1=R_4=R, R_2=R_3=9R$. Определить сопротивление $r$ источника {\sl(5 баллов)}.
  };
\end{tikzpicture}
'''