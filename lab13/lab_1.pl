% Exercise 13.1
%
% Exercise 3.2
directlyIn(katarina, olga).
directlyIn(olga, natasha).
directlyIn(natasha, irina).
in(X, Y) :- directlyIn(X, Y).
in(X, Y) :- directlyIn(X, Z), in(Z, Y).


%Exercise 4.5
tran(eins, one).
tran(zwei, two).
tran(drei, three).
tran(vier, four).
tran(fuenf, five).
tran(sechs, six).
tran(sieben, seven).
tran(acht, eight).
tran(neun, nine).
listtran([], []).
listtran([G|Tg], [E|Te]) :- tran(G, E), listtran(Tg, Te).

% Does Prolog implement a version of generalized modus ponens (i.e., modus ponens with variables and instatiation)? If so, demonstrate how it’s done; if not, explain why not. If it doesn’t, can you implement one? Why or why not?

% Yes, Prolog implements generalized modus ponens. On top of modus
% ponens, Prolog can also support variables and instantiations. It is
% done with backward chaining, for a query involving a variable, Prolog
% searches in the knowledge base for values that unify with the
% variable. For recursively-defined predicates, it searches for values
% that would satisfy the first rule, and if not, it will keep searching
% until it finds one or reaches the end.
% The previous two exercises are examples of Prolog's implementation of
% generalized modus ponens.
