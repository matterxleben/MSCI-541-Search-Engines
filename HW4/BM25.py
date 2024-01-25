import gzip
import sys
import os
import json
import math
from porter_stemmer import PorterStemmer

def queries_creator(term_files_path, queries_file):
    # queries_path = term_files_path + "/" + queries_file
    # can use this path, if queries file is stored in the term files path ^
    queries_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/msci-541-f23-hw4-matterxleben/topics files/" + queries_file
    
    if os.path.exists(queries_path):
        with open(queries_path , 'r', encoding='utf-8') as file:
            queries = file.read().splitlines()
    else:
        print("This path does not exist! Please enter the correct file name for your queries!")
        sys.exit()
    return queries

def inverted_index_load(term_files_path):
    inverted_index_path = term_files_path + "/inverted_index.json"
    #inverted_index_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files/inverted_index.json"
    
    if os.path.exists(inverted_index_path):
        with open(inverted_index_path, 'r', encoding='utf-8') as json_file:
            inverted_index = json.load(json_file)
    else:
        print("This path does not exist! Please enter the correct path to the index!")
        sys.exit()

    return inverted_index

def lexicon_load(term_files_path):
    lexicon_path = term_files_path + "/lexicon.json"
    # lexicon_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files/lexicon.json"
    

    if os.path.exists(lexicon_path):
        with open(lexicon_path, 'r', encoding='utf-8') as json_file:
            lexicon = json.load(json_file)
    else:
        print("This path does not exist! Please enter the correct path to the index!")
        sys.exit()

    return lexicon

def doc_lengths_load(term_files_path):
    doc_lengths_path = term_files_path + "/doc_lengths.txt"
    # lexicon_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files/lexicon.json"
    
    if os.path.exists(doc_lengths_path):
        with open(doc_lengths_path , 'r', encoding='utf-8') as file:
            doc_lengths = [int(doc_length) for doc_length in file.read().splitlines()]
    else:
        print("This path does not exist! Please enter the correct file name for your doc lengths file!")
        sys.exit()
    return doc_lengths

def bm25_retrieval(postings_list, doc_lengths):
    
    # iter = 2 for first one, = 1 for next ones due to results being just docids
    answer = []
    p1 = postings_list[0]

    if len(postings_list) == 1 :
        i = 0
        while i != len(p1) :
            answer.append(p1[i])
            i += 2
    else : 
        for count in range(1, len(postings_list)):
            p2 = postings_list[count]
            if count == 1:
                answer = intersect(p1,p2,2)
            else:
                answer = intersect(p1,p2,1)
            p1 = answer
            #print(answer)
    return answer

def intersect(p1, p2, iter) :
    i=0
    j=0
    answer = []

    while i != len(p1) and j != len(p2):
        if p1[i] == p2[j] :
            answer.append(p1[i])
            i += iter
            j += 2
        else :
            if p1[i] < p2[j] :
                i += iter
            else :
                j += 2
    return answer

def k_function(doc_length, average_doc_length):
    k1 = 1.2
    b = 0.75
    return k1*((1.0 - b) + b*(doc_length / average_doc_length))



def tokenizer(text, porter_stemmer):
    tokens = []
    text = text.lower()
    # print(text)
    start = 0
    i = 0

    for count, char in enumerate(text):
        # print(char)
        if not char.isalnum() :
            if start != count :

                token = text[start:count]
                #stemmed_token = porter_stemmer.stem(token, 0, len(token) - 1)
                tokens.append(token)
            start = count + 1

    token = text[start:count+1]
    #stemmed_token = porter_stemmer.stem(token, 0, len(token) - 1)
    tokens.append(token)
    return(tokens)

def lexicon_tokens(lexicon, tokens):
    term_ids = []
    for token in tokens :
        if token in lexicon : # if the term does not appear in vocab at all, remove it from the query and return results for the ones that do
            term_ids.append(lexicon[token])
        else :
            print(f"The term {token} does not appear in the lexicon! Therefore, it has been removed from the query!")
    return term_ids

def inverted_index_terms(inverted_index, term_ids) :
    postings_list = []
    for term_id in term_ids :
        postings_list.append(inverted_index[str(term_id)])
    return postings_list

def id_maps():
    id_to_docno_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/store/id_map/id_to_docno/id_to_docno.txt"

    if os.path.exists(id_to_docno_path):
        with open(id_to_docno_path , 'r', encoding='utf-8') as file:
            docno_list = file.read().splitlines()
    else:
        print("The path to the id map does not exist!")
        sys.exit()

    return(docno_list)

def output(topicID, docno_list, run_tag, sorted_accumulator):
    output_list = []
    rank = 0
    score = 0

    for doc_id in sorted_accumulator:
        if rank < 1000 :
            docno = docno_list[doc_id]
            rank += 1
            score = sorted_accumulator[doc_id]
            output_line = f"{topicID} Q0 {docno} {rank} {score} {run_tag}"
            output_list.append(output_line)
    return output_list

def save_output(total_answer, results_file, term_files_path) :
    results_path ="C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/msci-541-f23-hw4-matterxleben/results/" + results_file

    if not os.path.exists(results_path):
        with open(results_path, 'w', encoding='utf-8') as file:
            for index, item in enumerate(total_answer):
                if index == len(total_answer) - 1:
                    # Last in the list don't write a newline
                    file.write(item)
                else:
                    # Write a newline after the item
                    file.write(item + '\n')
    else:
        print("The output file already exists! Please enter a new name for your results file, or delete the previously stored file and rerun this program!")
        sys.exit()

def average_doc_length_calculator(doc_lengths):
    if not doc_lengths:
        return 0
    return round(sum(doc_lengths) / len(doc_lengths), 4)

def frequency_calculator(term_posting_list, doc_id, index) :
    freq_term_in_doc = 0
    i = 0
    while i != len(term_posting_list):
        if term_posting_list[i] == doc_id :
            freq_term_in_doc = term_posting_list[i+1]
            break
        i += 2
    return freq_term_in_doc

def bm25_score(N, ni, k, fi):
    return (fi / (k + fi))*math.log((N - ni + 0.5) / (ni + 0.5))


def main():
    # check if command line inputs from user are what is required
    if len(sys.argv) != 4 :
    #    print(
            """
            This input does not meet the requirements for this program! 
            The BM25 program's goal is to efficiently retrieve documents and based on input queries from the user, by performing BM25 Retrieval.
            
            The program accepts three command line arguments: 
            the directory location of your index, the queries file, and the name of a file to store your output
                1. a path to the location of your index, created by IndexEngine
                2. the queries file
                3. the name of a file to store your output
            
            For example, you would run BM25.py from the command prompt / terminal / shell as:
                python BM25.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/store/term_files queries.txt hw4-bm25-baseline-merxlebe.txt
            """
    #    )
    #    sys.exit()

    # command line inputs from user
    # python BooleanAND.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files queries.txt hw2-results-merxlebe.txt
    
    term_files_path = sys.argv[1]
    queries_file = sys.argv[2]
    results_file = sys.argv[3]

    #term_files_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/store/term_files"
    #queries_file = "queries.txt"
    #results_file = "hw4-bm25-stem-merxlebe.txt"
    
    porter_stemmer = PorterStemmer()

    queries = queries_creator(term_files_path, queries_file)
    inverted_index = inverted_index_load(term_files_path)
    print("Done loading inverted index!")

    lexicon = lexicon_load(term_files_path)
    docno_list = id_maps()
    doc_lengths = doc_lengths_load(term_files_path)
    total_answer = []
    run_tag = "merxlebeAND"
    N = len(docno_list)


    

    average_doc_length = average_doc_length_calculator(doc_lengths)
    
    # for count in range(1, 3, 2):
    for count in range(1, len(queries) + 1, 2):
        query = queries[count]
        
        tokens = tokenizer(query, porter_stemmer)
        term_ids = lexicon_tokens(lexicon, tokens)
        postings_list = inverted_index_terms(inverted_index, term_ids)
        topicID = queries[count-1]




        accumulator = {}
                
        # term at at time
        for count, term_id in enumerate(term_ids):
            term_posting_list = postings_list[count]
            ni = len(term_posting_list) / 2.0

            # for each doc
            i = 0
            while i != len(term_posting_list):
                
                doc_id = term_posting_list[i]
                freq_term_in_doc = term_posting_list[i+1]
                k = k_function(doc_lengths[doc_id], average_doc_length)

                # check if it contains in dict
                if doc_id in accumulator.keys() :
                    accumulator[doc_id] += bm25_score(N, ni, k, freq_term_in_doc)
                else :
                    accumulator[doc_id] = bm25_score(N, ni, k, freq_term_in_doc)
                i += 2
        
        # save scores for the query

        sorted_accumulator = dict(sorted(accumulator.items(), key = lambda x : x[1], reverse=True))
        output_list = output(topicID, docno_list, run_tag, sorted_accumulator)
        total_answer += output_list

    save_output(total_answer, results_file, term_files_path)
    print("Output saved!")

if __name__=="__main__":
    main()