from distutils.command import config
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.config import Config
from typing import List
from pathlib import Path

# Load .env
config = Config(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = Path(__file__).parent.parent / 'templates'
)


async def send_email(subject: str, recipient: List, message: dict):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        template_body = message
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="body.html")
