import requests
import json
import sys
import re
# from Rocchio import Rocchio 
# import numpy as np
from DataClean import DataClean


SearchAPI = "https://www.googleapis.com/customsearch/v1"
libraryPath = "./proj1-stop.txt"


def googleQuery(CSEKey, JsonAPIKey, query):
    payload = {'cx': CSEKey , 'key': JsonAPIKey ,'q' : query}
    r = requests.get(SearchAPI, params=payload)
    return json.loads(r.text)

def printResult(item):

    sys.stdout.write('Title: '+item["title"]+'\n')    
    sys.stdout.write('Link: '+item["link"]+'\n')
    sys.stdout.write('Summary: '+item["snippet"]+'\n')
    ans = input('Relevant(Y/N)?')
    if ans=='y' or ans=='Y':
        return True
    else:
        return False



def main():
    if len(sys.argv) < 4:
        sys.stdout.write('Usage : python '+ sys.argv[0] +' <JsonAPIKey> <CSEKey> <precision> <query>\n')
        sys.exit()
    JsonAPIKey = sys.argv[1]
    CSEKey = sys.argv[2]
    TargetPrecision = float(sys.argv[3])
    query = ' '.join(sys.argv[4:])
    DC = DataClean(libraryPath)
    DC.clean(query)
    
    posNum = 0;
    alpha = 1
    beta = 1.0
    gamma = 0.5

    result = googleQuery(CSEKey, JsonAPIKey, query)
    result_items = result["items"];
    summary_set = []
    pos_items = []
    neg_items = []
    if len(result_items) ==0:
        print("No result found")
    else:
        # RC = Rocchio(alpha, beta, gamma, DC)
        # RC.createDict(result_items, query)

        for item in result_items:
            tmp = []
            tmp = item["snippet"].split(' ')
            for string in tmp:
                summary_set.append(string)            
            if printResult(item):
                pos_items.append(item)
                posNum+=1
            else:
                neg_items.append(item)
        curPresision =  float(posNum/10)
        if curPresision<TargetPrecision:
            print(curPresision)
            # pos_vec_sum = np.zeros(len(RC.wordIndex.keys()))        
            # neg_vec_sum = np.zeros(len(RC.wordIndex.keys()))
            # for pos_item in pos_items:
            #     pos_vec_sum += RC.doc2Vec(pos_item)
            # for neg_items in neg_items:
            #     neg_vec_sum += RC.doc2Vec(neg_item)
            #     neg_vec_sum
            # pos_vec_sum = pos_vec_sum/posNum
            # neg_vec_sum = neg_vec_sum/(10-posNum)
            # RC.calculate(pos_vec_sum, neg_vec_sum)

            # queryList = query.split(" ")
            # queryList.append() = np.()
            # query = query
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



