import pandas as pd
import numpy as np
import os

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

adj_ft = db_path + "db_ft_adjacent_lot.csv"
ft_plot = db_path + "FTYieldPlot.csv"

adj_ws = db_path + "db_ws_adjacent_lot.csv"
ws_plot = db_path + "WSYieldPlot.csv"


ft_split_plot = db_path + "FTYieldPlotSplit.csv"

df1 = pd.read_csv (adj_ft)
df2 = pd.read_csv (adj_ws)
df3 = pd.read_csv(ft_plot)
df4 = pd.read_csv(ws_plot)


df_merge1 = pd.merge(df3,df1[['altera_lot_name','latest_lot_op_completion_date']],on='altera_lot_name', how='right')
df_merge1.to_csv(ft_plot,index=False)

df_merge2 =pd.merge(df4,df2[['altera_lot_number','last_lot_oper_end_date']],on='altera_lot_number', how='right')
df_merge2.to_csv(ws_plot,index=False)

if os.path.exists (ft_split_plot):
    df5 = pd.read_csv(ft_split_plot)
    df_merge3 =pd.merge(df5,df1[['altera_lot_name','latest_lot_op_completion_date']],on='altera_lot_name', how='right')
    df_merge3.to_csv(ft_split_plot,index=False)
