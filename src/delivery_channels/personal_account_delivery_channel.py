from .base_delivery_channel import DeliveryChannel

import requests


class PersonalAccountDeliveryChannel(DeliveryChannel):
    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.url = f"http://{config.api.url}:{config.api.port}/send-message"
        self.logger = logger

    def send_message(self, user, subject: str, message: str):
        self.logger.debug(
            f"personal account delivery message with user_id"
            f"{user.user_id} and message {message}"
        )

        url = f"{self.url}/{user.user_id}"
        self.logger.debug(f"url: {url}")
        data = {"message": message}
        response = requests.post(url, json=data)
        self.logger.debug(f"response: {response}")
