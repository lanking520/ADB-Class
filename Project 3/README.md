# Advanced Database System - Project 3

## Group 2
|  Name      |  UNI   |
|------------|--------|
|Li-Chieh Liu| ll3123 |
|  Qing Lan  | ql2282 |

## Files List:
requirement.txt - Dependency package<br>
ARM.py - Our main program
INTEGRATED-DATASET.csv
example-run.txt

## How to run our program
do `` pip install -r requirement.txt`` <br>

Next, you have to specify your command line parameter as follow: <br>
do ``python ARM.py INTEGRATED-DATASET.csv <min_sup> <min_conf>`` <br>

## NYC Open Data data set(s) you used to generate the INTEGRATED-DATASET file: 
We use **DOHMH New York City Restaurant Inspection Results**. To be more specific, 

## how do you map the original NYC Open Data data set(s) into your INTEGRATED-DATASET file: 

## What makes your choice of INTEGRATED-DATASET file compelling (in other words, justify your choice of NYC Open Data data set(s)). The explanation should be detailed enough to allow us to recreate your INTEGRATED-DATASET file exactly from scratch from the NYC Open Data site.

## The internal design of our a-priori algorithm:
We simply use the original version, which is Section 2.1 and 2.1.1 of the Agrawal and Srikant paper in VLDB 1994.
The algorithms has two step:
1. Generate all large item sets the union of Lk for k=2...k, which all have support greater than our minimum support.
  - To be more specific, when we 
2. Generate Association Rule for those union of Lk.

The command line specification of a compelling sample run (i.e., a min_sup, min_conf combination that produces association rules that are revealing, surprising, useful, or helpful; see above). Briefly explain why the results are indeed compelling.
Any additional information that you consider significant.
A text file named "example-run.txt" with the output of the compelling sample run of point 3f, listing all the frequent itemsets as well as association rules for that run, as discussed in the Association Rule Mining Algorithm section above.
