'''
This module implements the Bayesian network shown in the text, Figure 14.2.
It's taken from the AIMA Python code.

@author: kvlinden
@version Jan 2, 2013
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# From AIMA code (probability.py) - Fig. 14.2 - burglary example
happiness = BayesNet([
    ('Sunny', '', 0.7),
    ('Raise', '', 0.01),
    ('Happy', 'Sunny Raise', {(T, T): 1.0, (T, F): 0.7, (F, T): 0.9, (F, F): 0.1})
    ])

"""
5.3.a.i
P(Raise | sunny)
= P(Raise)
= <0.01, 0.99>

If we assume that weather doesn't affect the probability of the agent getting a raise, then it is <0.01, 0.99>.
"""
print("P(Raise | sunny): ", enumeration_ask('Raise', dict(Sunny=T), happiness).show_approx())

"""
5.3.a.ii
P(Raise | happy ^ sunny)
= alpha * P(happy ^ sunny | Raise) * P(Raise)
= alpha * P(happy | sunny, Raise) * P(sunny) * P(Raise)
= alpha * <(1.0 * 0.7 * 0.01), (0.7 * 0.7 * 0.99)>
= alpha * <0.007, 0.4851>
= <0.0142, 0.9858>
"""
print("P(Raise | happy ^ sunny): ", enumeration_ask('Raise', dict(Happy=T, Sunny=T), happiness).show_approx())


"""
5.3.b.i
P(Raise | happy)
= alpha * <P(happy | raise, Sunny) * P(raise) * P(Sunny), P(happy | -raise, Sunny) * P(-raise) * P(Sunny)>
= alpha * <(1.0 * 0.01 * 0.7 + 0.9 * 0.01 * 0.3), (0.7 * 0.99 * 0.7 + 0.1 * 0.99 * 0.3)>
= alpha * <0.0097, 0.5148>
= <0.0185, 0.9815>
"""
print("P(Raise | happy): ", enumeration_ask('Raise', dict(Happy=T), happiness).show_approx())


"""
5.3.b.ii
P(Raise | happy ^ -sunny)
= alpha * P(happy ^ -sunny | Raise) * P(Raise)
= alpha * P(happy | -sunny, Raise) * P(-sunny) * P(Raise)
= alpha * <(0.9 * 0.3 * 0.01), (0.1 * 0.3 * 0.99)>
= alpha * <0.0027, 0.0297)>
= <0.0833, 0.9167>
"""
print("P(Raise | happy ^ -sunny): ", enumeration_ask('Raise', dict(Happy=T, Sunny=F), happiness).show_approx())

"""
The results make sense. The prior probability of a raise is 0.01, but if the agent is happy, the probability of a raise
has now increased to 0.0185. However, if peeking out the window it is sunny, then their happiness could be from
the sunny weather, so that lowers the raise probability slightly. But if it is not sunny outside and the agent is still 
happy -- the happiness didn't get explained away by the weather -- it becomes much more likely that they are happy because
of a raise.

"""