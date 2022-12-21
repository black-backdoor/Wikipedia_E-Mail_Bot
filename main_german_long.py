import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reqs = requests.get("https://de.wikipedia.org/wiki/Wikipedia:Hauptseite")
soup = BeautifulSoup(reqs.text, 'html.parser')
temp = str(soup)

daily, old = temp.split('<div id="unten">')
old, daily = daily.split('<div id="spalten">', 1)

daily = daily.replace("//upload.wikimedia.org/", "https://upload.wikimedia.org/")
daily = daily.replace("/wiki/", "https://de.wikipedia.org/wiki/")

daily_html = """<!DOCTYPE html><html dir="ltr" lang="en-GB"><head></head><body>""" + daily + "</body>"
#myFile = open("website.html", "w+", encoding='utf8')
#myFile.write(daily_html)
#myFile.close()

e_mail_login = []
with open("saves/email_login.txt") as file:
    for line in file:
        line = line.rstrip("\n")
        e_mail_login.append(line)

receiver_emails = []
with open("saves/receiver_long_emails.txt") as file:
    for line in file:
        line = line.rstrip("\n")
        receiver_emails.append(line)


receiver_email = receiver_emails

server_address = e_mail_login[0]
server_port = e_mail_login[1]
user_email = e_mail_login[2]
password = e_mail_login[3]

with smtplib.SMTP_SSL(server_address, server_port) as server:
    server.login(user_email, password)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Wikipedia"
    message["From"] = user_email
    msg = MIMEText(daily_html, "html")
    message.attach(msg)
    for i in range(0, len(receiver_emails)):
        message["To"] = receiver_emails[i]
        server.sendmail(user_email, receiver_emails[i], msg.as_string())
        print(f"e-mail sendt to: {receiver_emails[i]}")