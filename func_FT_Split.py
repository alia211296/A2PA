import pandas as pd
import numpy as np

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_facr = db_path + "db_ft_facr_lot.csv"
file_object = db_path + "db_object.csv"
file_ft_unit = db_path + "FTUnitData.csv"
file_ft_date = db_path + "db_ft_adjacent_lot.csv"
file_ft_yield = db_path + "FTYieldPlot.csv"

output_lot = db_path + "FTYieldPlotSplit.csv"
output_unit = db_path + "FTUnitPassingICC.csv"
output_pat_limit = db_path + "FTPATLimit.csv"

df_input = pd.read_csv(file_object)
df_unit = pd.read_csv(file_ft_unit)
df_facr = pd.read_csv(file_facr)
df_ft_yield = pd.read_csv (file_ft_yield)

vendor_lot = df_facr.iloc[0]['lotop_vendor_lot']
altera_lot = df_facr.iloc[0]['altera_lot_name']
opn = df_input.iloc[0]['opn']
facr = df_input.iloc[0]['facr_no']
device = df_input.iloc[0]['device']
tfn = df_input.iloc[0]['test_flow_name']
wxy = altera_lot + "_" + df_input.iloc[0]['wxy']
test_step = 'FT'

facr_syl_yield = df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'ft_yield'].item()
syl_limit = df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'syl_limit'].item()

if facr_syl_yield > syl_limit: 
    print("split lot is not required")

else:

    #find manufacturing dtae to get limit
    date_ref = pd.read_csv (file_ft_date)
    ft_time = pd.to_datetime(date_ref.loc[(date_ref['altera_lot_name']==altera_lot)].latest_lot_op_completion_date, format='%Y-%m-%d %H:%M:%S').item()

    ###################################################################################################
    # Get SYL limit into syl_limit (label)
    ################################################################################################### 
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
    # Calculate FT Yield into FTYieldPlotSplit.csv
    ################################################################################################### 
    df_ft = df_unit[(df_unit['final_test_flag'] > 0)]
    col_set1 = ['device','altera_lot_name','lotop_vendor_lot','test_step','soft_bin_name','hard_bin_name','Pass_Flag']
    df1 = df_ft.reindex(columns=col_set1)

    df1['result_pass'] = np.where(df1['Pass_Flag'].isin([1]), 1, 0)
    df1['total_tested_unit'] = np.where(df1['device'] == device, 1, 0)
    df2 = df1.groupby(['lotop_vendor_lot']).sum().reset_index()
    df2['test_step'] = df1['test_step']
    df2['test_flow_name'] = tfn

    df_result_pass = df2.loc[: , "result_pass"]
    df_total_tested_unit = df2.loc[: , "total_tested_unit"]
    df2['ft_yield'] = round((df_result_pass/df_total_tested_unit)*100,2)
    df2["syl_limit"] = syl_limit
    
        
    col_name = ['lotop_vendor_lot','test_flow_name','result_pass','total_tested_unit','ft_yield','syl_limit','label']
    df3 = df2.reindex(columns=col_name)
    df3['label'] = df3['lotop_vendor_lot'].apply(lambda x : facr if x == vendor_lot else "ref").fillna(0, downcast='int64')
    
    col = ['altera_lot_name', 'lotop_vendor_lot']
    df_merge = pd.read_csv(file_ft_unit, skipinitialspace=True, usecols=col)
    df_merge1 = df_merge.drop_duplicates(subset='lotop_vendor_lot')
    final_output = pd.merge(df_merge1, 
                          df3, 
                          on ='lotop_vendor_lot', 
                          how ='left')

	
    df_ly_exclude = final_output[(final_output['ft_yield'] > final_output['syl_limit'].iloc[0] + 2)].dropna() 
    df_ly_exclude.to_csv(output_lot, index=False)
	
