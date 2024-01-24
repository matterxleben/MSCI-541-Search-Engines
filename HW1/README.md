# msci-541-f23-hw1-matterxleben

## MSCI 541 - Search Engines: Homework 1 - Problem 4

Name: Matthew Erxleben

ID: 20889980

### Installation Requirements:
1.	Please make sure Python is installed on your computer before running the program.
2.	Clone repository on your device by entering this into your terminal: git clone https://github.com/UWaterloo-MSCI-541/msci-541-f23-hw1-matterxleben.git

### Running the Programs
In order to run these programs, please navigate to where you cloned the repository and open the working directory .../msci-541-f23-hw1-matterxleben

#### IndexEngine: 
This program accepts two command line arguments:
1.	a path to the latimes.gz file
2.	a path to a directory where the documents and metadata will be stored.

For example, you would run IndexEngine from the command prompt / terminal / shell as:
python IndexEngine.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/raw-data/latimes.gz C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/store

#### GetDoc:
The program accepts three command line arguments: 
1.	a path to the location of the documents and metadata store created by the first program (IndexEngine)
2.	either the string "id" or the string "docno"
3.	either the internal integer id of a document or a DOCNO

For example, you would run GetDoc from the command prompt / terminal / shell as:
python GetDoc.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/store docno LA010189-0003
OR
python GetDoc.py C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/store id 2
