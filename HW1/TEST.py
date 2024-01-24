# TEST

import gzip
import sys




#data_path = sys.argv[1]
data_path = "C:/Users/matth/OneDrive/Desktop/University/3B/MSCI541-Search-Engines/HW1/raw-data/latimes.gz"
#store_path = sys.argv[2]
#print(data_path)

count = 0
docno_list = []
doc = ""
date = ""
is_date = False
headline = ""
is_headline = False
#meta_data_list

f = gzip.open(data_path,'rt')





for count, line in enumerate(f):
    if count < 1000 : 
        print(line)