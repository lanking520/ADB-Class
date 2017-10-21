import requests
import json
import sys
import re


SearchAPI = "https://www.googleapis.com/customsearch/v1"


def googleQuery(CSEKey, JsonAPIKey, query):
    payload = {'cx': CSEKey , 'key': JsonAPIKey ,'q' : query}
    r = requests.get(SearchAPI, params=payload)
    return json.loads(r.text)

def main():
    if len(sys.argv) < 7:
        sys.stdout.write('Usage : python3 '+ sys.argv[0] +' <google api key> <google engine id> <r> <t> <q> <k>\n')
        sys.exit()
    CSEKey = sys.argv[1]
    JsonAPIKey = sys.argv[2]
    RelationSelector = sys.argv[3]		# Select one from 4 from StanfordNLP
    ECT = sys.argv[4]					# extraction confidence threshold
    query = sys.argv[5]
    k = sys.argv[6]
    
    sys.stdout.write("Hello World!")
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("\n")
        exit()	


