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

class spamFilter():
    '''
    @param: goodCorpus: input of one or more lists of good emails.
    @param: spamCorpus: input of one or more lists of spams.
    @attributes: good/badWords: occurrences of words from good/spamCorpus,
                ngood/nspam: number of good messages that heed into good/badWords
                wordProbs: once a message is fed into the filter, will contain the probability of a word being "bad"
    '''
    def __init__(self, goodCorpus=[], spamCorpus=[]):
        self.goodWords = dict()
        self.badWords = dict()
        self.ngood = 0
        self.nspam = 0
        self.wordProbs = dict()
        for element in goodCorpus:
            #check if corpus contains a list of messages
            if type(element) is list:
                self.ngood += 1
                for word in element:
                    if type(word) is str:
                        word = word.lower()
                        try:
                            self.goodWords[word] += 1
                        except:
                            self.goodWords[word] = 1
            #if there is only one message
            elif type(element) is str:
                element = element.lower()
                self.ngood += 1
                try:
                    self.goodWords[element] += 1
                except:
                    self.goodWords[element] = 1
        #same thing creating the spam hash table
        for element in spamCorpus:
            # check if corpus contains a list of messages
            if type(element) is list:
                self.nspam += 1
                for word in element:
                    if type(word) is str:
                        word = word.lower()
                        try:
                            self.badWords[word] += 1
                        except:
                            self.badWords[word] = 1
            # if there is only one message
            elif type(element) is str:
                element = element.lower()
                self.nspam += 1
                try:
                    self.badWords[element] += 1
                except:
                    self.badWords[element] = 1


    '''
    @param: msg is a list of individual words that have been scanned and separated    
    @result: update self.wordProbs with the probability that each word in msg is associated with spam.
    '''
    def listProbs(self, msg):
        for word in msg:
            word = word.lower()
            #algorithm taken from Paul Graham's 'A Plan for Spam' (http://www.paulgraham.com/spam.html)
            try:
                g = 2 * self.goodWords[word]
            except:
                g = 0
            try:
                b = self.badWords[word]
            except:
                b = 0
            if (g + b) > 1:
                spam = max(0.01, min(0.99, (min(1, b/self.nspam) / (min(1, g/self.ngood) + min(1, b/self.nspam)))))
                self.wordProbs[word] = spam

    '''
    @param: msg is a list of pre-scanned tokens
    @return: based on the 15 most interesting probabilities of words in msg, calculate a overall probability that the message is spam
    '''
    def spamProb(self, msg):
        msgProbs = []
        for word in msg:
            if word in self.wordProbs:
                msgProbs.append(self.wordProbs[word])
        if len(msgProbs) > 15:
            msgProbs = [abs(x - 0.5) for x in msgProbs]
            msgProbs = sorted(msgProbs)[:15]
        prod = np.product(msgProbs)
        prod1 = np.product([1 - x for x in msgProbs])
        combined = prod / (prod + prod1)
        return combined

    '''
    @param: msg: list of tokens
    @param: list: a boolean manipulator on whether to print probability of individual words
    @result: print spam probability of this msg and individual word spam probabilities
    '''
    def spamResult(self, msg, list = 1):
        self.listProbs(msg)
        print("\nSpam probability: ", str(round(self.spamProb(msg), 3)))
        if list:
            print('{:15s}{:15s}'.format("Word:","Probability:"))
            for word in msg:
                word = word.lower()
                if word in self.wordProbs:
                    prob = self.wordProbs[word]
                    print('{:15s}{:15s}'.format(word, str(round(prob, 3))))


    '''
    @type: good or spam
    @msgs: a list of msgs, which each is a list of tokens
    @result: update the filter's goodWords or badWords dicts and ngood or nspam
    '''
    def updateFilter(self, type, msgs):
        type = type.lower()
        if type == "good":
            for msg in msgs:
                self.ngood += 1
                for word in msg:
                    if type(word) is str:
                        word = word.lower()
                        try:
                            self.goodWords[word] += 1
                        except:
                            self.goodWords[word] = 1
        elif type == "spam":
            for msg in msgs:
                self.nspam += 1
                for word in msg:
                    if type(word) is str:
                        word = word.lower()
                        try:
                            self.badWords[word] += 1
                        except:
                            self.badWords[word] = 1

if __name__ == '__main__':
    simpleFilter = spamFilter(ham_corpus, spam_corpus)
    if debug:
        print(simpleFilter.ngood, simpleFilter.nspam, simpleFilter.goodWords, simpleFilter.badWords)
    msgs = [ham_corpus[0], ham_corpus[1], spam_corpus[0], spam_corpus[1]]
    for msg in msgs:
        simpleFilter.spamResult(msg)
    test0 = ["self", "i", "spam","am", "do", "eggs", "piglet", "green"]
    test1 = ["this", "is", "spam", "spam", "am"]
    test2 = ["would", "you", "like", "some", "green", "eggs", "and", "ham", "?"]
    simpleFilter.spamResult(test0)
    simpleFilter.spamResult(test1)
    simpleFilter.spamResult(test2)

        #only count words that occur 2 or more times, and create one dictionary for all these words from all the messages


