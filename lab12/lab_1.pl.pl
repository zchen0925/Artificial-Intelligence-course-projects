% Exercise 1.4
% Lab 12
%
killer(butch). %killer(butch) follows the prolog syntax to make an identity statement about him. All names in prolog are lower-case.
married(mia, marsellus). %this says mia married marsellus. the eciprocity is implied in real-life, but in prolog to be inclusive another statement, married(marsellus, mia) should be included.
dead(zed).
kills(marsellus, X) :- givesfootMassage(X, mia).
% if the body of a rule is true, the head will be true. this reflects
% the original sentence: if anyone gives mia a foot massage, marsellus
% will kill them.
loves(mia, X) :- goodDancer(X).
eats(jules, X) :- nutritious(X); tasty(X).
%or is represented by ";" in prolog.

% Exercise 1.5
% wizard(ron): true
% this fact is stored in the knowledge base
% witch(ron): false
% witch is undefined
% wizard(hermione): false
% hermione is unknown in the knowledge base
% witch(hermione): false
% hermione is unknown in the knowledge base
% wizard(harry): true
% the rule states that if someone both has a wand and a broom, then they are a wizard. harry is a quidditch player which means he has a broom, and it is also stated he has a wand. it follows that he is a wizard.
% wizard(Y): false
% there is no rule that says everybody is a wizard
% witch(Y): false
% there is no rule that says everyone is a witch


% b: modus ponens
% Prolog does implement a version of modus ponens in propositional
% logic form. A rule of the form head :- body allows Prolog to infer the
% truth status of head based on the truth status of body. For example,
% ?- head will yield to true if and only if head :- body and body. This
% is equivalent to q if and only if p -> q and p, in which p is
% Prolog's body and q is the head.

% c: horn clauses
% Prolog represents Horn clauses in head :- body rules. Horn clauses are
% a disjunction of literals with at most one positive literal. The one
% positive literal is the head, and the rest negated disjuncted literals
% are the body, which in Prolog the body can be expressed as disjunction
% of negated properties or conjunction of properties. I think Prolog has
% stronger representative power than the other format for Horn Clauses
% because it can be either disjunction or conjunction, and it is clear
% which is the head and which is the body at first glance.
%
%
% d: Prolog supports this distinction between TELL and ASK. It allows
% TELL in the format of property(X), which returns names that have that
% property. It implements queries in the form of property(name), which
% returns a true or false to complete the ASK.
