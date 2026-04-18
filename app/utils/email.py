import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to, subject, body):
    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=to,
        subject=subject,
        html_content=f"<strong>{body}</strong>"
    )

    try:
        sg = SendGridAPIClient(os.getenv("5184b7870b05badd0a1df33c3ede8947"))
        response = sg.send(message)

        print("Status:", response.status_code)

    except Exception as e:
        print("Erro ao enviar email:", str(e))