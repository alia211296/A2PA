import pandas as pd
import glob, csv
from glob import glob

file_ft_retest = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_ft_retest_lot.csv"
file_ft = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_ft_facr_lot.csv"
file_ft_yield = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/FTYieldPlot.csv"
file_object = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_object.csv"

output_lot_retest =  "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/FTYieldPlotRetest.csv"

df_ft = pd.read_csv (file_ft)
df_ft_retest = pd.read_csv (file_ft_retest)
df_ft_yield = pd.read_csv (file_ft_yield)
df_input = pd.read_csv (file_object)

facr = df_input.iloc[0]['facr_no']


#Get SYL and SYL Limit
facr_syl_yield = df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'ft_yield'].item()
syl_limit = df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'syl_limit'].item()

#Check SYL Violation for original FT Yield
if facr_syl_yield > syl_limit:
    df_ft['syl_violation'] = "No"
	
#Check SYL Violation for retest FT Yield    
else:

    if df_ft_retest.at[0,'empty'] == 0: 
        retest_passed_unit = df_ft_retest['total_die_unit_passed'].iloc[0]
        retest_unit = df_ft_retest['total_die_unit_tested'].iloc[0]
        total_tested_unit = df_ft_yield.loc[df_ft_yield ['label'].str.contains(facr), 'total_tested_unit'].item()
        total_passed_unit = df_ft_yield.loc[df_ft_yield ['label'].str.contains(facr), 'result_pass'].item()
        ft_yield = df_ft_yield.loc[df_ft_yield ['label'].str.contains(facr), 'ft_yield'].item()

        reject_unit = total_tested_unit - total_passed_unit
        total_recovered_unit = total_passed_unit + retest_passed_unit
        ft_yield_retest = round((total_recovered_unit/total_tested_unit)*100,2)
        retest_lot = df_ft_retest['altera_lot_name'].iloc[0]
        
        df_ft['ft_yield'] = ft_yield
        df_ft['ft_yield_retest'] = ft_yield_retest
        
        if ft_yield_retest > syl_limit:
            df_ft['syl_violation'] = "No"
        else:
            df_ft['syl_violation'] = 1

    else: 
        df_ft['syl_violation'] = 1

df_ft.to_csv(file_ft, index=False)

#FT RETEST/RECLAIM & FTYieldFTPlot

if df_ft_retest.at[0,'empty'] == 1:
    df_ft["ft_retest"] = 'No'
  
else:
    df_ft["ft_retest"] = 'Yes'
    df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'altera_lot_name'] = retest_lot
    df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'result_pass'] = total_recovered_unit
    df_ft_yield.loc[df_ft_yield["label"].str.contains(facr),'ft_yield'] = ft_yield_retest
    df_ft_yield.to_csv(output_lot_retest, index=False)

df_ft.to_csv(file_ft, index=False)
