from math import log
import operator
import itertools

#################################################################################
#
# indexer: takes in the input_file and creates an inverted index and saves it to
#        the disc with the name provided in output_file
#
#################################################################################

def indexer(input_file, output_file):
    with open(input_file, 'r') as f:
        link_file = [line.strip() for line in f]

    # Used to store the document as key and the value would be the text for that doc id
    list = {}
    key = 0

    # Create a Dictionary with key as the document id and value as its text
    for i in link_file:
        if i.startswith('#'):
            # Get the key
            key = i[2:]
            list[key] = ""
        else:
            # Append text to the value of dictionary
            list[key] = list[key]+ " " + i

    # Used to store the inverted index. Key is the word and value will be a dictionary.
    # The value of Result
    word_index = {}

    for docId in list.keys():

        document = list[docId].split(' ')

        for word in document:

            # Do nothing for empty words
            if word == "":
                continue

            # Do nothing for Digit
            if word.isdigit():
                continue

            # Check if a word_index already contains the word
            if word in word_index.keys():
                docId_tf = word_index[word]
                # Check if docId already exists for this word
                if docId in docId_tf.keys():
                    docId_tf[docId] += 1
                else:
                    docId_tf[docId] = 1

            # If it does not than add it
            else:
                docId_tf = {}
                docId_tf[docId] = 1
                word_index[word] = docId_tf


    print("Index Created. Writing to File Now.")

    # Write to an output file. The file name is the one provided.
    f = open(output_file, 'w')
    f.write(str(word_index))
    f.close()


#################################################################################
#
#  bm25 : Fetches the inverted indexes from disc using the file - indexed_file
#         Fetches the queries from disc using file - queries_file
#         Fetches the maximum results to be shown using - q_size
#         Returns the output on screen/console of the rank/BM25 score of the top
#            q_size documents
#
#################################################################################

def bm25(indexed_file, queries_file, results_file, q_size=100):

    # Open and fetch the inverted index file
    index_dict = eval(open(indexed_file).read())

    # Used to store the docum
    doc_length = {}
    for word in index_dict.keys():

        docId_tf = dict(index_dict[word])

        for docId, tf in docId_tf.items():

            if docId in doc_length.keys():
                doc_length[docId] += tf
            else:
                doc_length[docId] = tf

    # N is the total number of documents in the given collection
    N = len(doc_length)

    sum = 0
    for docId in doc_length.keys():
        sum += doc_length[docId]

    # avdl is the average document length
    avdl = sum / N

    # Open and fetch the queries from the queries_file
    with open(queries_file, 'r') as f:
        queries_list = [line.strip() for line in f]

    # query_results is used to store results of every query
    query_results = []

    for query in queries_list:

        # Store the result of each query in this
        query_score = {}

        # Get words after splitting query
        for word in query.split(" "):

            # Check if word is present in inverse index
            if word in index_dict.keys():

                docId_tf = dict(index_dict[word])

                # Number of documents containing the term - word
                n = len(docId_tf)

                for docId, tf in docId_tf.items():

                    # Calculate the BM25 score
                    score = calculate_BM25_score(n, N, avdl, doc_length[docId], tf, 1)

                    # Check and store the score
                    if docId in query_score.keys():
                        query_score[docId] += score
                    else:
                        query_score[docId] = score

        query_results.append(query_score)


    # Query Id to be displayed or printed on screen
    queryId = 0

    f = open(results_file, 'w')

    print("query_id\tQ0\tdoc_id\trank\t\tBM25_score\tsystem_name")
    f.write("query_id\tQ0\tdoc_id\trank\t\tBM25_score\tsystem_name\n")

    # Fetch each query score from the query results
    for query_score in query_results:

        # Update the Query Id
        queryId += 1

        # Sort the results based on bm score for each query
        sorted_score = sorted(sorted(query_score.items()), key=operator.itemgetter(1), reverse=True)

        # Rank is zero on start
        rank = 0
        for value in itertools.islice(sorted_score, 0, q_size):

            rank += 1

            print("{0}\t\t\tQ0\t{1:4}\t{2}\t{3:.15f}\tAnirudh-PC".format(
                queryId, value[0], rank, value[1]))
            f.write("{0}\t\tQ0\t{1:4}\t{2}\t{3:.15f}\tAnirudh-PC\n".format(
                queryId, value[0], rank, value[1]))

    f.close()


#################################################################################
#
# calculate_BM25_score : Compute BM25 scores for documents in the lists.
# r = Relevant documents containing the term i
# n = Number of documents containing the term i
# N = Total number of documents in the given collection
# k1, k2, and K are parameters whose values are set empirically.
# b = Regulates the impact of the length normalization
# dl = The length of the document
# avdl = The average document length
# R = The relevance information
# f = The frequency of the ith term in the document
# qf = The frequency of term i in the query
#
#################################################################################
# Since relevance is given as zero
r = 0
R = 0
# Constants provided
k1 = 1.2
k2 = 100
b = 0.75

def calculate_BM25_score(n, N, avdl, dl, f, qf):
    K = k1*((1-b)+b*(float(dl)/float(avdl)))
    exp1 = log(((r+0.5)/(R-r+0.5))/((n-r+0.5)/(N-n-R+r+0.5)))
    exp2 = ((k1 + 1) * f)/(K + f)
    exp3 = ((k2+1)*qf)/(k2+qf)
    return exp1 * exp2 * exp3


#################################################################################
#
# THIS IS THE START OF THE PROGRAM
#
#################################################################################

while True:
    i = input("Please enter the command or any other key to exit ")
    try:
        args = i.split(" ")

        # If the first argument is indexer than call the indexer
        if args[0] == "indexer":
            indexer(args[1], args[2])
            print("\nIndexes written to file - ", args[2])

        # If the first argument is bm25 than call the bm25 algo
        elif args[0] == "bm25":
            bm25(args[1], args[2], args[5], int(args[3]))
            break

        # else break from the loop and exit
        else:
            print("Exiting the program..")
            break

    except IndexError:
        print("Incorrect number of arguments")
        print("  For Indexing use - indexer <input_file> <index_out>")
        print("  For BM25 algo use - bm25 <index_out> <queries_file> <size> > <results_file>")
    except FileNotFoundError:
        print("File not found. Please check the file name and try again")


