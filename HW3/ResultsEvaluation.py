import gzip
import sys
import os
import json
import math

def qrels_retrieval(qrels_path):
    qrels_dict = {}

    if not os.path.exists(qrels_path):
        print("This path does not exist! Please enter the correct path to the qrels doc!")
        sys.exit()
    
    with open(qrels_path , 'r', encoding='utf-8') as file:
        # fence post first topic
        first_line = file.readline()
        curr_topic = first_line[0:3]

        # relevant docs for each topic
        relevant_docs = []

        for line in file:
            # new topic
            if line[0:3] != curr_topic :
                qrels_dict[curr_topic] = relevant_docs
                relevant_docs = []
                curr_topic = line[0:3]
                
            if line[20:21] == "1" :
                relevant_docs.append(line[6:19])

        qrels_dict[curr_topic] = relevant_docs

        return qrels_dict


def results_retrieval(results_path, qrels_dict):

    if not os.path.exists(results_path):
        print("This path does not exist! Please enter the correct path to the results doc!")
        sys.exit()
    
    with open(results_path , 'r', encoding='utf-8') as file:
        # fence post first topic

        first_line = True
        count = 0
        relevant = 0
        relevance_score = 0
        precision_sum = 0
        dcg_sum = 0
        

        for i, line in enumerate(file):

            if len(line) < 24 :
                print(
                f"""
                    This line: {line}is not properly formatted! Each line must be atleast 24 characters long (24 with no username) in the format: 
                    401 Q0 LA021890-0100 1 1 username 
                    Therefore we must cancel the results for this file and exit the program!
                """)
                sys.exit()
            
            if not line[0:3].isnumeric() :
                print(
                f"""This line: {line}is not properly formatted! Each line must be in the format: 
                    401 Q0 LA021890-0100 1 1 username 
                    This line does not have a numeric topic number in the first 3 characters.
                    Therefore we must cancel the results for this file and exit the program!
                """)
                sys.exit()
            
            

            
            # student10.results error handling
            #line = line.replace(']', '')
            #line = line.replace('[', '')
            #print(line)
            
            # If theres a new topic, the past topic is completed
            # do all the things for topic
            count += 1
            relevant = 0

            

            if first_line:
                first_line = False
                curr_topic = line[0:3]
                curr_rel_docs = qrels_dict[curr_topic]
                number_of_rel_docs = float(len(curr_rel_docs))
            
            if line[0:3] != curr_topic:
                
                # error checking for improper formatting (student12)
                # e.g. the smallest the line could possible be is (with no username): 401 Q0 LA021890-0100 1 1, which is 24 characters
                # for student13 topic 410 error handling (if theres less than 10 results for a topic, still need to compute P@10)
                if count-1 < 10 :
                    precision_at_10 = precision * (float(count-1))/10.0



                #number_of_rel_docs = float(len(curr_rel_docs))
                average_precision = precision_sum/number_of_rel_docs
                idcg_sum = idcg_calculator(number_of_rel_docs, False, curr_topic)
                ndcg = ndcg_calculator(dcg_sum, idcg_sum)
                text_output = output(curr_topic, average_precision, precision_at_10, ndcg_at_10, ndcg)
                print(text_output)

                count = 1
                relevance_score = 0
                precision_sum = 0
                dcg_sum = 0
                idcg_sum = 0
                ndcg_at_10 = 0
                idcg_at_10 = 0
                curr_topic = line[0:3]
                curr_rel_docs = qrels_dict[curr_topic]
                number_of_rel_docs = float(len(curr_rel_docs))
                


            # .upper for error handling of student6.results, which has lowercase docno's
            docno = line[7:20]

            if "[" in docno :
                print(f"""
                    This docno: {docno}is not properly formatted! The docno must be 13 characters long in the format: LA123456-7890
                    
                    Therefore we must cancel the results for this file and exit the program!
                    """)
                sys.exit()                

            # student6 lowercase la
            if docno[0:2].islower():
                print(f"""
                    This docno: {docno}is not properly formatted! The docno must be 13 characters long in the format: LA123456-7890
                    
                    Therefore we must cancel the results for this file and exit the program!
                    """)
                sys.exit()

            if not len(docno.strip()) == 13 :
                print(f"""
                    This docno: {docno}is not properly formatted! The docno must be 13 characters long in the format: LA123456-7890
                    
                    Therefore we must cancel the results for this file and exit the program!
                    """)
                sys.exit()

            

            # check if relevant, add to a relevant tally
            if docno in curr_rel_docs :
                relevant = 1
                relevance_score += 1
            

            # calculate precision
            precision = precision_calculator(relevance_score, count)

            # add up precision summation for avg precision later
            precision_at_r = precision_at_rank(relevant, precision)
            precision_sum += precision_at_r

            # DCG
            dcg_at_r = dcg_at_rank(relevant, count)
            dcg_sum += dcg_at_r

            # P@10, NDCG@10
            if count == 10:
                precision_at_10 = round(precision, 4)
                idcg_at_10 = idcg_calculator(number_of_rel_docs, True, curr_topic)
                ndcg_at_10 = ndcg_calculator(dcg_sum, idcg_at_10)
                #print(f"{curr_topic} P@10: {precision_at_10}")
                # call method to calculate precision at 10 and NDCG@10
            




        
        number_of_rel_docs = float(len(curr_rel_docs))
        average_precision = precision_sum/number_of_rel_docs
        idcg_sum = idcg_calculator(number_of_rel_docs, False, curr_topic)
        ndcg = ndcg_calculator(dcg_sum, idcg_sum)
        text_output = output(curr_topic, average_precision, precision_at_10, ndcg_at_10, ndcg)
        print(text_output)


def output(curr_topic, average_precision, precision_at_10, ndcg_at_10, ndcg) :
    return(f"Topic: {curr_topic} AP: {round(average_precision, 4)} P@10: {round(precision_at_10, 4)} NDCG@10: {round(ndcg_at_10, 4)} NDCG@1000: {round(ndcg, 4)}")

def precision_calculator(relevance_score, rank) :
    if rank <= 1000:
        precision = float(relevance_score) / float(rank)
    else: 
        precision = 0.0
    return(precision)

def precision_at_rank(relevant, precision):
    precision_at_rank = (float(relevant))*(float(precision))
    return precision_at_rank

def dcg_at_rank(relevant, rank):
    dcg_at_rank = (float(relevant)) / (math.log(float(rank) + 1,2))
    return dcg_at_rank

def idcg_calculator(number_of_rel_docs, at_10, curr_topic) :
    idcg_sum = 0
    #if curr_topic == "409":
    #    print(number_of_rel_docs)

    
    if at_10 and number_of_rel_docs > 10 :
        number_of_rel_docs = 10
    for i in range(1, int(number_of_rel_docs) + 1): 
        idcg_at_rank = 1.0 / (math.log(float(i) + 1,2))
        idcg_sum += idcg_at_rank
        #if curr_topic == "409":
        #    print("topic is 410", number_of_rel_docs, idcg_at_rank, idcg_sum)
    return (idcg_sum)

def ndcg_calculator(dcg, idcg):
    ndcg = dcg/idcg
    return ndcg



def main():
    # check if command line inputs from user are what is required
    if len(sys.argv) != 3 :
        print(
        """Please enter the correct form for running this program! The program accepts 2 command line arguments: the directory location of your results file, the directory location of your qrels file:
        For example, you would run ResultsEvaluation.py from the command prompt / terminal / shell as:
            python ResultsEvaluation.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW3/hw3-files-2023/results-files/student12.results, C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW3/hw3-files-2023/qrels/LA-only.trec8-401.450.minus416-423-437-444-447.txt
        """
        )
        sys.exit()

    # command line inputs from user
    #results_path = 'C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW3/hw3-files-2023/results-files/student12.results'
    #qrels_path = 'C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW3/hw3-files-2023/qrels/LA-only.trec8-401.450.minus416-423-437-444-447.txt'
    results_path = sys.argv[1]
    qrels_path = sys.argv[2]
    
    
    qrels_dict = qrels_retrieval(qrels_path)
    results_retrieval(results_path, qrels_dict)


if __name__=="__main__":
    main()

