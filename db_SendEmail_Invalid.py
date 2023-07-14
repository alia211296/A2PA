import smtplib
import ssl
import csv
import pandas as pd
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

file_input = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/input/input_file.csv"
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

f_facr = facr[0:6] + facr[7:11]
f_user  = username.upper()
db_id =  f_user + "_" + f_facr + "_" + str(adj) 

###################################################################################################
#Emailing System
################################################################################################### 
# setting
smtp_server = "smtpauth.intel.com"
port = 587 
#sender email need to change to generic email
sender_email = "a2pa@intel.com" 
password =  "" 
addr_to   = [email,'alia.nabila.ismail@intel.com']

html = """
<html><body><p>Hi {username} !</p>
<p>
        Lot(s) is not exists in database.<br>
        It may due to (1) Wrong lot number or (2) Incomplete OPN detail.<br>
		Please refer to attach wrong input submission. 
        You can either re-submit the request through <a href="www.a2pa.intel.com"> A2PA Website </a> or contact us.<br>
</p>


<p style="color:grey;font-size:10px""> 
        --System generated email. Please do not reply.<br>
        --This request was submitted on {datetime}.
</p>

</body></html>
"""

# with open('//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_pedb_reload.csv') as input_file:
#     reader = csv.reader(input_file)
#     data = list(reader)

html = html.format(username=username, opn=opn, facr=facr, ft_lot=ft_lot, adj=adj, datetime=datetime,db_id=db_id)

msg = MIMEMultipart()

body = MIMEText(html, 'html')
msg.attach(body)

csv = MIMEApplication(open(file_input, "rb").read())
csv.add_header('Content-Disposition', 'attachment', filename="input_file.csv")
msg.attach(csv)
    
msg['Subject'] = facr + " Fail - Invalid Lot Number/Incomplete OPN."
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