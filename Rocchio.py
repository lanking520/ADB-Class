import numpy as np
from DataClean import DataClean

class Rocchio:
    def __init__(self, alpha, beta, ghamma, dc):
        self.alpha = alpha
        self.beta = beta
        self.ghamma = ghamma
        self.dc = dc

    def createDict(self, document, query):
        temp = {}
        for item in document:
            result = self.dc.stopWordRemoval(self.dc.clean(item['snippet']).split())
            for w in result:
                temp[w] = 0

        self.wordIndex = {}
        for index, item in eumerate(temp.keys()):
            self.wordIndex[item] = index

    def doc2Vec(self, doc):
        mylist = self.dc.stopWordRemoval(self.dc.clean(doc).split())
        result = np.zeros(len(self.wordIndex.keys()))
        for word in mylist:
            if word in self.wordIndex:
                result[self.wordIndex[word]] += 1
        return result

    def calculate(self, pos, neg):
        pass





