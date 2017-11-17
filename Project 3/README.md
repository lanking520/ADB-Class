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
We use **DOHMH New York City Restaurant Inspection Results**.## What makes your choice of INTEGRATED-DATASET file compelling (in other words, justify your choice of NYC Open Data data set(s)). The explanation should be detailed enough to allow us to recreate your INTEGRATED-DATASET file exactly from scratch from the NYC Open Data site.

## How do you map the original NYC Open Data data set(s) into your INTEGRATED-DATASET file: 
A row of this data set is like:<br>
|  Resuarant Location   |  Food Style |   Grade   |  Grade Date  |

So this data set is not the ordinary True-False table, which means that we must make numeric data to some interval to make association rule mining works. <br>
So <br> 
1. We make a coarse catergorize for the Food Style, for example: Chinese and Korean are all considered as Asian, Hamberger and BBQ are considered as NorthAmerican. 
2. We convert Grade Date into interval, that is by Season.

We the the two above mapping, we make a very fine data coarser, so that more data will satisfy our min_sup, and therefore find more interesting assocation rule. <br>



## The internal design of our a-priori algorithm:
We simply use the original version, i.e. Section 2.1 and 2.1.1 of the Agrawal and Srikant paper in VLDB 1994.
The algorithms has two step:
1. Generate all large item sets, the union of Lk for k=2...k, that all have support greater than our minimum support.
  - To be more specific, we first get large 1 item set L1, and a for loop that using Lk-1 to generate Ck. Ck is the candidate of large k item set, the candidate who survive through the min_sup can be part of Lk, and the list goes on.
  - The algorithm to generate Ck using Lk-1 is also the same as the paper, which is simply by comparing all entry except the last entry, and do some pruning to eliminate Ck those have impossible subset.
2. Generate Association Rule for those union of Lk. Make every bianry partition for every item_set that is qualified, and try to compute the confidence for this pair.


## 下面這個部分等你改一改之後再寫，我覺得我們parser可以改一下，把沒用的column全部刪掉，然後date只要樓grade date就好了這樣就不用特別標注是grade date還是inspection date了。 然後我覺得可以把food type的other裡面的一些東西強行歸類到北美 南美或亞洲，這樣也許可以找到多一點confidence。例如coffee就可以歸類到北美但現在是在other分類。 
The command line specification of a compelling sample run (i.e., a min_sup, min_conf combination that produces association rules that are revealing, surprising, useful, or helpful; see above). Briefly explain why the results are indeed compelling.
Any additional information that you consider significant.
A text file named "example-run.txt" with the output of the compelling sample run of point 3f, listing all the frequent itemsets as well as association rules for that run, as discussed in the Association Rule Mining Algorithm section above.
