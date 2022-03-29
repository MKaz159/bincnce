import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText


def SendEmailToMKAZ(message):
    try:
        # Create your SMTP session
        smtp = smtplib.SMTP('smtp.gmail.com', 587)

        # Use TLS to add security
        smtp.starttls()
        # User Authentication
        load_dotenv()
        password = os.getenv('EMAIL_PASS')
        smtp.login("mark2binance@gmail.com", password)

        # Sending the Email
        smtp.sendmail("mark2binance@gmail.com", "markk2316@gmail.com", message)

        # Terminating the session
        smtp.quit()
        print("Email sent successfully!")

    except Exception as ex:
        print("Something went wrong....", ex)


def main():
    mes = 'Test (quickstart performed RUN operation)'
    SendEmailToMKAZ(mes)


if __name__ == '__main__':
    main()
