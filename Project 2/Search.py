#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import tika
from bs4 import BeautifulSoup
from NLPCore import NLPCoreClient
from collections import defaultdict
import urllib.request as ur
import json
import sys
import re


SearchAPI = "https://www.googleapis.com/customsearch/v1"
# NLPPackagePath = '/User/lanking/Documents/GitHub/ADB-Class/stanford-corenlp-full-2017-06-09'
client = NLPCoreClient('/Users/lanking/Documents/GitHub/ADB-Class/stanford-corenlp-full-2017-06-09')

## Parameter for selection
DEBUG = True
USE_TIKA = False   # Default using BeautifulSoup, can choose TIKA
if USE_TIKA:
    tika.initVM()
checkList = {"Work_For":"ORGANIZATION PEOPLE", "OrgBased_In": "LOCATION ORGANIZATION", "Live_In":"LOCATION PEOPLE","Located_In":"LOCATION LOCATION"}

def googleQuery(CSEKey, JsonAPIKey, query):
    payload = {'cx': CSEKey , 'key': JsonAPIKey ,'q' : query}
    r = requests.get(SearchAPI, params=payload)
    return json.loads(r.text)

def print_formatter(source):
    print("=============== EXTRACTED RELATION ===============")
    print("Sentence:",source['text'])
    builder = []
    builder.append("RelationType: " + source['relation'])
    builder.append("Confidence: " + source['prob'])
    builder.append("EntityType1= " + source['e0'].type)
    builder.append("EntityValue1= "+ source['e0'].value)
    builder.append("EntityType2= " + source['e1'].type)
    builder.append("EntityValue2= "+ source['e1'].value)
    print(' | '.join(builder))
    print("============== END OF RELATION DESC ==============")

def printIntro(CSEKey, JsonAPIKey, relation, threshold, query, tuples):
    print("Parameters")
    print("Client key\t= ",CSEKey)
    print("Engine key\t= ",JsonAPIKey)
    print("Relation\t= ",relation)
    print("Threshold\t= ", threshold)
    print("Query\t\t= ", query)
    print("# of Tuples\t= ", tuples)

def printSummary(source, tuples):
    source = sorted(source, key=lambda k : k['prob'], reverse = True)
    upperbound = min(len(source), tuples)
    print("================== ALL RELATIONS =================")
    for i in range(upperbound):
        builder = []
        builder.append("RelationType: " + source[i]['relation']+'\t')
        builder.append("Confidence: " + "{0:.3f}".format(float(source[i]['prob']))+'\t')
        builder.append("Entity #1: " + source[i]['e0'].value +" ("+ source[i]['e0'].type+")\t")
        builder.append("Entity #2: " + source[i]['e1'].value +" ("+ source[i]['e1'].type+")")
        print('|'.join(builder))
        print('')
'''
        Data Cleaning Section
'''
def textExtractor(URL):
    # Default timeout 10 seconds
    ok = False
    text = ""
    try:
        text = ur.urlopen(URL).read()
    except Exception as e:
        print("URL open Failed:", e)
    
    if len(text) == 0:
        try:
            r = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                text = r.text
        except Exception as e:
            print("requests open Failed:", e)

    cleaned = []
    visible_text = ""
    if USE_TIKA:
        from tika import parser
        visible_text = parser.from_buffer(text)['content']
    else:
        soup = BeautifulSoup(text, "html.parser")
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
        visible_text = soup.getText()

    visible_text = re.sub(r'[^\x00-\x7F]+',' ', visible_text)
    # splitted = re.split(r'[^a-zA-Z0-9 ,\'&\-\(\)]+', visible_text)
    # visible_text = visible_text.encode('ascii', 'replace').decode('ascii')
    cleaned = visible_text.split('\n')
    # for item in splitted:
    #     length = len(item.split())
    #     if length > min and length < max:
    #         cleaned.append(item)
    ok = True

    return ok, cleaned

'''
        Pipeline for Stanford NLP
'''
def relation_judger(relation_name, source):
    determine = False
    if   relation_name == 'Live_In':
        determine = source['PERSON'] > 0 and source['LOCATION'] > 0
    elif relation_name == 'Located_In':
        determine = source['LOCATION'] > 1
    elif relation_name == 'OrgBased_In':
        determine = source['LOCATION'] > 0 and source['ORGANIZATION'] > 0
    elif relation_name == 'Work_For':
        determine = source['PERSON'] > 0 and source['ORGANIZATION'] > 0
    return determine


def Round1(text, relation_name):
    result = []
    if len(text) == 0:
        return result
    properties = {
        "annotators": "tokenize,ssplit,pos,lemma,ner",
        "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
        "ner.useSUTime": "0"
    }
    # relation_name = "Work_For"
    # ne1_type = "ORGANIZATION"
    # ne2_type = "PERSON"
    doc = client.annotate(text = text, properties = properties)
    if DEBUG: print("Number of sentences in round 1",len(doc.sentences))
    for sentence in doc.sentences:
        sb = []
        typechecker = defaultdict(int)
        for token in sentence.tokens:
            # print(token.ner)
            typechecker[token.ner] += 1
            sb.append(token.word)
        if relation_judger(relation_name,typechecker) and len(sb) < 50:
            line = u' '.join(sb)
            result.append(line)
    return result



def Round2(text, relation_name):
    result = []
    if len(text) == 0:
        return result
    properties = {
        "annotators": "tokenize,ssplit,pos,lemma,ner,parse,relation",
        "parse.model": "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
        "ner.useSUTime": "0"
    }
    # relation_name = 'Work_For'
    # ne1_type = "ORGANIZATION"
    # ne2_type = "PEOPLE"
    threshold = 0.35
    doc = client.annotate(text = text, properties = properties)
    for item in doc.sentences:
        r = item.relations
        line = ""
        for relation in r:
            probs = relation.probabilities
            e = relation.entities
            key = ' '.join(sorted([e[0].type,e[1].type]))
            if key != checkList[relation_name]:
                if DEBUG: print(key,"Length of entities", len(e))
                continue
            if relation_name in probs and probs[relation_name] == max(probs.values()):
                if len(relation.entities) == 2:
                    if len(line) == 0:
                        temp = []
                        for token in item.tokens:
                            temp.append(token.word)
                        line = ' '.join(temp)
                    
                    if e[1].type > e[0].type:
                        swap = e[0]
                        e[0] = e[1]
                        e[1] = swap
                    result.append({'e0':e[0], 'e1': e[1], 'prob':probs[relation_name], 'text':line,'relation':relation_name})
    return result

def remove_dupes(source):
    origin= {}
    for item in source:
        key = ' '.join(sorted([item['e0'].value, item['e1'].value]))
        if not key in origin:
            origin[key] = item
        else:
            if origin[key]['prob'] < item['prob']:
                origin[key] = item
    return origin.values()

def threshold_cutoff(source, threshold):
    result = []
    for item in source:
        if item['prob'] >= threshold:
            result.append(item)
    return result

'''
        Helper and Main function
'''

def batch_call(source, chunck_size,func_name, relation_name):
    methods = {'Round1': Round1, 'Round2':Round2}
    result = []
    length = 0
    while length + chunck_size < len(source):
            result += methods[func_name](source[length:length + chunck_size],relation_name)
            length += chunck_size
            if DEBUG: print("Finished", length,"/",len(source))

    result += methods[func_name](source[length : len(source)],relation_name)
    return result


def new_query(source, query, queryed):
    source = sorted(source, key=lambda k : k['prob'], reverse = True)
    query_set = set(query.split())
    for item in source:
        if item['e0'].value in query_set and item['e1'].value in query_set:
            continue
        else:
            query = item['e0'].value + ' ' + item['e1'].value
            if not query in queryed:
                return query
    return query

def test():
    ok, extracted = textExtractor("https://en.wikipedia.org/wiki/Bill_Gates")
    if ok:
        print("Prepare to Processing Round1",len(extracted))
        text = batch_call(extracted, 10000, 'Round1')

        print("Prepare to Processing Round2",len(text))
        result = batch_call(text, 10000, 'Round2')

        print("Remove Dupes...", len(result))
        result = remove_dupes(result)
        print("Dupes Removed!", len(result))
        for item in result:
            print_formatter(item)
    else:
        print("Error Happened during the fetching and cleaning steps")

def main():
    if len(sys.argv) < 7:
        sys.stdout.write('Usage : python3 '+ sys.argv[0] +' <google api key> <google engine id> <r> <t> <q> <k>\n')
        sys.exit()
    CSEKey = sys.argv[1]
    JsonAPIKey = sys.argv[2]
    RelationSelector = sys.argv[3]		# Select one from 4 from StanfordNLP
    threshold = sys.argv[4]					# extraction confidence threshold
    query = sys.argv[5]                 # Initial Feedin Query
    k = sys.argv[6]                     # Number of tuple needed
    # Initialization
    relation_name = ["Live_In", "Located_In", "OrgBased_In", "Work_For"][int(RelationSelector) - 1]
    printIntro(CSEKey, JsonAPIKey, relation_name, threshold, query, k)
    result_set = []
    not_finished = True
    curr_round = 1
    requestedURL = {}
    queryed = {}
    while not_finished:
        print("=========== Iteration:",curr_round,"- Query:", query,"===========")
        query_result = googleQuery(JsonAPIKey, CSEKey, query)
        result_items = query_result['items']
        for item in result_items:
            URL = item['link']
            result = []
            print("Processing:",URL)
            if URL in requestedURL:
                print("URL Already Requested!")
            else:
                requestedURL[URL] = True
                ok, extracted = textExtractor(URL)
                if ok:
                    text = batch_call(extracted, 10000, 'Round1', relation_name)
                    result = batch_call(text, 10000, 'Round2', relation_name)
                    result = remove_dupes(result)
                    for item in result:
                        print_formatter(item)
                else:
                    print("URL calling Failed...")
            result_set.extend(result)
            print("Relations extracted from this website:", len(result) ,"(Overall:", len(result_set) ,")")

        print("Pruning relations below threshold...")
        result_set = remove_dupes(result_set)
        result_set = threshold_cutoff(result_set, threshold)
        print("Number of tuples after pruning:",len(result_set))
        printSummary(result_set, int(k))

        if len(result_set) >= int(k):
            not_finished = False
            print("Program reached", k ,"number of tuples. Shutting down...")
        else:
            nquery = new_query(result_set, query, queryed)
            if nquery == query:
                not_finished = False
                print("Cannot find a new query from the result! Shutting down...")
            queryed[query] = True
            query = nquery
        curr_round += 1


if __name__ == "__main__":
    try:
        main()
        # test()
    except KeyboardInterrupt:
        print ("\n")
        exit()	



