#database/input/input_file.csv

import glob, os

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

#folder
folder_queue = db_path + "queue"
folder_input = db_path + "input"

#files
file_input = folder_input + "/input_file.csv"

if not os.listdir(folder_input):
    print ("Get the oldest request into input folder")
    
    list_of_files = glob.glob(folder_queue + "/*") # * means all if need specific format then *.csv
    oldest_file = min(list_of_files, key=os.path.getctime)
    os.rename(oldest_file, file_input)
    
else:
    print ("Input file is already exits")
    