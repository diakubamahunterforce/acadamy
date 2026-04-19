import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIGURAÇÕES
smtp_server = "smtp.gmail.com"
port = 587

sender_email = "diakubamahunterforce@gmail.com"
password = "lrzg tyvr voon xhua"  # não é a senha normal do Gmail
receiver_email = "diakubamalinuxo@gmail.com"

# CRIAR EMAIL
msg = MIMEMultipart()
msg["Subject"] = "Teste de envio de email com Python aç"
msg["From"] = "Your Name <youremail@gmail.com>"
msg["To"] = receiver_email

# CORPO DO EMAIL
body = "Olá! Este email foi enviado usando Python com smtplib."
msg.attach(MIMEText(body, "plain"))

# ENVIO
try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)

    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    print("Email enviado com sucesso!")
except Exception as e:
    print("Erro ao enviar email:", e)