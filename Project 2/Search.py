import requests
from bs4 import BeautifulSoup
from NLPCore import NLPCoreClient
from collections import defaultdict
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

def textExtractor(URL, min = 10, max = 30):
    # Default timeout 10 seconds
    r = requests.get(URL, timeout = 10)
    ok = False
    visible_text = ""
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        # import re
        # splitted = re.split(r'[^a-zA-Z0-9 ,\'&\-\(\)]+', visible_text)
        cleaned = visible_text.split('\n')
        # for item in splitted:
        #     length = len(item.split())
        #     if length > min and length < max:
        #         cleaned.append(item)
        ok = True

    return ok, cleaned


def Round1(text):
    result = []
    properties = {
        "annotators": "tokenize,ssplit,pos,lemma,ner",
        "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
        "ner.useSUTime": "0"
    }
    relation_name = 'Work_For'
    ne1_type = "ORGANIZATION"
    ne2_type = "PERSON"
    doc = client.annotate(text = text, properties = properties)
    print("Number of sentences in round 1",len(doc.sentences))
    for sentence in doc.sentences:
        sb = []
        typechecker = defaultdict(int)
        for token in sentence.tokens:
            # print(token.ner)
            typechecker[token.ner] += 1
            sb.append(token.word)
        if typechecker[ne1_type] > 0 and typechecker[ne2_type] > 0 and len(sb) < 50:
            line = ' '.join(sb)
            result.append(line)
    return result



def Round2(text):
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
    threshold = 0.35
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
            if max_rel_desc == relation_name and max_val >= threshold:
                if [ne1_type, ne2_type] == sorted([relation.entities[0].type, relation.entities[1].type]):
                    print(relation)

def test():
    ok, extracted = textExtractor("https://en.wikipedia.org/wiki/Bill_Gates")
    if ok:
        print("Prepare to Processing Round1",len(extracted))
        length = 0
        chunck_size = 1000
        text = []
        while length + chunck_size < len(extracted):
            text += Round1(extracted[length:length + chunck_size])
            length += chunck_size
            print("Finished", length,"/",len(extracted))

        text += Round1(extracted[length : len(extracted)])

        print("Prepare to Processing Round2",len(text))
        length = 0
        while length + chunck_size < len(text):
            Round2(text[length : length + chunck_size])
            length += chunck_size
            print("Finished", length,"/",len(text))
        Round2(text[length : len(text)])
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



