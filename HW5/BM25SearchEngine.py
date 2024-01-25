import gzip
import sys
import os
import json
import math
import time

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

def tokenizer(text):
    tokens = []
    token = ''
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
    
    if len(text) > 1:
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
    id_to_docno_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW5/store/id_map/id_to_docno/id_to_docno.txt"

    if os.path.exists(id_to_docno_path):
        with open(id_to_docno_path , 'r', encoding='utf-8') as file:
            docno_list = file.read().splitlines()
    else:
        print("The path to the id map does not exist!")
        sys.exit()

    return(docno_list)

def clean_doc(doc):
    # remove tags from doc
    xml = False
    cleaned_doc = ''
    split_doc = []

    for i in doc:
        if i == '<':
            xml = True
        elif i == '>':
            xml = False
        elif not xml and i != '\n':
            cleaned_doc += i

    cleaned_doc = cleaned_doc.replace('?', ".")
    cleaned_doc = cleaned_doc.replace('!', ".")

    split_doc = cleaned_doc.split(".")

    return split_doc

def snippet_engine(doc, headline, query_tokens):
    split_doc = clean_doc(doc)
    best_snippet_score = 0
    best_snippet = ""
    
    for sent_number, sentence in enumerate(split_doc):
        h = 0
        l = 0
        c = 0
        d = 0
        streak = 0
        query_terms_in_sentence = []
        tokenized_sentence = tokenizer(sentence)

        if headline in sentence: # is headline
            h = 1
        if sent_number == 0 : # first sentence
            l = 2
        elif sent_number == 1 : # second sentence
            l = 1
        
        for count, token in enumerate(tokenized_sentence):
            if token in query_tokens : # in query, include repitions
                c += 1
                if token not in query_terms_in_sentence: # in query, exclude repitions
                    query_terms_in_sentence.append(token)
                    d += 1
                if streak == 0 :
                    streak = 1

                next_count = count + 1
                temp_streak = 1

                while(next_count < len(tokenized_sentence)) :
                    if tokenized_sentence[next_count] not in query_tokens:
                        break
                    temp_streak += 1
                    if temp_streak > streak :
                        streak = temp_streak
                    next_count += 1
        snippet_score = h+(0.1)*l+c+(1.5)*d+(1.5)*streak # scale down l

        if snippet_score > best_snippet_score :
            best_snippet_score = snippet_score
            
            if sent_number < len(split_doc) - 1:
                best_snippet = sentence + "." + split_doc[sent_number+1] + "..."
            else : 
                best_snippet = sentence + "..."

    return best_snippet
            
def output(docno_list, sorted_accumulator, term_files_path, query_tokens):
    output_list = []
    rank = 0
    score = 0
    rank_to_docno = {}

    for doc_id in sorted_accumulator:
        if rank < 10:
            docno = docno_list[doc_id]
            rank += 1
            rank_to_docno[rank] = docno
            doc, meta_data = get_doc(docno, term_files_path)


            snippet = snippet_engine(doc, meta_data['headline'], query_tokens)

            #if meta_data['headline'] = 

            output_line = f"{rank}. {meta_data['headline']} ({meta_data['date']})\n{snippet} ({docno})\n\n"
            output_list.append(output_line)
            #print(output_line)  
    return output_list, rank_to_docno

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

def get_doc(docno, store_path):
    docs_path, meta_data_path = paths(docno, store_path)
    doc = doc_retrival(docs_path)
    meta_data = meta_data_retrival(meta_data_path)
    return doc, meta_data

def paths(docno, store_path) :
    mm = docno[2:4].strip()
    dd = docno[4:6].strip()
    yy = docno[6:8].strip()

    docs_path = store_path + f"/files/{yy}/{mm}/{dd}/docs/{docno}.txt"
    meta_data_path = store_path + f"/files/{yy}/{mm}/{dd}/meta_data/{docno}.json"
    return(docs_path, meta_data_path)

def doc_retrival(docs_path) :
    if os.path.exists(docs_path):
        with open(docs_path , 'r', encoding='utf-8') as file:
            doc = file.read()
        return(doc)
    else : 
        print("This path does not exist! Please enter the correct path to the documents and meta data!")
        sys.exit()

def meta_data_retrival(meta_data_path) :
    if os.path.exists(meta_data_path):
        with open(meta_data_path, 'r', encoding='utf-8') as json_file:
            meta_data = json.load(json_file)
        return(meta_data)
    else :
        print("This path does not exist! Please enter the correct path to the documents and meta data!")
        sys.exit()

def main():
    term_files_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW5/store/term_files"
    store_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW5/store"
   
    inverted_index = inverted_index_load(term_files_path)
    print("Done loading inverted index!")

    lexicon = lexicon_load(term_files_path)
    docno_list = id_maps()
    doc_lengths = doc_lengths_load(term_files_path)
    total_answer = []
    N = len(docno_list)
    average_doc_length = average_doc_length_calculator(doc_lengths)
    new_request = True

    # FIRST ITERATION

    query = input("Please enter a query: ")

    start_time = time.time()

    tokens = tokenizer(query)
    term_ids = lexicon_tokens(lexicon, tokens)
    postings_list = inverted_index_terms(inverted_index, term_ids)

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
    output_list, rank_to_docno = output(docno_list, sorted_accumulator, store_path, tokens)
    total_answer += output_list

    for line in output_list:
        print(line)
    
    # Time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Retrieval took: {round(elapsed_time, 2)} seconds")

    while new_request :
        user_input = input("Please type one of the following options depending on what you would like to do next:\n1. The rank of the document that you would like to view (from 1 to 10)\n2. \"N\", to enter a new query\n3. \"Q\", to quit the program\n")
        
        try:
            int_user_input = int(user_input)

            # check if the input is 1 to 10
            if 1 <= int_user_input <= 10:
                docno = rank_to_docno[int_user_input]
                doc, meta_data = get_doc(docno, store_path)
                print(f"{doc}\n")
            else:
                print("User input seems to be numeric. If the user is trying to see a document based on inputting its rank, please make sure the input is between 1 and 10.")
        # if the user entered a string instead
        except ValueError:
            if user_input == "Q":
                sys.exit()
            elif user_input == "N":

                query = input("Please enter a query: ")

                start_time = time.time()

                tokens = tokenizer(query)
                term_ids = lexicon_tokens(lexicon, tokens)
                postings_list = inverted_index_terms(inverted_index, term_ids)

                accumulator = {}

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
                output_list, rank_to_docno = output(docno_list, sorted_accumulator, store_path, tokens)
                total_answer += output_list

                for line in output_list:
                    print(line)
                
                # Time
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Retrieval took: {round(elapsed_time, 2)} seconds") 
            
if __name__=="__main__":
    main()