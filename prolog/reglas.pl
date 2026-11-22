% estado_stock(Stock, Minimo, Estado)
% sin_stock si ya no queda, stock_bajo si quedan pocos, ok si esta bien
estado_stock(Stock, _, sin_stock) :-
    Stock =< 0, !.
estado_stock(Stock, Minimo, stock_bajo) :-
    Stock =< Minimo, !.
estado_stock(_, _, ok).

% reponer(Stock, Minimo, Estado)
% se cumple cuando hay que volver a comprar el producto
reponer(Stock, Minimo, Estado) :-
    estado_stock(Stock, Minimo, Estado),
    Estado \== ok.

% revisar(Lista)
% recorre la lista de item(Numero, Stock, Minimo) y escribe los que hay que reponer
revisar([]).
revisar([item(N, Stock, Minimo) | Resto]) :-
    reponer(Stock, Minimo, Estado), !,
    write(N), write(' '), write(Estado), nl,
    revisar(Resto).
revisar([_ | Resto]) :-
    revisar(Resto).
