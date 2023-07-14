#database/db_ws_adjacent_lot.csv

import pandas as pd

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_facr_lot = db_path + "db_ft_facr_lot.csv"
file_object = db_path + "db_object.csv"
file_ws_lots = db_path + "db_ws_adjacent_lots.csv"
file_output = db_path + "db_ws_adjacent_lot.csv"

df_facr_lot = pd.read_csv (file_facr_lot)
df_object = pd.read_csv (file_object)
df_lots = pd.read_csv (file_ws_lots)
df_new = df_lots.sort_values(by='last_lot_oper_end_date', ascending=True)
df_new.to_csv (file_ws_lots,index=False)

df_wlots = pd.read_csv (file_ws_lots)

altera_lot = df_facr_lot.iloc[0]['altera_lot_name']
row = df_object.iloc[0]['range'] / 2
row_round = round(row)

altera_lot = df_facr_lot.iloc[0]['altera_lot_name']
ws_altera_lot_name = altera_lot[0:9]
row = df_object.iloc[0]['range'] / 2
row_round = round(row)

if ws_altera_lot_name in df_wlots.values:
    
    #before FACR Lot
    df1 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-row_round:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-1]
    #after FACR Lot
    df2 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]+1:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]+row_round]    
    #FACR Lot
    df3 = df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name]   
    
    row_round_df1 = len(df1.index)
    row_round_df2 = len(df2.index)
    total_get = row_round_df1 + row_round_df2
    add = df_object.iloc[0]['range'] - total_get
    x_df1 = row_round_df1 + add
    y_df2 = row_round_df2 + add

    if (row_round_df1 == row_round) and (row_round_df2 == row_round):
        df1 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-row_round:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-1]
        df2 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name ].index[0]+1:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]+row_round]
    
    if (row_round_df1 == row_round) and (row_round_df2 != row_round):
        df1 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-x_df1:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-1]
        df2 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name ].index[0]+1:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]+row_round]

    if (row_round_df1 != row_round) and (row_round_df2 == row_round):
        df1 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-row_round:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]-1]
        df2 = df_wlots.loc[df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name ].index[0]+1:df_wlots[df_wlots['altera_lot_name'] == ws_altera_lot_name].index[0]+y_df2]

    frames = [df1,df2,df3]
    result = pd.concat(frames, ignore_index=True)
    result.to_csv (file_output,index=False)

else:
    print("Lot is not exists")
