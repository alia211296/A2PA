#database/queue.csv

import os
import pandas as pd
  
# path of the directory
path = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/queue"
queue_csv = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/queue.csv"

# check the list of A2PA ANALYSIS REQUEST in queue folder
dir = os.listdir(path)

# check if the list is empty or not
if len(dir) == 0:
    frame = [0]
    df = pd.DataFrame(frame,columns = ['status'])
    df.to_csv(queue_csv,index=0)

else:
    frame = [1]
    df = pd.DataFrame(frame,columns = ['status'])
    df.to_csv(queue_csv,index=0)