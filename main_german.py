import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reqs = requests.get("https://de.wikipedia.org/wiki/Wikipedia:Hauptseite")
soup = BeautifulSoup(reqs.text, 'html.parser')
temp = str(soup)

old , daily = temp.split('<div class="hauptseite-box" id="artikel">', 1)
daily, old = daily.split('<div id="rechts">', 1)

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
with open("saves/receiver_emails.txt") as file:
    for line in file:
        line = line.rstrip("\n")
        receiver_emails.append(line)

#creat e-mail
sender_email = e_mail_login[0]
receiver_email = receiver_emails
password = e_mail_login[1]

with smtplib.SMTP_SSL("server.de", 465) as server:
    server.login(sender_email, password)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Wikipedia"
    message["From"] = sender_email
    msg = MIMEText(daily_html, "html")
    message.attach(msg)
    for i in range(0, len(receiver_emails)):
        message["To"] = receiver_emails[i]
        server.sendmail(sender_email, receiver_emails[i], msg.as_string())
        print(f"e-mail sendt to: {receiver_emails[i]}")