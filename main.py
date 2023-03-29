import os

import functions_framework
import sentry_sdk
from flask import jsonify
from sentry_sdk.integrations.gcp import GcpIntegration

from simple_ses_mailer.mailers import SesEmailMessage
from jinja2 import Environment, select_autoescape, FileSystemLoader


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
        env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', ])
        )
        template = env.get_template('mail.html')
        html = template.render(name=your_name)

        msg = SesEmailMessage(
            subject='mail_subject',
            body_html=html,
            embedded_attachments_list=['templates/logo.png'],
            mail_to=os.getenv('MAIL_TO'),
        )
        msg.send()

        return jsonify({
            'success': True,
            'message': 'Message sent',
        })
