# Advanced Database System - Project 2

## Group 2
|  Name      |  UNI   |
|------------|--------|
|Li-Chieh Liu| ll3123 |
|  Qing Lan  | ql2282 |

## Files List:
requirement.txt - Dependency package<br>
Search.py - Our main program
NLPCore.py
data.py 


## Google Search API
Engine ID: 014170202143592210537:4zb34sjofuu<br> 
JSON API key: AIzaSyBz-iFhhFx_sQSBMxKBMh9d5ZjD2nyQtLw

## How to run our program
do `` pip3 install -r requirement.txt`` <br>

Next, you have to specify your command line parameter as follow: <br>
do ``python3 Search.py  <google api key> <google engine id> <r> <t> <q> <k> <Stanford NLP Package Path>`` <br>


## Internal design of this project

### Step 1 Getting Required URL and Content
Using Google Custom Search Engine and obtained the 10 search result. For each URL, the system would try to do the normal HTTP GET call through urllib. If request failed, it will use requests call with headers added. Then, user can choose to use TIKA or BeautifulSoup to do the text cleaning. TIKA was chosen by default. For TIKA configuration, Content will be extracted. For BeautifulSoup, the visible content from HTML will be extracted.

### Step 2 Data Cleaning for the Content
A couples of way tried to do the cleaning including remove special Symbols(\[^a-zA-Z0-9 .!?-\']+), and removing none ascii symbols. The final solution was just do the ascii translation(encoding + decoding), replace all \n to dot. It would maximize the relation found in the text documents. Finally, pass them as a list to the two pipelines.

### Step 3 Stanford NLP Relation Extraction
Two pipeline was inplemented in our case. The first pipeline are specifically used to find if some keywords existed in the sentences. It would extract the useful sentences from the raw data. The second pipeline would extract the relation in these sentences. If there is a match to the requirement, it would be stored into the list and passed back to the main function. Please see the follows for more detailed implementation on Step 3. Each item in the list would in the following format:

- relationEntity 1
- relationEntity 2
- Text
- Probabilities
- relation name

### Step 4 Remove Dupes and to the next cycle
When the result obtained from stanfordNLP, these data would be stored in a list. Then the program would move on into next URL to extract query. The program would start removing duplicated items when all result obtained. The duplicated is determined by the relationEntities value. If both name existed in the list, we only keep the one with the higher probabilities. Then, the item would be eliminated if it is smaller than the threashold that user defined. After that, the program would check the number of items reach to the requirement or not. If the number is smaller than the number that user required, the program would move back to step 1 with the query that is not searched before.


## How you carried out Step 3
### First Pipeline
The design of first pipeline is generally follow the requirement and the following steps would be taken during the annotation:

- Annotator: tokenize,ssplit,pos,lemma,ner
- parse.model: "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"
- ner.useSUTime: "0"

After this step, we will start the search ner from all sentences that the annotator defined and store them in the dictionary. A filter would be applied to filter out the entities set that not match our requirement. Filter implementation is as follows:

- Live_In : PERSON and LOCATION should be in the dictionary
- Located_In: LOCATION numbers should be greater than 1
- OrgBased_In: LOCATION and ORGANIZATION should be in the dictionary
- Work_For: ORGANIZATION and PERSON should be in the dictionary

It a match has been found, we would reconstruct it as a string from all tokens in the sentences. In our case, any sentences with token number greater than 50 would be eliminated to save time.

### Second Pipeline
After the first pipline, the number of matched sentences would be greatly reduced. We feed them to the second pipeline. Comparing to the first pipeline, the second one added "parse" and "relation" step in order to do the relation extraction. After the annotation, we would find the sentence with relation that user required is the maximum of all relations that the sentence holds. Then, the sentence would be reconstructed and stored in the dictionary.

