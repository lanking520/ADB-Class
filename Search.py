import requests
import json
import sys
import re
from Rocchio import Rocchio 
import numpy as np
from DataClean import DataClean


SearchAPI = "https://www.googleapis.com/customsearch/v1"
libraryPath = "./proj1-stop.txt"


def googleQuery(CSEKey, JsonAPIKey, query):
    payload = {'cx': CSEKey , 'key': JsonAPIKey ,'q' : query}
    r = requests.get(SearchAPI, params=payload)
    return json.loads(r.text)

def printResult(item):
    sys.stdout.write('\nTitle: '+item["title"]+'\n')    
    sys.stdout.write('Link: '+item["link"]+'\n')
    sys.stdout.write('Summary: '+item["snippet"]+'\n')
    ans = input('Relevant(Y/N)?')
    if ans=='y' or ans=='Y':
        return True
    else:
        return False



def main():
    if len(sys.argv) < 4:
        sys.stdout.write('Usage : python3 '+ sys.argv[0] +' <JsonAPIKey> <CSEKey> <precision> <query>\n')
        sys.exit()
    JsonAPIKey = sys.argv[1]
    CSEKey = sys.argv[2]
    TargetPrecision = float(sys.argv[3])
    query = ' '.join(sys.argv[4:])
    DC = DataClean(libraryPath)
    query = DC.clean(query)

    curPresision = 0
    alpha = 1
    beta = 1.0
    gamma = 0.5

    while curPresision<TargetPrecision:
          
        result = googleQuery(CSEKey, JsonAPIKey, query)
        result_items = result["items"] 
        # print(RC.wordIndex)
        if len(result_items) < 10:
            print("No result found or reuslt items smaller than 10")
            return 

        posNum = 0
        pos_items = []
        neg_items = []   
        for item in result_items:           
            if printResult(item):
                pos_items.append(item)
                posNum+=1
            else:
                neg_items.append(item)

        curPresision =  float(posNum/10)
        if curPresision <= 0.0:
            print("No correct item found!")
            return
        if curPresision<TargetPrecision:
            print(curPresision)
        else:
            print("Finished!")
            return

        RC = Rocchio(alpha, beta, gamma, DC)
        RC.createDict(result_items, query)
        query +=" " + RC.calculate(pos_items, neg_items, posNum)
        print(query)


    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



