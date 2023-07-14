import pandas as pd

file = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_ft_facr_lot.csv"
df_ref = pd.read_csv (file)

#FACR is available, empty is equal to 1
if not df_ref.empty:
    df_ref.at[0,'empty'] = 1

#FACR is NOT available, empty is equal to 0
else:
    df_ref.at[0,'empty'] = 0


df_ref['empty'] = df_ref['empty'].astype('int64')
    
df_ref.to_csv(file, index=False)