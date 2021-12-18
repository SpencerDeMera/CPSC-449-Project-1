import smtplib
import requests
import os
import socket
from dotenv import load_dotenv

def email_notify(username, id):
    email_text = None
    fromAddr = 'admin@fakeTwitter.com'
    load_dotenv()
    userPort = os.environ.get('userAPI')
    domainName = socket.gethostbyname(socket.getfqdn())

    url = "http://" + str(domainName) + ":" + str(userPort) + "/users/" + str(username) + "/getEmail"
    emailAddr = requests.get(url)

    if id[0] == "p":
        # send email saying poll <id> is invalid
        email_text = "We are sorry the poll at id: " + id + " is invalid please try again"
    else:
        # senbd email saying post <id> is invalid
        email_text = "We are sorry the post at id: " + id + " is invalid please try again"

    server = smtplib.SMTP(str(domainName))
    server.set_debuglevel(1)
    server.sendmail(fromAddr, emailAddr, email_text)
    server.quit()


