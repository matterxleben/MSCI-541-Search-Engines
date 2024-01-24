import gzip
import sys
import os
import json

def id_maps(store_path):
    id_to_docno_path = store_path + "/id_map/id_to_docno/id_to_docno.txt"

    if os.path.exists(id_to_docno_path):
        with open(id_to_docno_path , 'r', encoding='utf-8') as file:
            docno_list = file.readlines()
    else:
        print("This path does not exist! Please enter the correct path to the documents and meta data!")
        sys.exit()

    docno_list = [docno.strip() for docno in docno_list] # Remove trailing newline characters from each line

    docno_to_id_path = store_path + "/id_map/docno_to_id/docno_to_id.json"
    if os.path.exists(id_to_docno_path):
        with open(docno_to_id_path, 'r', encoding='utf-8') as json_file:
            docno_to_id_dict = json.load(json_file)
    else:
        print("This path does not exist! Please enter the correct path to the documents and meta data!")
        sys.exit()
    
    return(docno_list, docno_to_id_dict)

def internal_id_fetch(docno_list, id_value):
    if (len(docno_list)-1) >= int(id_value) :
        return(docno_list[int(id_value)])
    else :
        print("This Internal ID does not exist! Please enter a correct Internal ID for a document!")
        sys.exit()

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
    # check if command line inputs from user are what is required
    if len(sys.argv) != 4 :
        print(
            """
            This input does not meet the requirements for this program! 
            The GetDoc program's goal is to efficiently retrieve a document and its metadata, based on inputs from the user.
            
            The program accepts three command line arguments: 
                1. a path to the location of the documents and metadata store created by the first program (IndexEngine)
                2. either the string "id" or the string "docno"
                3. either the internal integer id of a document or a DOCNO
            
            For example, you would run GetDoc from the command prompt / terminal / shell as:
                python GetDoc.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/store docno LA010189-0003
            OR
                python GetDoc.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/store id 2
            """
        )
        sys.exit()

    # command line inputs from user
    # C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/store
    store_path = sys.argv[1]
    id_type = sys.argv[2]
    id_value = sys.argv[3]

    docno_list, docno_to_id_dict = id_maps(store_path)    
    
    if id_type == 'id' :
        docno = internal_id_fetch(docno_list, id_value)
    elif id_type == 'docno' :
        docno = id_value
    else :
        print("This input does not meet the requirements for this program! Please supply either \"id\" or \"docno\" as the second argument to the program on the command line.")
        sys.exit()

    docs_path, meta_data_path = paths(docno, store_path)


    doc = doc_retrival(docs_path)
    meta_data = meta_data_retrival(meta_data_path)

    print(f"docno: {meta_data['docno']}\ninternal id: {meta_data['internal id']}\ndate: {meta_data['date']}\nheadline: {meta_data['headline']}")
    print(f"raw document:\n{doc}")

if __name__=="__main__":
    main()