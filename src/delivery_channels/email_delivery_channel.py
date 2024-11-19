from .base_delivery_channel import DeliveryChannel

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailDeliveryChannel(DeliveryChannel):
    def __init__(self, config, logger):
        super().__init__(config, logger)

    def send_message(self, user, subject: str, message: str):
        self.logger.debug(f"email send message to user {user.user_id}")

        msg = MIMEMultipart()
        msg["From"] = user.email
        msg["To"] = "server@mailhog.com"
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(self.config.mail.host, self.config.mail.port)
        server.set_debuglevel(0)
        server.send_message(msg)
        server.quit()
