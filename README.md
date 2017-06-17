# BM25 Algorithm

This script can be used to create inverted indexes for any given input file. The input file should be of follow the given format:
a) A # followed by a document ID
b) Lines below the document ID line contain stemmed words from the document.

After index has been created, than this script can be used to calculate the BM25 algorithm for the given set of queries.

Numerical tokens have been ignored in this script.

## SETUP

1. Download the latest version of python - "Python 3.5.0".
2. Install PyCharm.
3. Execute code. 

## ABOUT THE CODE

1. The code is divided into 2 significan portions. One part is the indexer and the other is the BM25 score calculator

2. The script request user input.

3. If the input is of type 'indexer <file_to_be_indexed> <inverted_index_output>'. Than the indexer method is invoked. Example
indexer tccorpus.txt index.out
In this case the indexer will be called to read the file 'tccorpus.txt' and will print the output as 'index.out'. The input file in this case must follow the format # followed by document id and than the lines below the document id should be the words.

4. If the input is of type bm25 <inverted_index_file> <input_queries> <Output_size> > <results_file>. In this case the bm25 method will be invoked. Example
bm25 index.out queries.txt 100 > results.eval
In this case the bm25 method will take the input of the inverted index file 'index.out' and the input queries as 'queries.txt'. The max results per query were input as '100'. The output will both be printed on screen and also saved to file named - 'results.eval'


## CONTACT

Please contact 'Anirudh Devgun' at 'devgun.a@husky.neu.edu' in case of any issues.