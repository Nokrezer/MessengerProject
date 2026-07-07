from email.message import EmailMessage
import aiosmtplib

from settings.config import *

import asyncio

class EmailService():
    async def _send_email(self, email, subject, message):
        message_info = EmailMessage()
        message_info["From"] = EMAIL_SENDER
        message_info["To"] = email
        message_info["Subject"] = subject
        message_info.set_content(message)

        await aiosmtplib.send(
            message_info,
            hostname=EMAIL_SMTP,
            port=EMAIL_SMTP_PORT,
            username=EMAIL_SENDER,
            password=EMAIL_APP_PASSWORD,
            start_tls=True
        )
    
    async def send_auth_code(self, email, code):
        asyncio.create_task(self._send_email(email, "Код для входа", code))

    async def send_reg_code(self, email, code):
        asyncio.create_task(self._send_email(email, "Код для регистрации", code))