import requests
from bs4 import BeautifulSoup
from NLPCore import NLPCoreClient
import urllib
import json
import sys
import re


SearchAPI = "https://www.googleapis.com/customsearch/v1"
# NLPPackagePath = '/User/lanking/Documents/GitHub/ADB-Class/stanford-corenlp-full-2017-06-09'
client = NLPCoreClient('/Users/lanking/Documents/GitHub/ADB-Class/stanford-corenlp-full-2017-06-09')

def googleQuery(CSEKey, JsonAPIKey, query):
    payload = {'cx': CSEKey , 'key': JsonAPIKey ,'q' : query}
    r = requests.get(SearchAPI, params=payload)
    return json.loads(r.text)

def textExtractor(URL):
    # Default timeout 10 seconds
    r = requests.get(URL, timeout = 10)
    ok = False
    visible_text = ""
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        import re
        splitted = re.split(r'[^a-zA-Z0-9 ,\'&\-\(\)]+', visible_text)
        cleaned = []
        for item in splitted:
            length = len(item.split())
            if length > 10 and length < 30:
                cleaned.append(item)
        ok = True

    return ok, cleaned

def NLP(text):
    # Path
    # for item in text:
    # 	if type(item) !='str':
    # 		print("Crack on items")
    
    properties = {
        "annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation",
        "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
        "ner.useSUTime": "0"
    }
    relation_name = 'Work_For'
    ne1_type = "ORGANIZATION"
    ne2_type = "PEOPLE"
    doc = client.annotate(text = text, properties = properties)
    for item in doc.sentences:
        r = item.relations
        for relation in r:
            probs = relation.probabilities
            max_val = 0.0
            for key, value in probs.items():
                if max_val < float(value):
                    max_val = float(value)
                    max_rel_desc = key
            if max_rel_desc == relation_name:
                if [ne1_type, ne2_type] == sorted([relation.entities[0].type, relation.entities[1].type]):
                    print(relation)

def test():
    ok, extracted = textExtractor("https://en.wikipedia.org/wiki/Bill_Gates")
    if ok:
        print("Prepare to Processing",len(extracted))
        print(extracted)
        length = 0
        while length + 10 < len(extracted):
            NLP(extracted[length : length + 10])
            length +=10
            print("Finished", length,"/",len(extracted))
        NLP(length : len(extracted))
        # print(extracted)
    else:
        print("Error Happened during the fetching and cleaning steps")

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
    # Initialization
    ExtractedTuple = {}
    SeenURL = {}
    sys.stdout.write("Hello World!")
    


if __name__ == "__main__":
    try:
        # main()
        test()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



