import os
import smtplib
from email.mime.text import MIMEText

EMAIL_FROM = os.getenv("EMAIL_FROM")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def send_reset_email(email, token):
    reset_url = f"https://skin-vision-brown.vercel.app/reset-password?token={token}"
    subject = "Reset your password"
    body = f"""
    <p>Hello,</p>
    <p>Click the link below to reset your password. This link will expire in 1 hour:</p>
    <p><a href="{reset_url}">{reset_url}</a></p>
    """

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(EMAIL_FROM, email, msg.as_string())
        return True
    except Exception as e:
        print(f"[Email Error] {e}")
        raise


SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp-relay.brevo.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM_BREVO = os.getenv("EMAIL_FROM")

def send_reset_email_brevo(email, token):
    reset_url = f"https://skin-vision-brown.vercel.app/reset-password?token={token}"
    subject = "Reset your password"
    body = f"""
    <p>Hello,</p>
    <p>Click <a href="{reset_url}">here</a> to reset your password. This link will expire in 1 hour.</p>
    """

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM_BREVO
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM_BREVO, email, msg.as_string())
        return True
    except Exception as e:
        print("[SMTP ERROR]", e)
        raise
