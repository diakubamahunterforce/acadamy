import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# carregar .env
load_dotenv()

API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER = os.getenv("SENDER_EMAIL")

print("API KEY:", API_KEY)
print("SENDER:", SENDER)

try:
    message = Mail(
        from_email=SENDER,
        to_emails="diakubamahunterforce@gmail.com",  # coloca teu email para receber
        subject="Teste SendGrid",
        html_content="<strong>Funcionando!</strong>"
    )

    sg = SendGridAPIClient(API_KEY)
    response = sg.send(message)

    print("Status:", response.status_code)
    print("Body:", response.body)
    print("Headers:", response.headers)

except Exception as e:
    print("Erro:", str(e))