from distutils.command import config
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.config import Config
from typing import List
from pathlib import Path
import os
# Load .env
config = Config(".env")

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = config("MAIL_PORT"),
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_TLS = config("MAIL_TLS"),
    MAIL_SSL = config("MAIL_SSL"),
    USE_CREDENTIALS = config("USE_CREDENTIALS"),
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
