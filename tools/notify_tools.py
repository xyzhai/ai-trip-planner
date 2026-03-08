import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_deal_email(subject, html_content):
    """
    Sends the formatted deal report to your verified email.
    """
    message = Mail(
        from_email='your-verified-sender@domain.com',
        to_emails='your-personal-email@gmail.com',
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Email failed: {e}")