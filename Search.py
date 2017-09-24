import requests
import json
import sys
import re
# import numpy as np

SearchAPI = "https://www.googleapis.com/customsearch/v1"
libraryPath = "./proj1-stop.txt"


class DataClean:
    def __init__(self, path):
        f = open(path)
        self.library = f.read().splitlines()

    def clean(self, query):
        # Half-piece
        query = re.sub('[^a-zA-Z0-9]', ' ', query)
        return query

    def stopWordRemoval(self, text):
        text = [w for w in text if not w in self.library and not w.replace('.', '', 1).isdigit()]
        return text


def googleQuery(CSEKey, JsonAPIKey, precsion, query):
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
    precision = float(sys.argv[3])
    query = ' '.join(sys.argv[4:])
    DC = DataClean(libraryPath)
    DC.clean(query)
    

    alpha = 1
    beta = 1.0
    gamma = 0.5

    result = googleQuery(CSEKey, JsonAPIKey, precision, query)
    result_items = result["items"];
    summary_set = []
    pos = []
    neg = []
    if len(result_items) ==0:
        print("No result found")
    else:
        for item in result_items:
            tmp = []
            tmp = item["snippet"].split(' ')
            for string in tmp:
                summary_set.append(string)            
            if printResult(item):
                pos.append(item)
            else:
                neg.append(item)

    

    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



