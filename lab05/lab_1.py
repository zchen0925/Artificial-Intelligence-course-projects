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
burglary = BayesNet([
    ('Burglary', '', 0.001),
    ('Earthquake', '', 0.002),
    ('Alarm', 'Burglary Earthquake', {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
    ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
    ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
    ])



"""
 P(Alarm | burglary ^ - earthquake)
 = <P(a | b ^ -e), P(-a | b ^ -e)>
 = <0.94, 0.04>
"""
print("P(A | b ^ -e): ", enumeration_ask('Alarm', dict(Burglary=T, Earthquake=F), burglary).show_approx())

"""
 P(John | burglary ^ -earthquake)
 = <P(j | b ^ -e), P(-j | b ^ -e)>
 = <P(j, A, b, -e), p(-j, A, b, -e)>
 = P(J | A) * P(A | b ^ -e) * P(b) * P(-e)
 = <P(j | A) * P(A | b ^ -e) * P(b) * P(-e),     P(-j | A) * P(A | b ^ -e) * P(b) * P(-e)>
 = alpha * <P(j | A) * P(A| b ^ -e),   P(-j | A) * P(A | b ^ -e)>
 = alpha * < (0.90 * 0.94 + 0.05 * 0.06),     (0.10 * 0.94 + 0.95 * 0.06) >
 = alpha * <0.849,  0.151>
 = <0.849, 0.151>
"""
print("P(J | b ^ -e): ", enumeration_ask('JohnCalls', dict(Burglary=T, Earthquake=F), burglary).show_approx())

"""
P(Burglary | alarm)
= P(B, E, a)
= P(B) * P(E) * P(a|B, E)
= alpha * <P(b) * P(E) * P(a|b ^ E),   P(-b) * P(E) * P(a| -b ^ E)>
= alpha * < (0.001 * (0.002 * 0.95 + 0.998 * 0.94)),   (0.999 * (0.002 * 0.29 + 0.998 * 0.001))>
= <0.00094002, 0.001576422>
=~ <0.374, 0.626>
"""
print("P(B | a): ", enumeration_ask('Burglary', dict(Alarm=T), burglary).show_approx())

"""
P(Burglary | john ^ mary)
= alpha * P(B, E, A, j, m)
= alpha * P(B) * P(E) * P(A|B, E) * P(j | A) * P(m | A)
P(burglary | john ^ mary)
= alpha * P(b) * P(E) * P(A |b, E) * P(j | A) * P(m | A)
= (0.001 * 0.002 * 0.95 * 0.90 * 0.70) + (0.001 * 0.002 * 0.05 * 0.05 * 0.01) + (0.001 * 0.998 * 0.94 * 0.90 * 0.70) + (0.001 * 0.998 * 0.06 * 0.05 * 0.01)
= 0.00059224259

P(-burglary | john ^ mary)
= alpha * P(-b) * P(E) * P(A |-b, E) * P(j | A) * P(m | A)
= 0.999 * 0.002 * 0.29 * 0.90 * 0.70 + 0.999 * 0.002 * 0.71 * 0.05 * 0.01 + 0.999 * 0.998 * 0.001 * 0.90 * 0.70 + 0.999 * 0.998 * 0.999 * 0.05 * 0.01
= 0.001491857649

P(Burlgary | john ^ mary) = alpha * <0.00059224259, 0.001491857649> = <0.284, 0.716>
"""

# Compute P(Burglary | John and Mary both call).
print("P(B | j ^ m): ", enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary).show_approx())
# elimination_ask() is a dynamic programming version of enumeration_ask().
print(elimination_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary).show_approx())
# gibbs_ask() is an approximation algorithm helps Bayesian Networks scale up.
print(gibbs_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary).show_approx())
# See the explanation of the algorithms in AIMA Section 14.4.

"""
The first two examples are causal computations, we can see that if there has been a burglary happens and no earthquake. 
it is likely that both the alarm rings and John calls, although it is even more likely the alarm rings.

The last two examples are diagnostic computations, inferring the event of a burglary if the alarm rung or both neighbors
called. If the alarm rung, it is more likely that a burglary had happened than if both neighbors called. 

From these two sets of computations, it seems that the event of burglary is more closely tied to the event of alarm ringing.

All these examples used the chain rule as demonstrated in the class notes.
"""