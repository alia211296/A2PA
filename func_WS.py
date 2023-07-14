import pandas as pd
import numpy as np

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_facr = db_path + "db_ft_facr_lot.csv"
file_object = db_path + "db_object.csv"
file_ws_die = db_path + "WSDieData.csv"
file_ws_date = db_path + "db_ws_adjacent_lot.csv"

output_yield = db_path + "WSYieldSummary.csv"
output_label = db_path + "WSYieldPlot.csv"

df_input = pd.read_csv (file_object)
df_die = pd.read_csv (file_ws_die)
df_facr = pd.read_csv(file_facr)

base_die = df_input.iloc[0]['base_die']
altera_lot = df_facr.iloc[0]['altera_lot_name'][3:9]
altera_lot_name_ws = df_facr.iloc[0]['altera_lot_name'][0:9]
facr = df_input.iloc[0]['facr_no']
test_step = 'WS'

###################################################################################################
# Get SYL limit into syl_limit (label)
###################################################################################################
date_ref = pd.read_csv (file_ws_date)
ws_time = pd.to_datetime(date_ref.loc[(date_ref['altera_lot_name']==altera_lot_name_ws)].last_lot_oper_end_date, format='%Y-%m-%d %H:%M:%S').item()

directory_syl =  "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/setting/SYLLimit.xlsx"
df_ex = pd.read_excel(directory_syl,sheet_name=test_step) 
df_convert = df_ex.T 
df_convert.columns = df_ex.T.iloc[0]
df_convert = df_convert[1:]
df_convert = df_convert.reset_index().rename(columns = {"index": "date"})
df_convert["date"] = pd.to_datetime(df_convert["date"]).dt.date
target_date = df_convert[df_convert["date"] <= ws_time]["date"].max()
syl_limit = df_convert[df_convert["date"] == target_date][base_die].item()

###################################################################################################
# Calculate WS Yield into WSYieldPlot.csv
################################################################################################### 
df_ws = df_die[(df_die['final_test_flag'] > 0)]
col_set1 = ['device','altera_lot_number','test_step','sb_bin_name','hb_bin_name']
df1 = df_ws.reindex(columns=col_set1)
df1['result_pass'] = np.where(df1['hb_bin_name'] == 'PERFECT', 1, 0)
df1['total_tested_unit'] = np.where(df1['device'] == base_die, 1, 0)
df2 = df1.groupby(['altera_lot_number']).sum().reset_index()
df2['test_step'] = df1['test_step']

df_result_pass = df2.loc[: , "result_pass"]
df_total_tested_unit = df2.loc[: , "total_tested_unit"]
df2['ws_yield'] = round((df_result_pass/df_total_tested_unit)*100,2)
df2["syl_limit"] = syl_limit
col_name = ['altera_lot_number','test_step','result_pass','total_tested_unit','ws_yield','syl_limit','label']
df3 = df2.reindex(columns=col_name)


df3['altera_lot_number'].str.contains(altera_lot)
df3['label'] = df3['altera_lot_number'].str.contains(altera_lot).fillna(0, downcast='int64')

df3.loc[df3['altera_lot_number'].str.contains(altera_lot), 'label'] = facr
df3.loc[~df3['altera_lot_number'].str.contains(altera_lot), 'label'] = 'ref'

df3.to_csv (output_label, index = False)