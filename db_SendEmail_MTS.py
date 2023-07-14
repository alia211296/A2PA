import smtplib
import ssl
import csv, os
import pandas as pd
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

file_input = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/input/input_file.csv"
text_info = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/info_file.txt"
db_input = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_input.csv"


df_input = pd.read_csv (file_input)
email = df_input.iloc[0]['email_address']
username = df_input.iloc[0]['username']
datetime = df_input.iloc[0]['datetime']

df = pd.read_csv(db_input)
facr = df.iloc[0]['facr_no']
opn = df.iloc[0]['opn']
ft_lot = df.iloc[0]['ft_altera_lot_name']
adj = df.iloc[0]['range']

###################################################################################################
#Emailing System
################################################################################################### 
# setting
smtp_server = "smtpauth.intel.com"
port = 587 
#sender & receiver
sender_email = "a2pa@intel.com" 
password =  "" 
addr_to   = [email,'alia.nabila.ismail@intel.com']

if os.path.exists(text_info):
    os.remove(text_info) 

more_lines = ['OPN:'+opn,'FACR ID:'+facr,'FACR Lot Number:'+ft_lot,'Number of Adjacent Lot:'+str(adj)]
f = open(text_info, "x")

with open(text_info, 'w') as f:
    f.writelines('\n'.join(more_lines))
    f.close()

#email body
html = """
<html><body><p>Hi {username} !</p>

<p>
    Lot(s) is not exists in database. 
    It may be due to the lot is over 2 years data retention period. <br> 
    Click <a href="http://pgspsiweb002.gar.corp.intel.com/mts/#/ticket/495"> MTS ticket </a> to submit the lot table below. <br> 
</p>

{table}

<p style="color:grey;font-size:10px"">
    --System generated email. Please do not reply.<br>
    --This request was submitted on {datetime}.
</p>

</body></html>
"""

#email body setting
with open('//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_pedb_reload.csv') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"), username=username, opn=opn, facr=facr, ft_lot=ft_lot, adj=adj, datetime=datetime)

msg = MIMEMultipart()

body = MIMEText(html, 'html')
msg.attach(body)
    
text = MIMEApplication(open(text_info, "rb").read())
text.add_header('Content-Disposition', 'attachment', filename="info_file.txt")
msg.attach(text)

csv = MIMEApplication(open(file_input, "rb").read())
csv.add_header('Content-Disposition', 'attachment', filename="input_file.csv")
msg.attach(csv)

msg['Subject'] = facr + " Action Required - Submit MTS ticket to retrieve Die/Unit level data."
msg['From'] = sender_email
msg['To'] = ", ".join(addr_to)

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
connection = smtplib.SMTP(smtp_server, port)
connection.ehlo()
connection.starttls(context=context)
connection.ehlo()
connection.login(sender_email, password)
#connection.set_debuglevel(1)
connection.sendmail(sender_email, addr_to, msg.as_string())
connection.quit()
