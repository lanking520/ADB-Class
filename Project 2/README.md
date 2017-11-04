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
A couples of way tried 

## How you carried out Step 3



