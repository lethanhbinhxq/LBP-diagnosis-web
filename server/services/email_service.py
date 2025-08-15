import os
from email.message import EmailMessage
from aiosmtplib import SMTP
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FEEDBACK_RECEIVER_EMAIL = os.getenv("FEEDBACK_RECEIVER_EMAIL")

async def send_feedback_email(name: str, email: str, message: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USERNAME
    msg["To"] = FEEDBACK_RECEIVER_EMAIL
    msg["Subject"] = f"[LBP Diagnosis] New Feedback from {name or 'Anonymous'}"

    body = f"""
------------------------------
New Feedback Submission
------------------------------

Name    : {name or 'N/A'}
Email   : {email or 'N/A'}

Message :
{message}

------------------------------
This message was sent from your Feedback Form.
"""

    msg.set_content(body)

    smtp = SMTP(hostname=SMTP_HOST, port=SMTP_PORT, start_tls=True)
    await smtp.connect()
    await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    await smtp.send_message(msg)
    await smtp.quit()
