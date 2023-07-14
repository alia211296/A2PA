#update database/db_qa_facr_lot.csv

import pandas as pd

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_qa = db_path + "db_qa_facr_lot.csv"
file_qa_re = db_path + "db_qa_retest_lot.csv"
file_ft = db_path + "db_ft_facr_lot.csv"

df_qa = pd.read_csv (file_qa)
df_qa_re = pd.read_csv (file_qa_re)
df_ft = pd.read_csv (file_ft)

qa_yield = df_qa['qa_yield'].item()

#Check QA Violation
if not qa_yield == 100 and df_qa_re.empty:
    
    df_qa['qa_yield_retest'] = round((df_qa_re['total_die_unit_passed']/df_qa_re['total_die_unit_tested'])*100,2)
    qa_yield_new = df_qa['qa_yield_retest'].iloc[0]
    
    if qa_yield_new == 100:
        df_qa.qa_violation = "No"
    else:
        df_qa.qa_violation = "N/A"
        
else:
    df_qa.qa_violation = "No"

df_qa.to_csv(file_qa, index=False)