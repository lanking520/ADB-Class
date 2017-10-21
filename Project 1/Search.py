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
    sys.stdout.write('URL: '+item["link"]+'\n')
    sys.stdout.write('Title: '+item["title"]+'\n')    
    sys.stdout.write('Summary: '+item["snippet"]+'\n\n')
    ans = input('Relevant(Y/N)?')
    if ans=='y' or ans=='Y':
        return True
    else:
        return False

def printFeedback(query, precision, TargetPrecision):
    sys.stdout.write("======================\n")
    sys.stdout.write("FEEDBACK SUMMARY\n")
    sys.stdout.write("Query " + query+"\n")
    sys.stdout.write("Precision " + str(precision)+"\n")
    if precision <= 0.0:
        sys.stdout.write("No correct item found!")
        return True
    if precision < TargetPrecision:
        sys.stdout.write("Still below the TargetPrecision " + str(TargetPrecision) + "\n")
        return False
    else:
        sys.stdout.write("Meet the TargetPrecision!\n")
        return True

def printIntro(query, CSEKey, JsonAPIKey, precision):
    sys.stdout.write("Parameters\n")
    sys.stdout.write("Client key = " + CSEKey + "\n")
    sys.stdout.write("Engine key = " + JsonAPIKey + "\n")
    sys.stdout.write("Query      = " + query + "\n")
    sys.stdout.write("Precision  = " + str(precision)+"\n")

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
    RC = Rocchio(alpha, beta, gamma, DC)

    while curPresision < TargetPrecision:
          
        result = googleQuery(CSEKey, JsonAPIKey, query)
        result_items = result["items"] 
        # print(RC.wordIndex)
        printIntro(query, CSEKey, JsonAPIKey, TargetPrecision)
        sys.stdout.write("Google Search Results:\n======================\n")
        if len(result_items) < 10:
            print("No result found or reuslt items smaller than 10\n")
            return 

        posNum = 0
        pos_items = []
        neg_items = []   
        for idx, item in enumerate(result_items):
            print("\nResult " +str(idx+1)+"\n")       
            if printResult(item):
                pos_items.append(item)
                posNum+=1
            else:
                neg_items.append(item)

        curPresision =  float(posNum/10)
        if printFeedback(query, curPresision, TargetPrecision):
            return

        sys.stdout.write("Indexing results ....\n")
        RC.createDict(result_items, query)
        newWord = RC.calculate(pos_items, neg_items, posNum)
        sys.stdout.write("Augmenting by "+newWord+"\n")
        query += " " + newWord
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



