% estado del stock de un producto
estado_stock(Stock, _, sin_stock) :-
    Stock =< 0, !.
estado_stock(Stock, Minimo, stock_bajo) :-
    Stock =< Minimo, !.
estado_stock(_, _, ok).

% si hay que reponer
reponer(Stock, Minimo, Estado) :-
    estado_stock(Stock, Minimo, Estado),
    Estado \== ok.

% escribe los que hay que reponer
revisar([]).
revisar([item(N, Stock, Minimo) | Resto]) :-
    reponer(Stock, Minimo, Estado), !,
    write(N), write(' '), write(Estado), nl,
    revisar(Resto).
revisar([_ | Resto]) :-
    revisar(Resto).
