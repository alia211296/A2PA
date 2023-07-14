import pandas as pd
import glob, csv
from glob import glob

db_path = '//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/'

file_ft_unit = db_path + "FTUnitData.csv"
file_ft = db_path + "db_ft_adjacent_lot.csv"

file_ws_die = db_path + "WSDieData.csv"
file_ws = db_path + "db_ws_adjacent_lot.csv"

input_file = db_path + "db_input.csv"
output_file = db_path + "db_pedb_reload.csv"

df_ft_unit = pd.read_csv (file_ft_unit)
df_ft = pd.read_csv (file_ft)
df_ws_die = pd.read_csv (file_ws_die)
df_ws = pd.read_csv (file_ws)

df_input = pd.read_csv (input_file)
df_table = pd.DataFrame()

ft_lot_extract = df_ft_unit["altera_lot_name"].drop_duplicates().tolist()
ft_lot_range = df_ft["altera_lot_name"].tolist()

ws_lot_extract = df_ws_die["altera_lot_name"].drop_duplicates().tolist()
ws_lot_range = df_ws["altera_lot_name"].tolist()

a = set(ft_lot_extract)
b = set(ft_lot_range)
c = set(ws_lot_extract)
d = set(ws_lot_range)

difference_ft = a.symmetric_difference(b)
list_difference_ft = list(difference_ft)

difference_ws = c.symmetric_difference(d)
list_difference_ws = list(difference_ws)

FT = ', '.join(list_difference_ft)
WS = ', '.join(list_difference_ws)

#match, then 1
if a==b and c==d :
    df_input["unit_ops"] = 1
else:
    df_input["unit_ops"] = 0
    df_table['Test Step'] = ['FT','WS']
    df_table['Impacted Lot List'] = [FT,WS]
    df_table.to_csv(output_file,index=False)

df_input.to_csv(input_file)