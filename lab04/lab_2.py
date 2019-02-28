'''
This module implements a simple classroom example of probabilistic inference
over the full joint distribution specified by AIMA, Figure 13.3.
It is based on the code from AIMA probability.py.

@author: kvlinden
@version Jan 1, 2013
'''

from probability import JointProbDist, enumerate_joint_ask
'''
Exercise 4.2
i. There are 16 entries in the table now.
ii. The probabilities sum up to 1 and they should. The probabilities in a sample space always sums to 1.
iii. No. We can use 0 and 1 to denote True or False, but essentially they can only take on these values. This is because
in the real world an event either happens or doesn't happen (not considering Schrodinger's cat scenario)
iv. No, the probability of rain is not independent of the probability of toothache. Since people seem to have toothaches
more often when it rains, I chose the probability of rain to be 0.6 given toothache, and probability of rain = 0.3
when no toothache.

P(toothache | rain) = P(toothache ^ rain) / P(rain)
                    = (0.0648 + 0.0072 + 0.0096 + 0.0384) 
                        / (0.0648 + 0.0072 + 0.0096 + 0.0384 + 0.0216 + 0.0024 + 0.0432 + 0.1728)
                    ~= 0.333
P(-toothache | rain) = 1 - 0.333 = 0.667
P(Toothahce | rain) = <0.333, 0.667> 

'''
# The Joint Probability Distribution Fig. 13.3 with added Rain variable (from AIMA Python)
Pr = JointProbDist(['Toothache', 'Rain', 'Cavity', 'Catch'])
T, F = True, False
Pr[T, T, T, T] = 0.0648;
Pr[T, T, F, T] = 0.0096
Pr[F, T, T, T] = 0.0216;
Pr[F, T, F, T] = 0.0432
Pr[T, F, T, T] = 0.0432;
Pr[T, F, F, T] = 0.0064
Pr[F, F, T, T] = 0.0504;
Pr[F, F, F, T] = 0.1008
Pr[T, T, T, F] = 0.0072;
Pr[T, T, F, F] = 0.0384
Pr[F, T, T, F] = 0.0024;
Pr[F, T, F, F] = 0.1728
Pr[T, F, T, F] = 0.0048;
Pr[T, F, F, F] = 0.0256
Pr[F, F, T, F] = 0.0056;
Pr[F, F, F, F] = 0.4032

Ptr = enumerate_joint_ask('Toothache', {'Rain': T}, Pr)
print(Ptr.show_approx())