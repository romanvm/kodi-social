"""
Email notification to a Social Media manager
"""
import os
import smtplib
from email.mime.text import MIMEText

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>A new article on kodi.tv: {title}</title>
</head>
<body>
    <p>A new article has been published on kodi.tv: <strong><a href="{link}" target="_blank">{title}</a></strong></p>
</body>
</html>"""


def notify(title: str, link: str) -> None:
    if os.getenv('NOTIFY_BY_EMAIL') != '1':
        return
    email_content = TEMPLATE.format(title=title, link=link)
    message = MIMEText(email_content, 'html', 'utf-8')
    message['Subject'] = f'[A new article on kodi.tv] {title}'
    message['From'] = os.getenv('EMAIL_FROM')
    recipient = os.getenv('EMAIL_TO')
    message['To'] = recipient
    message['X-Mailer'] = 'Kodi Social script'
    host = os.getenv('EMAIL_HOST')
    port = int(os.getenv('EMAIL_PORT'))
    user = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL(host, port) as smtp_server:
        smtp_server.login(user, password)
        smtp_server.sendmail(user, [recipient], message.as_string())
