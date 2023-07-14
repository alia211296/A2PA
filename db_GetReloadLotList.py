#database/db_pedb_reload.csv

import pandas as pd


db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_qa_retest = db_path + "db_qa_retest_lot.csv"
file_ft_retest = db_path + "db_ft_retest_lot.csv"
file_ft = db_path + "db_ft_adjacent_lot.csv"
file_ws = db_path + "db_ws_adjacent_lot.csv"
file_qa = db_path + "db_qa_facr_lot.csv"
file_output = db_path + "db_pedb_reload.csv"

df_qa_retest = pd.read_csv (file_qa_retest)
df_ft_retest = pd.read_csv (file_ft_retest)
df_ft = pd.read_csv (file_ft)
df_ws = pd.read_csv (file_ws)
df_qa = pd.read_csv (file_qa)


df_ft_retest_lot = df_ft_retest["altera_lot_name"].tolist()
df_ft_lot = df_ft["altera_lot_name"].tolist()
df_ws_lot = df_ws["altera_lot_name"].tolist()
df_qa_lot = df_qa["altera_lot_name"].tolist()

FT = ', '.join(map(str,df_ft_lot+df_ft_retest_lot))
WS = ', '.join(map(str,df_ws_lot))

if not df_qa_retest.empty:
    df_qa_retest_lot = df_qa["qa_retest_lot"].tolist()
    QA = ', '.join(map(str,df_qa_lot+df_qa_retest_lot))
else:
    QA = ', '.join(map(str,df_qa_lot))

df_table = pd.DataFrame()
df_table['Test Step'] = ['FT','WS','QA']
df_table['Impacted Lot List'] = [FT,WS,QA]

df_table.to_csv(file_output,index=False)