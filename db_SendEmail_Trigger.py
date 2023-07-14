import smtplib
import ssl
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

input_file = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/input/input_file.csv"
db_input = "//pggappchiawenc1.gar.corp.intel.com/C/A2PA/streamlit/database/db_input.csv"

df_input = pd.read_csv (input_file)
email = df_input.iloc[0]['email_address']
username = df_input.iloc[0]['username']
datetime = df_input.iloc[0]['datetime']

df = pd.read_csv(db_input)
facr = df.iloc[0]['facr_no']
opn = df.iloc[0]['opn']

###################################################################################################
#Emailing System
################################################################################################### 
# setting
smtp_server = "smtpauth.intel.com"
port = 587 

#sender & receiver
sender_email = "a2pa@intel.com" 
password =  "" 
addr_to   = ['alia.nabila.ismail@intel.com']

#email body
html = """

<p>

        OPN: {opn} <br>
        ID: {username} <br>
        DT: {datetime} <br>
        
</p>

</body></html>
"""

#email body setting
html = html.format(opn=opn, facr=facr, username=username, datetime=datetime)

msg = MIMEMultipart()
body = MIMEText(html, 'html')

msg.attach(body)   
msg['Subject'] = facr + " FACR Analysis Request"
msg['From'] = sender_email
msg['To'] = ", ".join(addr_to)

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
connection = smtplib.SMTP(smtp_server, port)
connection.ehlo()
connection.starttls(context=context)
connection.ehlo()
connection.login(sender_email, password)
connection.sendmail(sender_email, addr_to, msg.as_string())
connection.quit()