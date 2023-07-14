#database/db_object.csv

import pandas as pd


db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"

file_facr_lot = db_path + "db_ft_facr_lot.csv"
file_input = db_path + "db_input.csv"
file_object = db_path + "db_object.csv"

df_facr_lot = pd.read_csv (file_facr_lot)
df_input = pd.read_csv (file_input)

z = df_facr_lot['altera_lot_name'].iloc[0]
y = df_facr_lot['lotop_vendor_lot'].iloc[0]
k = df_facr_lot['device'].iloc[0]

s = df_input['ft_altera_lot_name'].iloc[0]

#if user input ft_altera_lot_name = N/A, then update altera_lot_name, else update lotop_vendor_lot under db_input.csv
if s == '%%':
    df_input.ft_altera_lot_name = z
    
else:
    df_input.lotop_vendor_lot = y

#add device column 
df_input['device']  = k

import re
length = len(re.sub("[^a-zA-Z]", "", z))

if length <= 5:
#for altera lot number with 5 letter, for examnple: 'NADAU62947'
    
    numft_6 = z[3:6]

    symbol = "%"
    group = symbol + numft_6 + symbol
    df_input['ft_object'] = group 
    df_input['ws_object'] = group

    df_input.to_csv (file_object, index=False)

    ##add ft retest into facr lot
    altera_lot =  df_facr_lot.iloc[0]['altera_lot_name'][1:9]
    last_digit =  df_facr_lot.iloc[0]['altera_lot_name'][9:]

    n = int(last_digit)+1
    ft_retest_lot = 'W' + altera_lot + str(n)
    df_facr_lot['ft_retest_lot'] = ft_retest_lot
    df_facr_lot.to_csv (file_facr_lot, index=False)

  
else: 
#for altera lot number with 6 letter, for examnple: 'NADAU6294X7'

    numft_5 = z[3:5]

    symbol = "%"
    group = symbol + numft_5 + symbol
    df_input['ft_object'] = group 
    df_input['ws_object'] = group

    df_input.to_csv (file_object, index=False)

    ##add ft retest into facr lot
    altera_lot =  df_facr_lot.iloc[0]['altera_lot_name'][1:10]
    last_digit =  df_facr_lot.iloc[0]['altera_lot_name'][10:]

    n = int(last_digit)+1
    ft_retest_lot = 'W' + altera_lot + str(n)
    df_facr_lot['ft_retest_lot'] = ft_retest_lot
    df_facr_lot.to_csv (file_facr_lot, index=False)

    