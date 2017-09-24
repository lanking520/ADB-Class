import numpy as np
from DataClean import DataClean

class Rocchio:
    def __init__(self, alpha, beta, gamma, dc):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.dc = dc
        self.wordIndex = {}
        self.num2Word = {}

    def createDict(self, document, query):
        temp = {}
        for item in document:
            result = self.dc.stopWordRemoval(self.dc.clean(item['snippet']+" "+item['title']).lower().split())
            for w in result:
                temp[w] = 0
        for q_word in query.lower().split(" "):
            if q_word in temp: 
                del temp[q_word]

        for index, item in enumerate(temp.keys()):
            self.wordIndex[item] = index
            self.num2Word[index] = item


    def doc2Vec(self, doc):
        mylist = self.dc.stopWordRemoval(self.dc.clean(doc).split())
        result = np.zeros(len(self.wordIndex.keys()))
        for word in mylist:
            if word in self.wordIndex:
                result[self.wordIndex[word]] += 1
        return result

    def calculate(self, pos_items, neg_items, posNum):

        pos_vec_sum = np.zeros(len(self.wordIndex.keys()))        
        neg_vec_sum = np.zeros(len(self.wordIndex.keys()))
        for pos_item in pos_items:
            pos_vec_sum += self.doc2Vec(pos_item['snippet']+pos_item['title'])
        for neg_item in neg_items:
            neg_vec_sum += self.doc2Vec(neg_item['snippet']+neg_item['title'])
            neg_vec_sum    
        pos_vec_sum = pos_vec_sum/posNum
        neg_vec_sum = neg_vec_sum/(10-posNum)
        final_sum = self.beta*pos_vec_sum-self.gamma*neg_vec_sum
        finalindex = np.argsort(final_sum)
        # for index in finalindex:
        #     print(self.num2Word[index])
        return self.num2Word[finalindex[-1]]





