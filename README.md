# Advanced Database System - Project 1 

## Group 2
|  Name      |  UNI   |
|------------|--------|
|Li-Chieh Liu| ll3123 |
|  Qing Lan  | ql2282 |

## Files List:
Search.py - Our main program <br>
DataClean.py - Remove stop words and symbols <br>
Rocchio.py - Modified Rocchio algorithms <br>


## Google Search API
Engine ID: 014170202143592210537:4zb34sjofuu<br> 
JSON API key: AIzaSyBz-iFhhFx_sQSBMxKBMh9d5ZjD2nyQtLw

## How to run our program
do ``python3 Search.py <JsonAPIKey> <CSEKey> <precision> <query>``


## internal design of your project

## Our Query Modification Method
We basically use the following formula<br> 

![alt text](rocchio-formula.png "Rocchio Formula") <br> 

Dj: Relevant Document Vector<br> 
Dk: Irrelevant Document Vector<br> 
Qo: Original Query Vector<br> 
Qm: Voted Query Vector<br> 
Here we set:<br> 
a = 0 (since we cannot delete words in the original query)<br> 
b = 1<br> 
c = 0.5<br> 

We add one word at a time, the new word would be the highest voted word in vector Qm.<br> 
We create a long vector, each entry is a word appear in the top 10 search, if a document is marked as relevantm, we upvote the words in this document by weight b = 1, if it is irrelevant, we downvote the the word in this document by weight c = 0.5, and therefore comes out an vector Qm, we sort Qm to get the highest voted word and add to our new query. 


