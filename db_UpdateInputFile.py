#database/db_input.csv

import pandas as pd
import csv

#paths
db_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/"
setting_path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/setting/"

#files
file_config = setting_path + "OPNRelationshipFile.csv"
file_input = db_path + "input/input_file.csv"
file_output = db_path + "db_input.csv"

df_input = pd.read_csv (file_input)
df_lookup = pd.read_csv (file_config)

opn = df_input.iloc[0]['opn']

#lookup
df_input['test_flow_name'] = df_lookup.loc[df_lookup['OPN'] == opn, 'Test Flow Name'].iloc[0]
df_input['mpna'] = df_lookup.loc[df_lookup['OPN'] == opn, 'MPNA'].iloc[0]
df_input['base_die'] = df_lookup.loc[df_lookup['OPN'] == opn, 'Base Die'].iloc[0]

cols = ['wafer', 'x', 'y']
df_input['wxy'] = df_input[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

#add_flag
y = df_input['opn'][0] in (None, "")

def altera(row):
    if y == 'False':
        val = 0
    else:
        val = 1
    return val

df_input['lot_ready']  = df_input.apply(altera, axis=1)

#sort_col
col = ['facr_no','customer_unit','wxy',
 'opn','mpna','test_flow_name','ft_altera_lot_name',
 'lotop_vendor_lot','base_die','range',
 'lot_ready']
df_new = df_input.reindex(columns=col)

df_new.to_csv (file_output, index=False)