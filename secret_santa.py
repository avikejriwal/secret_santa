import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import numpy as np
from sklearn.utils import shuffle

port = 465  # For SSL
password = '1234567890'  # see here: https://support.google.com/mail/answer/185833?hl=en
sender_email = 'test_email@email.com'  # input real email here
context = ssl.create_default_context()
subject = "Secret Santa Assignment"

data = pd.read_csv('file.csv', header=0)
data = shuffle(data)
data['assignee email'] = np.roll(data['Email'], 1)

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)

    for _, row in data.iterrows():
        message = MIMEMultipart()
        message['From'] = sender_email
        receiver_email = row['assignee email']
        message['Subject'] = subject
        message_text = f"""\
        Your Secret Santa Assignment is: {row['Name']}

        Their mailing address is: {row['Mailing Address']}
        """

        blurb = row['Personality/Hobby blurbs']
        if blurb != '' and blurb == blurb:
            message_text += '\n\nExtra stuff about them:' + blurb

        message.attach(MIMEText(message_text, 'plain'))

        server.sendmail(sender_email, receiver_email, message.as_string())
