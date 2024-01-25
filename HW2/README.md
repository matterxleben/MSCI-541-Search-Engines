# msci-541-f23-hw2-matterxleben

## MSCI 541 - Search Engines: Homework 2

Name: Matthew Erxleben

ID: 20889980

### Installation Requirements:
1.	Please make sure Python is installed on your computer before running the program.
2.	Clone repository on your device by entering this into your terminal: git clone https://github.com/UWaterloo-MSCI-541/msci-541-f23-hw2-matterxleben.git

### Running the Programs
In order to run these programs, please navigate to where you cloned the repository and open the working directory .../msci-541-f23-hw2-matterxleben

#### IndexEngine: 
This program accepts two command line arguments:
1.	a path to the latimes.gz file
2.	a path to a directory where the documents, metadata, and term files will be stored.

For example, you would run IndexEngine from the command prompt / terminal / shell as:
python IndexEngine.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/raw-data/latimes.gz C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store

#### GetDoc:
The program accepts three command line arguments: 
1.	a path to the location of the documents and metadata store created by the first program (IndexEngine)
2.	either the string "id" or the string "docno"
3.	either the internal integer id of a document or a DOCNO

For example, you would run GetDoc from the command prompt / terminal / shell as:
python GetDoc.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store docno LA010189-0003
OR
python GetDoc.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store id 2

#### BooleanAND:

The program accepts three command line arguments: the directory location of your index, the queries file, and the name of a file to store your output
    1. a path to the location of your index, created by IndexEngine
    2. the queries file
    3. the name of a file to store your output

For example, you would run BooleanAND from the command prompt / terminal / shell as:
    python BooleanAND.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/store/term_files queries.txt test-results.txt

For this program, the queries file (search topics file) is in the /topics files folder. In the code for the program, the path is hardcoded as:
C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW2/msci-541-f23-hw2-matterxleben/topics files/" + queries_file

Please change this to your own computers path to the msci-541-f23-hw2-matterxleben/topics files/ folder to obtain the queries (search topics) !
