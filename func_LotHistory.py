import pandas as pd
import glob, csv
from glob import glob
import plotly.graph_objects as go

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_facr = db_path + "db_object.csv"
file_facr2 = db_path + "db_ft_facr_lot.csv"
file_facr3 = db_path + "db_input.csv"
file_facr4 = db_path + "db_qa_facr_lot.csv"
file_yield = db_path + "FTYieldPlot.csv"

csv_output = db_path + "result_lot_history.csv"
fig_output = db_path + "result_lot_history.png"

df_facr = pd.read_csv (file_facr)
df_facr2 = pd.read_csv (file_facr2)
df_facr3 = pd.read_csv (file_facr3)
df_facr4 = pd.read_csv(file_facr4)
df_yield = pd.read_csv(file_yield)

facr = df_facr3.iloc[0]['facr_no']

facr_no = df_facr['facr_no'].tolist()
cust_unit = df_facr3['customer_unit'].fillna('N/A')
mpna = df_facr['mpna'].tolist()
opn = df_facr['opn'].tolist()
prod_lot = df_facr2['altera_lot_name'].tolist()
lot_comp_date= pd.to_datetime(df_facr2['latest_lot_op_completion_date']).dt.date
temp_grade = df_facr2['temperature_grade'].tolist()
facr_package = df_facr2['package_type'].tolist()
tp_rev = df_facr2['test_program_rev'].tolist()
syl_violation = df_facr2['syl_violation'].fillna('N/A')
qa_violation = df_facr4['qa_violation'].fillna('N/A')

s = df_facr3['ft_altera_lot_name'].iloc[0]

if s == 'N%':
  cust_lot = df_facr2['altera_lot_name'].tolist()
    
else:
  cust_lot = df_facr2['lotop_vendor_lot'].tolist()

facr_syl_yield = df_yield.loc[df_yield["label"].str.contains(facr,na=False),'ft_yield'].item()
syl_limit = df_yield.loc[df_yield["label"].str.contains(facr,na=False),'syl_limit'].item()


###################################################################################################
# SYL & RETEST Condition
###################################################################################################  

#FAIL limit + NO retest

if facr_syl_yield < syl_limit and df_facr2.at[0,'ft_retest'] == "No":

    file_yield_split = db_path + "FTYieldPlotSplit.csv"
    df_yield_split = pd.read_csv(file_yield_split)

    ft_yield = df_yield_split.loc[df_yield_split['label'].str.contains(facr, na=False), 'ft_yield'].tolist()
    ft_retest = df_facr2['ft_retest'].tolist()

    df = pd.DataFrame(list(zip(facr_no, cust_unit, mpna, opn, cust_lot, prod_lot, lot_comp_date, temp_grade, facr_package, tp_rev, ft_yield, ft_retest, syl_violation, qa_violation)),
    columns =['FACR NUMBER', 'CUSTOMER UNIT','MPNA','CUSTOMER OPN', 'CUSTOMER REPORTED LOT', 'PRODUCTION TEST LOT', 'LOT OPERATION DATE', 'TEMPERATURE GRADE', 'PACKAGE TYPE', 'TEST PROGRAM REVISION', 'FT LOT YIELD', 'FT RETEST','SYL VIOLATION', 'QAPR VIOLATION'])
    df.to_csv(csv_output, index = False)
    df_get = df.T
    df_get2 = df_get.reset_index().rename(columns = {"index": "LOT INFORMATION", 0:"LOT DATA"})
    df_get2.to_csv(csv_output, index = False)

#FAIL limit + YES retest
else: 
    if facr_syl_yield < syl_limit and df_facr2.at[0,'ft_retest'] == "Yes":
      file_yield_retest = db_path + "FTYieldPlotRetest.csv"
      df_yield_retest = pd.read_csv(file_yield_retest)

      ft_yield_retest = df_yield_retest.loc[df_yield_retest['label'].str.contains(facr,na=False), 'ft_yield'].tolist()
      ft_retest = df_facr2['ft_retest'].tolist()

      df = pd.DataFrame(list(zip(facr_no, cust_unit, mpna, opn, cust_lot, prod_lot, lot_comp_date, temp_grade, facr_package, tp_rev, ft_yield_retest, ft_retest, syl_violation, qa_violation)),
                columns =['FACR NUMBER', 'CUSTOMER UNIT','MPNA','CUSTOMER OPN', 'CUSTOMER REPORTED LOT', 'PRODUCTION TEST LOT', 'LOT OPERATION DATE', 'TEMPERATURE GRADE', 'PACKAGE TYPE', 'TEST PROGRAM REVISION','FT LOT YIELD', 'FT RETEST','SYL VIOLATION', 'QAPR VIOLATION'])
      df_get = df.T
      df_get2 = df_get.reset_index().rename(columns = {"index": "LOT INFORMATION", 0:"LOT DATA"})
      df_get2.to_csv(csv_output, index = False)
  
  #PASS limit + NO retest 
    else:

      ft_yield= df_yield.loc[df_yield['label'].str.contains(facr, na=False), 'ft_yield'].tolist()
      ft_retest = df_facr2['ft_retest'].tolist()

      df = pd.DataFrame(list(zip(facr_no, cust_unit, mpna, opn, cust_lot, prod_lot, lot_comp_date, temp_grade, facr_package, tp_rev, ft_yield, ft_retest, syl_violation, qa_violation)),
                columns =['FACR NUMBER', 'CUSTOMER UNIT','MPNA','CUSTOMER OPN', 'CUSTOMER REPORTED LOT', 'PRODUCTION TEST LOT', 'LOT OPERATION DATE', 'TEMPERATURE GRADE', 'PACKAGE TYPE', 'TEST PROGRAM REVISION','FT LOT YIELD', 'FT RETEST','SYL VIOLATION', 'QAPR VIOLATION'])
      df_get = df.T
      df_get2 = df_get.reset_index().rename(columns = {"index": "LOT INFORMATION", 0:"LOT DATA"})
      df_get2.to_csv(csv_output, index = False)

###################################################################################################
# Table Layout Configuration
###################################################################################################    

df_info = pd.read_csv(csv_output, na_filter= False)
lot_info = df_info['LOT INFORMATION']
lot_data = df_info['LOT DATA']

headerColor = '#86B0D9'
rowEvenColor = '#e6f2ff' 
rowOddColor = 'white'

fig = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>LOT INFORMATION</b>','<b>LOT DATA</b>'], line_color='darkslategray',
    fill_color=headerColor,
    align=['left','left'],
    font=dict(color='black', size=13)
  ),
  cells=dict(
    values=[lot_info, lot_data],
    line_color='darkslategray', fill_color=[[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor,rowEvenColor,rowOddColor, rowEvenColor]*8],
    align='left', font= dict(color = 'darkslategray', size = 13), height=25
  ))
])

fig.update_layout(width=600, height=600)  
# fig.show() 
fig.write_image(fig_output)