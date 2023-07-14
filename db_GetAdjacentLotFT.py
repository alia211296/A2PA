#database/db_ft_adjacent_lot.csv

import pandas as pd

db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_facr_lot = db_path + "db_ft_facr_lot.csv"
file_object = db_path + "db_object.csv"
file_ft_lots = db_path + "db_ft_adjacent_lots.csv"
file_output = db_path + "db_ft_adjacent_lot.csv"

df_facr_lot = pd.read_csv (file_facr_lot)
df_object = pd.read_csv (file_object)
df_lots = pd.read_csv (file_ft_lots)

altera_lot = df_facr_lot.iloc[0]['altera_lot_name']
row = df_object.iloc[0]['range'] / 2
row_round = round(row)

#filer only N lots
lot_prefix ="N"
filter_lot = df_lots["altera_lot_name"].str.startswith(lot_prefix, na = False) 
df = df_lots[filter_lot]
df_sort = df.sort_values(by='latest_lot_op_completion_date', ascending=True)
df_sort.to_csv (file_ft_lots,index=False)

df_flots = pd.read_csv (file_ft_lots)

if altera_lot in df_flots.values:
    
    #before FACR Lot
    df1 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-row_round:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-1]
    #after FACR Lot
    df2 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]+1:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]+row_round]    
    #FACR Lot
    df3 = df_flots[df_flots['altera_lot_name'] == altera_lot]   
    
    row_round_df1 = len(df1.index)
    row_round_df2 = len(df2.index)
    total_get = row_round_df1 + row_round_df2
    add = df_object.iloc[0]['range'] - total_get
    x_df1 = row_round_df1 + add
    y_df2 = row_round_df2 + add


    if (row_round_df1 == row_round) and (row_round_df2 == row_round):
        df1 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-row_round:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-1]
        df2 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot ].index[0]+1:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]+row_round]
    
    if (row_round_df1 == row_round) and (row_round_df2 != row_round):
        df1 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-x_df1:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-1]
        df2 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot ].index[0]+1:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]+row_round]

    if (row_round_df1 != row_round) and (row_round_df2 == row_round):
        df1 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-row_round:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]-1]
        df2 = df_flots.loc[df_flots[df_flots['altera_lot_name'] == altera_lot ].index[0]+1:df_flots[df_flots['altera_lot_name'] == altera_lot].index[0]+y_df2]

    frames = [df1,df2,df3]
    result = pd.concat(frames, ignore_index=True)
    result.to_csv (file_output,index=False)

else:
    print("Lot is not exists")
