import os
import functions_framework

from flask import escape
from ses_mailer import send_email
from template_loader import env


@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    your_name = request_json.get("your_name")

    mail_to = os.getenv('MAIL_TO')
    template = env.get_template('mail.html')
    html = template.render(name=your_name)

    send_email(mail_subject="mail_subject",
               mail_body=html,
               mail_to=[mail_to],
               )

    return escape("email sent")
