% CS 344 Lab 12
% Lab12_3

burn(X) :- witch(X). %a witch must be burned
burn(X) :- wood(X). %wood also burns
witch(X) :- wood(X). %witches are made of wood (which is why they burn, apparently, this is not a logical conclusion at all)
%woods float, and
floats(X) :- wood(X).
floats(X) :- duck(X). %ducks also float in water.
wood(X) :- duck(Y),sameWeight(X, Y). %if someone weighs the same as duck, they are made of wood. (this step made many incorrect jumps)
%therefore, she/he is a witch.

duck(anotherduck).
duck(aduck). %we have a duck
sameWeight(person, aduck). %we have someone who weighs the same as a duck.


% Running this program yields the result that person is indeed a witch.
