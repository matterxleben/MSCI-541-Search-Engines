import gzip
import sys
import os
import json

# this is the code for MSCI 541 HW2 Problem 1

def dir_creator(mmddyy, store_path) :
    mm = mmddyy[0:2]
    dd = mmddyy[2:4]
    yy = mmddyy[4:6]

    # Parent Directory
    #parent_dir = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/dates" # user input
    parent_dir = store_path

    # Leaf directory
    directory = f"files/{yy}/{mm}/{dd}"

    # docs dir
    docs_directory = directory + "/docs"

    # meta_data dir
    meta_data_directory = directory + "/meta_data"
    
    # Path
    docs_path = os.path.join(parent_dir, docs_directory)

    meta_data_path = os.path.join(parent_dir, meta_data_directory)

    # Create the directory
    # docs
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        #print("Directory '%s' created" %docs_directory)

    # meta data
    if not os.path.exists(meta_data_path):
        os.makedirs(meta_data_path)
        #print("Directory '%s' created" %meta_data_directory)
        
    return(docs_path, meta_data_path)
    
def save_files(doc, mmddyy, docno, meta_data, store_path) :

    docs_path, meta_data_path = dir_creator(mmddyy, store_path) 
    docs_path += f"/{docno}.txt"
    meta_data_path += f"/{docno}.json"

    with open(docs_path, 'w', encoding='utf-8') as file:
        # Write the string to the file
        file.write(doc)

    with open(meta_data_path, 'w', encoding='utf-8') as json_file:
        # Serialize the dictionary to JSON and write it to the file
        json.dump(meta_data, json_file)

def date_maker(docno) :
    mm = docno[2:4].strip()
    dd = docno[4:6].strip()
    yy = docno[6:8].strip()

    month_map = {
        '01':'January',
		'02':'February',
		'03':'March',
		'04':'April',
		'05':'May',
		'06':'June',
		'07':'July',
		'08':'August',
		'09':'September',
		'10':'October',
		'11':'November',
		'12':'December'
    }

    month = month_map[mm]
    day = dd.lstrip("0")
    year = "19" + yy
    mmddyy = mm + dd + yy
    date = month + " " + day + ", " + year

    return(date, mmddyy)

def meta_data_creator(docno, internal_id, date, headline):
    meta_data = {
        'docno' : docno,
		'internal id' : internal_id,
		'date' : date,
		'headline' : headline,
    }
    return (meta_data)

def docno_to_id_dict(docno_list) :
    return({docno: internal_id for internal_id, docno in enumerate(docno_list)})

def id_map(docno_list, store_path):
    docno_dict = docno_to_id_dict(docno_list)
    
    id_to_docno_path, docno_to_id_path = id_map_dir(store_path)

    id_to_docno_path += "/id_to_docno.txt"
    docno_to_id_path += "/docno_to_id.json"

    # Open the file in write mode ('w') and specify the encoding as 'utf-8'
    with open(id_to_docno_path, 'w', encoding='utf-8') as file:
        for index, docno in enumerate(docno_list):
            if index == len(docno_list) - 1:
                # Last docno in the list don't write a newline
                file.write(docno)
            else:
                # Write a newline after the docno
                file.write(docno + '\n')
    with open(docno_to_id_path, 'w', encoding='utf-8') as json_file:
        # Serialize the dictionary to JSON and write it to the file
        json.dump(docno_dict, json_file)

def id_map_dir(store_path) :
    parent_dir = store_path
    directory = "id_map"

    # id_to_docno list
    id_to_docno_directory = directory + "/id_to_docno"
    # docno_to_id dict
    docno_to_id_directory = directory + "/docno_to_id"
    
    # Path
    id_to_docno_path = os.path.join(parent_dir, id_to_docno_directory)
    docno_to_id_path = os.path.join(parent_dir, docno_to_id_directory)

    # id_to_docno
    if not os.path.exists(id_to_docno_path):
        os.makedirs(id_to_docno_path)

    # id_to_docno
    if not os.path.exists(docno_to_id_path):
        os.makedirs(docno_to_id_path)
    
    return(id_to_docno_path, docno_to_id_path)

def save_term_files(doc_lengths, inverted_index, lexicon, lexicon_id_to_term, store_path):
    
    term_files_path = term_files_dir(store_path)

    doc_lengths_path = term_files_path + "/doc_lengths.txt"
    inverted_index_path = term_files_path + "/inverted_index.json"
    lexicon_path = term_files_path + "/lexicon.json"
    lexicon_id_to_term_path = term_files_path + "/lexicon_id_to_term.json"
    
    with open(doc_lengths_path, 'w', encoding='utf-8') as file:
        for index, length in enumerate(doc_lengths):
            if index == len(doc_lengths) - 1:
                # Last doc in the list don't write a newline
                file.write(str(length))
            else:
                # Write a newline after the doc length
                file.write(str(length) + '\n')
    
    with open(inverted_index_path, 'w', encoding='utf-8') as json_file:
        # Serialize the dictionary to JSON and write it to the file
        json.dump(inverted_index, json_file)
    
    with open(lexicon_path, 'w', encoding='utf-8') as json_file2:
        # Serialize the dictionary to JSON and write it to the file
        json.dump(lexicon, json_file2)
    
    with open(lexicon_id_to_term_path, 'w', encoding='utf-8') as json_file3:
        # Serialize the dictionary to JSON and write it to the file
        json.dump(lexicon_id_to_term, json_file3)

def term_files_dir(store_path) :
    parent_dir = store_path
    directory = "term_files"

    # Path
    term_files_path = os.path.join(parent_dir, directory)

    if not os.path.exists(term_files_path):
        os.makedirs(term_files_path)

    return(term_files_path)


def tokenizer(text):
    tokens = []
    text = text.lower()
    # print(text)
    start = 0
    i = 0

    for count, char in enumerate(text):
        #print(char)
        if not char.isalnum() :
            if start != count :
                # print(text[start:count-start])
                tokens.append(text[start:count])
            start = count + 1
    #if start != count :
    #    tokens.append(text[start:count])
    #print(tokens)
    return(tokens)

def convert_tokens_to_ids(tokens, lexicon, lexicon_id_to_term):
    token_ids = []
    for count, token in enumerate(tokens):
        if token in lexicon :
            token_ids.append(lexicon[token])
        else :
            token_id = len(lexicon)
            lexicon[token] =  token_id #length of dictionary, add term ID as length of lexicon to put it at end
            lexicon_id_to_term[token_id] = token # also the vice versa lexicon
            token_ids.append(token_id)
    
    return token_ids # returns token ids that are in this document

def count_words(token_ids) :
    word_counts = {} # of term id (int) ----> count in current document  (int)
    for token_id in token_ids :
        if token_id in word_counts :
            word_counts[token_id] += 1
        else :
            word_counts[token_id] = 1
    return word_counts

def add_to_postings(word_counts, doc_id, inverted_index) :
    for term_id in word_counts :
        count = word_counts[term_id]
        if term_id in inverted_index:
            postings = inverted_index[term_id] # inverted index stores list of docid, then count, (as value), accessed by term id (as its key)
        else :
            postings = []

        postings.append(doc_id)
        postings.append(count)
        inverted_index[term_id] = postings


def main():
    #initialize variables
    docno_list = []
    doc = ""
    date = ""
    headline = ""
    text = ""
    graphic = ""
    is_headline = False
    is_text = False
    is_graphic = False
    lexicon = {}
    lexicon_id_to_term = {}
    inverted_index = {}
    doc_lengths = []

    # check if command line inputs from user are what is required
    if len(sys.argv) != 3 :
        print(
            """
            This input does not meet the requirements for this program!
            The IndexEngine program's goal is to read the latimes.gz file and be able to store separately each document and its associated metadata.
            
            This program accepts two command line arguments:
                1. a path to the latimes.gz file
                2. a path to a directory where the documents and metadata will be stored.
            
            For example, you would run IndexEngine from the command prompt / terminal / shell as:
                python IndexEngine.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/raw-data/latimes.gz C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/store
            """
        )
        sys.exit()

    # command line inputs from user
    data_path = sys.argv[1]
    store_path = sys.argv[2]

    if not os.path.exists(data_path) :
        print("This path does not exist! Please enter the correct path to the latimes data!")
        sys.exit()

    if os.path.exists(store_path):
        print("This storing directory already exists! Please enter a new storing directory that does not already exist (or delete the directory off your DISK that your are looking to store to) and rerun this program!")
        sys.exit()
    elif not os.path.exists(store_path):
        os.makedirs(store_path)
        print(f"Created the directory: {store_path}")

    #data_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/raw-data/latimes.gz"
    #store_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/dates"
    # user input: C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/raw-data/latimes.gz C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/dates
    

    with gzip.open(data_path,'rt') as f:
        for line in f:
                if "</DOC>" in line:
                    doc += line.strip() # take out last /n from last line
                    meta_data = meta_data_creator(docno, docno_list.index(docno), date, headline.strip())
                    save_files(doc, mmddyy, docno, meta_data, store_path) # SAVE DOC TO DIRECTORY (CALL A FUNCTION TO DO THAT)
                    doc = "" # re-instate doc as empty string
                    
                    
                    tokens = tokenizer(headline + text + graphic) # tokenizing
                    doc_lengths.append(len(tokens)) # add number of words in doc to doc lenghts list

                    token_ids = convert_tokens_to_ids(tokens, lexicon, lexicon_id_to_term) # adding to lexicon (if term doesnt exist there already), AND add tokenIDs to token id list
                    word_counts = count_words(token_ids) # term ID to count in document dictionary
                    add_to_postings(word_counts, docno_list.index(docno), inverted_index) # adds doc id to posting list for each term in document, and adds that to inverted index at termid key



                    headline = ""
                    text = ""
                    graphic = ""
                else :
                    doc += line
                    if is_headline == True and "<P>" not in line and "</P>" not in line and "</HEADLINE>" not in line:
                        headline += line.strip() + " "
                    elif is_text == True and "<P>" not in line and "</P>" not in line and "</TEXT>" not in line:
                        text += line.strip() + " "
                    elif is_graphic == True and "<P>" not in line and "</P>" not in line and "</GRAPHIC>" not in line:
                        graphic += line.strip() + " "
                    elif "<DOCNO>" in line:
                        docno = line[7:line.index("</DOCNO>")].strip() # <DOCNO> is 0-6 index, therefore 7 is start of index
                        docno_list.append(docno)
                        date, mmddyy = date_maker(docno)
                    elif "<HEADLINE>" in line:
                        is_headline = True
                    elif "</HEADLINE>" in line:
                        is_headline = False
                    elif "<TEXT>" in line:
                        is_text = True
                    elif "</TEXT>" in line:
                        is_text = False
                    elif "<GRAPHIC>" in line:
                        is_graphic = True
                    elif "</GRAPHIC>" in line:
                        is_graphic = False

    
    # is_graphic = False


    id_map(docno_list, store_path)
    save_term_files(doc_lengths, inverted_index, lexicon, lexicon_id_to_term, store_path)

    print("Completed storing all documents and metadata in the respective directory!")         

if __name__=="__main__":
    main()