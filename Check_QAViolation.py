#database/ddb_qa_facr_lot.csv

import pandas as pd

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_qa = db_path + "db_qa_facr_lot.csv"
file_ft = db_path + "db_ft_facr_lot.csv"

df_qa = pd.read_csv (file_qa)
df_ft = pd.read_csv (file_ft)

altera_lot =  df_ft.iloc[0]['altera_lot_name'][1:9]
last_digit =  df_ft.iloc[0]['altera_lot_name'][9:]

#Possible QA Retest Lot 
# n = int(last_digit)+1
qa_retest_lot = 'W' + altera_lot + "%%"

df_qa['qa_yield'] = round((df_qa['total_die_unit_passed']/df_qa['total_die_unit_tested'])*100,2)
qa_yield = df_qa['qa_yield'].iloc[0]

##Check QA Violation for original QA Yield
if qa_yield == 100:
    df_qa['qa_violation'] = "No"
    df_qa.to_csv(file_qa, index=False)
else:
    df_qa['qa_violation'] = "N/A"
    df_qa['qa_retest_lot'] = qa_retest_lot
    df_qa.to_csv(file_qa, index=False)