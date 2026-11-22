% Revisa el stock de un producto y devuelve su estado
estado_stock(_, Stock, _, sin_stock) :-
    Stock =< 0, !.

estado_stock(_, Stock, Minimo, stock_bajo) :-
    Stock > 0,
    Stock =< Minimo, !.

estado_stock(_, _, _, ok).

% Indica si hay que reponer el producto
reponer(Nombre, Stock, Minimo) :-
    estado_stock(Nombre, Stock, Minimo, Estado),
    (Estado = sin_stock ; Estado = stock_bajo).