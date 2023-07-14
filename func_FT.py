import pandas as pd
import numpy as np

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_facr = db_path + "db_ft_facr_lot.csv"
file_object = db_path + "db_object.csv"
file_ft_unit = db_path + "FTUnitData.csv"
file_ft_date = db_path + "db_ft_adjacent_lot.csv"

output_lot = db_path + "FTYieldPlot.csv"
output_unit = db_path + "FTUnitPassingICC.csv"
output_pat_limit = db_path + "FTPATLimit.csv"

df_input = pd.read_csv (file_object)
df_unit = pd.read_csv (file_ft_unit)
df_facr = pd.read_csv(file_facr)

altera_lot = df_facr.iloc[0]['altera_lot_name']
opn = df_input.iloc[0]['opn']
facr = df_input.iloc[0]['facr_no']
device = df_input.iloc[0]['device']
tfn = df_input.iloc[0]['test_flow_name']
wxy = altera_lot + "_" + df_input.iloc[0]['wxy']
test_step = 'FT'

###################################################################################################
# Get SYL limit into syl_limit (label)
################################################################################################### 
date_ref = pd.read_csv (file_ft_date)
ft_time = pd.to_datetime(date_ref.loc[(date_ref['altera_lot_name']==altera_lot)].latest_lot_op_completion_date, format='%Y-%m-%d %H:%M:%S').item()

directory_syl =  "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/setting/SYLLimit.xlsx"
df_syl = pd.read_excel(directory_syl,sheet_name=test_step) 
df_get_syl = df_syl.T 
df_get_syl.columns = df_syl.T.iloc[0]
df_get_syl = df_get_syl[1:]
df_get_syl = df_get_syl.reset_index().rename(columns = {"index": "date"})
df_get_syl["date"] = pd.to_datetime(df_get_syl["date"]).dt.date
target_date_syl = df_get_syl[df_get_syl["date"] <= ft_time]["date"].max()
syl_limit = df_get_syl[df_get_syl["date"] == target_date_syl][opn].item()

###################################################################################################
# Get PAT limit into FTPATLimit.csv
################################################################################################### 
directory_pat =  "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/setting/PATLimit.xlsx"
df_pat = pd.read_excel(directory_pat, sheet_name = opn)
df_get_pat = df_pat.T
df_get_pat.columns = df_pat.T.iloc[0]
df_get_pat = df_get_pat[1:]
df_get_pat = df_get_pat.reset_index().rename(columns = {"index": "date"})
df_get_pat["date"] = pd.to_datetime(df_get_pat["date"]).dt.date

target_date_pat = df_get_pat[df_get_pat["date"] <= ft_time]["date"].max()
pat_limit = df_get_pat[df_get_pat["date"] == target_date_pat]

df_pat_limit = pat_limit.T
df_pat_limit.drop(index=df_pat_limit.index[0], axis=0,inplace=True)
output_limit = df_pat_limit.rename(columns={df_pat_limit.columns[0]: "pat_limit", "index":"parameter"})
output_limit.to_csv (output_pat_limit)

###################################################################################################
# Get list of parameter name into col_param_name (label)
################################################################################################### 
df_param = pd.read_csv(output_pat_limit) 
col_param_name = df_param['parameter'].tolist()

#list down the list of sheet name # xl = pd.ExcelFile(directory_pat) # xl.sheet_names

###################################################################################################
# Calculate FT Yield into FTYieldPlot.csv
################################################################################################### 
df_ft = df_unit[(df_unit['final_test_flag'] > 0)]
col_set1 = ['device','altera_lot_name','test_step','soft_bin_name','hard_bin_name']
df1 = df_ft.reindex(columns=col_set1)

df1['result_pass'] = np.where(df1['soft_bin_name'].isin(['Passing', 'PASSING']), 1, 0)
df1['total_tested_unit'] = np.where(df1['device'] == device, 1, 0)
df2 = df1.groupby(['altera_lot_name']).sum().reset_index()
df2['test_step'] = df1['test_step']
df2['test_flow_name'] = tfn

df_result_pass = df2.loc[: , "result_pass"]
df_total_tested_unit = df2.loc[: , "total_tested_unit"]
df2['ft_yield'] = round((df_result_pass/df_total_tested_unit)*100,2)
df2["syl_limit"] = syl_limit

col_name = ['altera_lot_name','test_step','test_flow_name','result_pass','total_tested_unit','ft_yield','syl_limit','label']
df3 = df2.reindex(columns=col_name)
df3['altera_lot_name'].str.contains(altera_lot)
df3['label'] = df3['altera_lot_name'].str.contains(altera_lot).fillna(0, downcast='int64')
df3.loc[df3['altera_lot_name'].str.contains(altera_lot), 'label'] = facr
df3.loc[~df3['altera_lot_name'].str.contains(altera_lot), 'label'] = 'ref'

df3.to_csv (output_lot, index = False)

###################################################################################################
# Label WXY in Unit File into FTUnitPassingICC.csv
################################################################################################### 
col_lot_info = ['device',
 'altera_lot_name',
 'altera_lot_number',
 'lotop_vendor_lot',
 'test_step',
 'wafer_number',
 'die_x_pos',
 'die_y_pos']

new_col = col_lot_info + col_param_name

#facr, adjacent unit to label 
df4 = df_unit[(df_unit['final_test_flag'] > 0) & (df_unit['soft_bin_name'] == 'PASSING') | (df_unit['soft_bin_name'] == 'Passing')]
df5 = df4.reindex(columns=new_col)
df7 = df5.fillna(0)

df7["lot_w_x_y"] = df7['altera_lot_name'].astype(str) + '_' + df7['wafer_number'].astype(int).astype(str) + '_' + df7['die_x_pos'].astype(int).astype(str) + '_' + df7['die_y_pos'].astype(int).astype(str)

df7['label_lot'] = df7['altera_lot_name'].str.contains(altera_lot).fillna(0, downcast='int64')
df7.loc[df7['altera_lot_name'].str.contains(altera_lot), 'label_lot'] = facr
df7.loc[~df7['altera_lot_name'].str.contains(altera_lot), 'label_lot'] = 'ref'

df7['label_unit'] = df7['lot_w_x_y'].str.contains(wxy).fillna(0, downcast='int64')
df7.loc[df7['lot_w_x_y'].str.contains(wxy), 'label_unit'] = facr
df7.loc[~df7['lot_w_x_y'].str.contains(wxy), 'label_unit'] = 'ref'

df7.to_csv(output_unit,index=False)
