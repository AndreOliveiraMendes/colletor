import smtplib
import urllib.parse
import urllib.request
from email.mime.text import MIMEText

from config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN


def send_mail(to, subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "seu@email.com"
    msg["To"] = to

    with smtplib.SMTP("localhost") as server:
        server.send_message(msg)

def send_telegram(msg):
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    }).encode()

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    req = urllib.request.Request(url, data=data)
    urllib.request.urlopen(req)