import os, shutil, glob
import pandas as pd
from pathlib import Path

file_input = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/input/input_file.csv"
df_input = pd.read_csv (file_input)


username = df_input.iloc[0]['username']
facr = df_input.iloc[0]['facr_no']
adj = df_input.iloc[0]['range']

f_facr = facr[0:6] + facr[7:11]
f_user  = username.upper()
new_name =  f_user + "_" + f_facr + "_" + str(adj) 

new_folder = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/id/" + new_name

if not os.path.exists(new_folder):
    os.mkdir(new_folder)

source_1 = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/input/input_file.csv"   
source_2 = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/result_lot_history.png"   

shutil.move(source_1, new_folder + "/input_file.csv")

if os.path.exists(source_2):
    shutil.move(source_2, new_folder + "/result_lot_history.png")

path = '//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/'
extension_csv = 'csv'
extension_txt = 'txt'
os.chdir(path)
result_csv = glob.glob('*.{}'.format(extension_csv))
result_txt = glob.glob('*.{}'.format(extension_txt))


for file_name_csv in result_csv:
    shutil.move(os.path.join(path, file_name_csv), os.path.join(new_folder, file_name_csv))

for file_name_txt in result_txt:
    shutil.move(os.path.join(path, file_name_txt), os.path.join(new_folder, file_name_txt))
