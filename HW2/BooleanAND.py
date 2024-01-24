import gzip
import sys
import os
import json

def queries_creator(term_files_path, queries_file):
    # queries_path = term_files_path + "/" + queries_file
    # can use this path, if queries file is stored in the term files path ^
    queries_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/msci-541-f23-hw2-matterxleben/topics files/" + queries_file
    
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

def results_retrieval(postings_list):
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

def tokenizer(text):
    tokens = []
    text = text.lower()
    # print(text)
    start = 0
    i = 0

    for count, char in enumerate(text):
        # print(char)
        if not char.isalnum() :
            if start != count :
                # print(text[start:count-start])
                tokens.append(text[start:count])
            start = count + 1
    #if start != count :
    tokens.append(text[start:count+1])
    #print(tokens)
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
    id_to_docno_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/id_map/id_to_docno/id_to_docno.txt"

    if os.path.exists(id_to_docno_path):
        with open(id_to_docno_path , 'r', encoding='utf-8') as file:
            docno_list = file.read().splitlines()
    else:
        print("The path to the id map does not exist!")
        sys.exit()

    return(docno_list)

def output(topicID, docno_list, run_tag, answer):
    output_list = []
    rank = 0
    score = 0

    for doc_id in answer:
        docno = docno_list[doc_id]
        rank += 1
        score = len(answer) - rank
        output_line = f"{topicID} Q0 {docno} {rank} {score} {run_tag}"
        output_list.append(output_line)
    return output_list

def save_output(total_answer, results_file, term_files_path) :
    results_path ="C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/msci-541-f23-hw2-matterxleben/" + results_file

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


def main():
    # check if command line inputs from user are what is required
    if len(sys.argv) != 4 :
        print(
            """
            This input does not meet the requirements for this program! 
            The BooleanAND program's goal is to efficiently retrieve documents and based on input queries from the user.
            
            The program accepts three command line arguments: 
            the directory location of your index, the queries file, and the name of a file to store your output
                1. a path to the location of your index, created by IndexEngine
                2. the queries file
                3. the name of a file to store your output
            
            For example, you would run BooleanAND from the command prompt / terminal / shell as:
                python BooleanAND.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files queries.txt test-results.txt
            """
        )
        sys.exit()

    # command line inputs from user
    # python BooleanAND.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files queries.txt hw2-results-merxlebe.txt
    
    term_files_path = sys.argv[1]
    queries_file = sys.argv[2]
    results_file = sys.argv[3]

    #term_files_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files"
    #queries_file = "queries.txt"
    #results_file = "hw2-results-merxlebe.txt"

    queries = queries_creator(term_files_path, queries_file)
    inverted_index = inverted_index_load(term_files_path)
    print("Done loading inverted index!")

    lexicon = lexicon_load(term_files_path)
    docno_list = id_maps()
    answer = []
    total_answer = []
    run_tag = "merxlebeAND"
    
    # for count in range(1, 3, 2):
    for count in range(1, len(queries) + 1, 2):
        query = queries[count]
        
        tokens = tokenizer(query)
        # print(tokens)
        term_ids = lexicon_tokens(lexicon, tokens)
        postings_list = inverted_index_terms(inverted_index, term_ids)
        answer = results_retrieval(postings_list)

        topicID = queries[count-1]
        output_list = output(topicID, docno_list, run_tag, answer)
        total_answer += output_list

    save_output(total_answer, results_file, term_files_path)
    print("Output saved!")

if __name__=="__main__":
    main()