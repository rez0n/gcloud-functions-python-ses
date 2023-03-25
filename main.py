import os

import functions_framework
import sentry_sdk
from flask import jsonify
from sentry_sdk.integrations.gcp import GcpIntegration

from ses_mailer import send_email
from template_loader import env

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', ''),
    integrations=[
        GcpIntegration(),
    ],
    traces_sample_rate=1.0
)


@functions_framework.http
def main(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    # Basic ping response
    if request.method == 'GET' or not request_json:
        response = jsonify({
            'success': True,
            'message': 'Service online',
        })
        return response

    # Processing POST request json data
    if request.method == 'POST' and request_json:
        your_name = request_json.get("your_name")
        if not your_name:
            return jsonify({
                'success': False,
                'message': 'Name should be supplied',
            })

        # Send email if name has been specified
        mail_to = os.getenv('MAIL_TO')
        template = env.get_template('mail.html')
        html = template.render(name=your_name)

        send_email(mail_subject="mail_subject",
                   mail_body=html,
                   mail_to=[mail_to],
                   )

        return jsonify({
            'success': True,
            'message': 'Message sent',
        })
