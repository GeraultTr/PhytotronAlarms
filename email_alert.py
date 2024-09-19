import smtplib
from email.mime.text import MIMEText

recipients = ["tristan.gerault@inrae.fr"]

def send_email_alert(body, subject="Phytotrons report"):
    subject = subject
    sender = "info.phytotrons.saclay"
    #recipients = ["tristan.gerault@inrae.fr", "alain.fortineau@inrae.fr"]
    password = "oxxx hqpq ksxi pqqb"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Alert message sent!")

if __name__ == "__main__":
    send_email_alert(body="test_alert")