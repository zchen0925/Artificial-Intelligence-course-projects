'''
Exercise 2 for CS 344 Homework02, Fall 2019
Professor Vander Linden
@author: Ziqi Chen
@version: Mar 5th, 2019
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

cloudy = BayesNet([('Cloudy', '', 0.5),
                   ('Sprinkler', 'Cloudy', {T: 0.10, F: 0.50}),
                   ('Rain', 'Cloudy', {T: 0.80, F: 0.20}),
                   ('WetGrass', 'Sprinkler Rain', {(T, T): 0.99, (T, F):0.90, (F, T): 0.90, (F, F): 0.00})
                   ])


"""
d.i 
P(cloudy) = 0.5
"""
print("P(Cloudy): ", enumeration_ask('Cloudy', dict(), cloudy).show_approx())

"""
d.ii
    P(Sprinkler | cloudy)
=   <0.10, 0.50>
"""
print("P(Sprinkler | cloudy): ", enumeration_ask('Sprinkler', dict(Cloudy = T), cloudy).show_approx())

"""
d.iii
    P(Cloudy | the sprinkler is running and it's not raining)
=   P(Cloudy | sprinker ^ -rain)
=   alpha * P(sprinkler ^ -rain | Cloudy) * P(Cloudy)
=   alpha * <0.02 * 0.5, 0.40 * 0.50>
=   <0.0476, 0.9524>
"""
print("P(Cloudy | sprinkler ^ -rain): ", enumeration_ask('Cloudy', dict(Sprinkler = T, Rain = F), cloudy).show_approx())

"""
d.iv
    P(WetGrass | it's cloudy, the sprinkler is running and it's raining)
=   P(WetGrass | cloudy ^ sprinkler ^ rain)
=   P(WG | sprinkler ^ rain) * P(sprinkler ^ rain | cloudy) * P(cloudy)
=   <0.99, 0.01>
"""
print("P(WetGrass | cloudy, sprinkler, rain): ", enumeration_ask('WetGrass', dict(Cloudy = T, Sprinkler = T, Rain = T), cloudy).show_approx())

"""
d.v
    P(Cloudy | grass is not wet)
=   P(- wetgrass | Sprinkler, Rain) * P(Sprinkler, Rain | Cloudy) * P(Cloudy)
=   alpha * P(-wetgrass | Sprinkler, Rain) * P(Sprinkler, Rain | Cloudy)
=   alpha * <(0.01 * 0.08 + 0.10 * (0.02 + 0.72) + 1 * 0.18,  (0.01 * 0.10 + 0.10 * (0.40 + 0.10) + 1 * 0.40)>
=   alpha * <0.2548, 0.451>
=   <0.361, 0.639>
"""
print("P(Cloudy | -wetgrass): ", enumeration_ask('Cloudy', dict(WetGrass = F), cloudy).show_approx())
