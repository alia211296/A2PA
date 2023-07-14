import pandas as pd
import glob, csv
from glob import glob

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_ft_retest = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_ft_retest_lot.csv"
file_ft = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_ft_facr_lot.csv"
file_object = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_object.csv"
file_facr = db_path + "db_ft_facr_lot.csv"


df_facr = pd.read_csv(file_facr)
df_ft = pd.read_csv (file_ft)
df_ft_retest = pd.read_csv (file_ft_retest)
df_input = pd.read_csv (file_object)
    
    
# vendor_lot = df_facr.iloc[0]['lotop_vendor_lot']
# facr = df_input.iloc[0]['facr_no']

# y = vendor_lot.item()
# x = isinstance(y, int)

file_ft_yield = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/FTYieldPlot.csv"
output_lot_retest =  "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/FTYieldPlotRetest.csv"

   
df_ft_yield = pd.read_csv (file_ft_yield)

facr = df_input.iloc[0]['facr_no']


#Get SYL and SYL Limit
facr_syl_yield = df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'ft_yield'].item()
syl_limit = df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'syl_limit'].item()

#Check SYL Violation for original FT Yield

if facr_syl_yield > syl_limit: 
    print("split lot is not required")
    df_ft['syl_violation'] = "No"

#Check SYL Violation for retest FT Yield    
else:
    file_ft_yield_split = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/FTYieldPlotSplit.csv"
    df_ft_yield_split = pd.read_csv (file_ft_yield_split)

    total_tested_unit = df_ft_yield_split.loc[df_ft_yield_split ['label'].str.contains(facr), 'total_tested_unit'].item()
    total_passed_unit = df_ft_yield_split.loc[df_ft_yield_split ['label'].str.contains(facr), 'result_pass'].item()
    ft_yield = df_ft_yield_split.loc[df_ft_yield_split ['label'].str.contains(facr), 'ft_yield'].item()
    df_ft['syl_violation'] = "N/A"

df_ft.to_csv(file_ft, index=False)


if df_ft_retest.at[0,'empty'] == 0:
    df_ft["ft_retest"] = 'No'

else: 
    df_ft["ft_retest"] = 'Yes'

df_ft.to_csv(file_ft, index=False)
