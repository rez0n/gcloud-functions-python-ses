import os
from email.mime.image import MIMEImage

import boto3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(mail_subject, mail_body, mail_to):
    mail_to_str = ','.join(mail_to)

    mail_from = os.getenv('MAIL_FROM')

    msg = MIMEMultipart()
    msg["Subject"] = mail_subject
    msg["From"] = mail_from
    msg["To"] = mail_to_str

    # Set message body
    body = MIMEText(mail_body, 'html')
    msg.attach(body)

    filename = "templates/logo.png"
    with open(filename, "rb") as attachment:
        part = MIMEImage(attachment.read())
        part.add_header('Content-ID', '<logo.png>')
    msg.attach(part)

    ses_client = boto3.client(
        "ses",
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_SES_REGION'),
    )

    response = ses_client.send_raw_email(
        Source=mail_from,
        Destinations=mail_to,
        RawMessage={"Data": msg.as_string()}
    )
