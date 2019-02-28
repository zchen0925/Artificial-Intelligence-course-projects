'''
This module implements a simple classroom example of probabilistic inference
over the full joint distribution specified by AIMA, Figure 13.3.
It is based on the code from AIMA probability.py.

@author: kvlinden
@version Jan 1, 2013
'''

from probability import JointProbDist, enumerate_joint_ask

# The Joint Probability Distribution Fig. 13.3 (from AIMA Python)
P = JointProbDist(['Toothache', 'Cavity', 'Catch'])
T, F = True, False
P[T, T, T] = 0.108; P[T, T, F] = 0.012
P[F, T, T] = 0.072; P[F, T, F] = 0.008
P[T, F, T] = 0.016; P[T, F, F] = 0.064
P[F, F, T] = 0.144; P[F, F, F] = 0.576

# Compute P(Cavity|Toothache=T)  (see the text, page 493).
PC = enumerate_joint_ask('Cavity', {'Toothache': T}, P)
print(PC.show_approx())

'''
Exercise 4.1.b
P(Cavity | Catch) = P(Cavity ^ Catch) / P(Catch)
                = (0.108 + 0.072) / (0.108 + 0.072 + 0.016 + 0.144)
                =~ 0.529
P(- Cavity | Catch) = P(- Cavity ^ Catch) / P(Catch)
                = (0.016 + 0.144) / (0.108 + 0.072 + 0.016 + 0.144)
                =~ 0.471 (or 1-P(Cavity | Catch)
'''
Pcc = enumerate_joint_ask('Cavity', {'Catch': T}, P)
print(Pcc.show_approx())


# Exercise 4.1.C
C = JointProbDist(['Coin1', 'Coin2'])
Heads, Tails = True, False
C[Heads, Heads] = 0.25;   C[Heads, Tails] = 0.25
C[Tails, Heads] = 0.25;   C[Tails, Tails] = 0.25

'''
P( Coin2 = heads | Coin1 = heads) = P(Coin2 = heads ^ Coin1 = heads) / P(Coin1 = heads)
                          = (0.5 * 0.5) / 0.5
                          = 0.5
                          
P(Coin2 = tails | Coin1 = heads) = 1 - P(Coin2 = heads | Coin1 = heads) = 0.5
'''
Phh = enumerate_joint_ask('Coin2', {'Coin1': Heads}, C)
print(Phh.show_approx())

'''
The probability that coin2 comes up heads given that coin1 is heads is 0.5. This confirms what I generally believe about
 flipping coins. Because we generally assume each coin flip is independent of the results of previous flips, and each 
 flip has a 50% chance of being heads or tails, the probability of having heads or tails on the second coin shouldn't be
 influenced by the result on the first coin.
 
 
 It seems that full joint is difficult to scale. With the addition of each new variable, the number of entries in the 
 joint probability distribution table doubles. This will be clumsy if we are dealing with a large quantity of variables, 
 and it would be hard to maintain if new variables are added constantly.
'''

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
Pr[T, T, T, T] = 0.0648; Pr[T, T, F, T] = 0.0096
Pr[F, T, T, T] = 0.0216; Pr[F, T, F, T] = 0.0432
Pr[T, F, T, T] = 0.0432; Pr[T, F, F, T] = 0.0064
Pr[F, F, T, T] = 0.0504; Pr[F, F, F, T] = 0.1008
Pr[T, T, T, F] = 0.0072; Pr[T, T, F, F] = 0.0384
Pr[F, T, T, F] = 0.0024; Pr[F, T, F, F] = 0.1728
Pr[T, F, T, F] = 0.0048; Pr[T, F, F, F] = 0.0256
Pr[F, F, T, F] = 0.0056; Pr[F, F, F, F] = 0.4032

Ptr = enumerate_joint_ask('Toothache', {'Rain': T}, Pr)
print(Ptr.show_approx())