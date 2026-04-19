import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "smtp.gmail.com"
port = 587

sender_email = "diakubamahunterforce@gmail.com"
password = "lrzgtyvrvoonxhua"  # não é a senha normal do Gmail


def send_email(to, subject, body):

    # 🔥 GARANTIR TIPOS CORRETOS
    to = str(to)
    subject = str(subject)
    body = str(body)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = f"Your App <{sender_email}>"
    msg["To"] = to

    # 🔥 UTF-8 (resolve erros de acentos)
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()

        server.login(sender_email, password)

        server.sendmail(sender_email, [to], msg.as_string())

        server.quit()

        print("Email enviado com sucesso")
        return True

    except Exception as e:
        print("Erro ao enviar email:", e)
        return False