import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailClient:
    
    def send_email(self, sender: str, recipient: str, subject: str, username: str, 
                   template: str = settings.MAIN_EMAIL_TEMPLATE, part1=None, part2=None, part3=None):
        message = Mail(
            from_email=sender,
            to_emails=recipient
        )
        message.dynamic_template_data = {
            'subject': subject,
            'username': username,
            'part_1': part1,
            'part_2': part2,
            'part_3': part3
        }
        
        self._send_mail_via_sendgrid(message, template)
    
    def _send_mail_via_sendgrid(self, message: Mail, template_id: str):
        try:
            api_key = settings.SENDGRID_API_KEY
            sg = SendGridAPIClient(api_key)
            message.template_id = template_id
            sg.send(message)
        except Exception as e:
            settings.logger.error(e)