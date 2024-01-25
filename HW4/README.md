# msci-541-f23-hw4-matterxleben

## MSCI 541 - Search Engines: Homework 4

Name: Matthew Erxleben

ID: 20889980

### Installation Requirements:
1.	Please make sure Python is installed on your computer before running the program.
2.	Clone repository on your device by entering this into your terminal: git clone https://github.com/UWaterloo-MSCI-541/msci-541-f23-hw4-matterxleben.git

### Running the Programs
In order to run these programs, please navigate to where you cloned the repository and open the working directory .../msci-541-f23-hw4-matterxleben

#### IndexEngine: 
This program accepts two command line arguments:
1.	a path to the latimes.gz file
2.	a path to a directory where the documents, metadata, and term files will be stored.

For example, you would run IndexEngine from the command prompt / terminal / shell as:
python IndexEngine.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/raw-data/latimes.gz C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/store


#### BM25:

The program accepts three command line arguments: the directory location of your index, the queries file, and the name of a file to store your output
1. a path to the location of your index, created by IndexEngine
2. the queries file
3. the name of a file to store your output

For example, you would run BooleanAND from the command prompt / terminal / shell as:
    python BM25.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/store/term_files queries.txt hw4-bm25-baseline-merxlebe.txt

For this program, the queries file (search topics file) is in the /topics files folder. In the code for the program, the path is hardcoded as:
C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/msci-541-f23-hw4-matterxleben/topics files/" + queries_file

Please change this to your own computers path to the msci-541-f23-hw2-matterxleben/topics files/ folder to obtain the queries (search topics)!


#### ResultsEvaluation.py:

The program accepts 2 command line arguments: 
1. the directory location of your results file
2. the directory location of your qrels file

For example, you would run ResultsEvaluation.py from the command prompt / terminal / shell as:
    python ResultsEvaluation.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/msci-541-f23-hw4-matterxleben/results/hw4-bm25-baseline-merxlebe.txt C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW4/hw3-files-2023/qrels/LA-only.trec8-401.450.minus416-423-437-444-447.txt
