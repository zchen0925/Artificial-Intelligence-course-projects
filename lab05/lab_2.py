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
cancer = BayesNet([
    ('Cancer', '', 0.01),
    ('Test1', 'Cancer', {T: 0.90, F: 0.20}),
    ('Test2', 'Cancer', {T: 0.90, F: 0.20})
    ])



"""
 P(Cancer | test1 ^ test2)
 = alpha * P(Cancer, test1, test2)
 = alpha * P(test1 ^ test2 | Cancer) * P(Cancer) 
 = alpha * <(0.9 * 0.9 * 0.01), (0.2 * 0.2 * 0.99)>
 = alpha * <0.0081,  0.0396>
 = <0.170, 0.830> 
"""
print("P(Cancer | test1 ^ test2): ", enumeration_ask('Cancer', dict(Test1=T, Test2=T), cancer).show_approx())

"""
 P(Cancer | test1 ^ -test2)
= alpha * P(Cancer) * P(test1 | Cancer) * P(-test2 | Cancer)
= alpha * <(0.01 * 0.90 * 0.1, 0.99 * 0.20 * 0.80>
= alpha * <0.0009, 0.1584>
= <0.006, 0.994>
"""
print("P(Cancer | test1 ^ -test2): ", enumeration_ask('Cancer', dict(Test1=T, Test2=F), cancer).show_approx())

"""
The results make sense because 80% of the time a failed test indicates the absence of cancer. Since the prior probability 
of cancer is already low and not having cancer is already high, this increases the probability of no cancer. 
Test2 also explains away why test1 is positive -- if there's no cancer, there is still a 20% chance of having a positive 
result on the first test. So 1 failed test out of 2 decreased the probability of having cancer from 0.17 to 0.006, 
making it 30 times less likely.
"""