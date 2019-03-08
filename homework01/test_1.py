'''
Exercise 1 for CS 344 Homework02, Fall 2019
Professor Vander Linden
@author: Ziqi Chen
@version: Mar 5th, 2019
'''
import numpy as np

debug = 1

spam_corpus = [["I", "am", "spam", "spam", "I", "am"], ["I", "do", "not", "like", "that", "spamiam"]]
ham_corpus = [["do", "i", "like", "green", "eggs", "and", "ham"], ["i", "do"]]

'''
@param: *corpus: input of one or more list of innocent tokens
@return: a dict containing unique words and their occurrences
'''
def hashgood(*corpus):
    good = dict()
    for list in corpus:
        for word in list:
            if word not in good:
                good[word] = 1
            elif word in good:
                good[word] += 1
    return good

'''
@param: *corpus: input of one or more list of spam tokens
@return: a dict containing unique words and their occurrences
'''
def hashbad(*corpus):
    bad = dict()
    for list in corpus:
        for word in list:
            if word not in bad:
                bad[word] = 1
            elif word in bad:
                bad[word] += 1
    return bad


def spamProb(msg, good, bad, ngood = 2, nbad = 2):
    probs = dict()
    for word in msg:
        try:
            g = 2 * good[word]
        except:
            g = 0
        try:
            b = bad[word]
        except:
            b = 0
        if (g + b) >= 1:
            spam = max(0.01, min(0.99, (min(1, b/nbad) / (min(1, g/ngood) + min(1, b/nbad)))))
            probs[word] = spam
    return probs


def interesting(prob):
    return abs(prob - 0.5)

def combinedProb(probs):
    if len(probs) > 15:
        probs = sorted(probs, key=interesting)
        probs = probs[:15]
    prod = np.product(probs)
    prod1 = np.product([1-x for x in probs])
    combined = prod / (prod + prod1)
    return combined


if __name__ == '__main__':
    good = hashgood(ham_corpus[0], ham_corpus[1])
    bad = hashbad(spam_corpus[0], spam_corpus[1])
    msgs = [ham_corpus[0], ham_corpus[1], spam_corpus[0], spam_corpus[1]]
    for msg in msgs:
        probs = list(spamProb(msg, good, bad).values())
        print('{:75s}{:25s}{:25s}'.format(str(msg), "spam probability: ", str(round(combinedProb(probs), 5))))

    if debug:
        print(str(good),str(bad))
        for msg in msgs:
            print(spamProb(msg, good=good, bad=bad))

