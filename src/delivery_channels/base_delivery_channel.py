from logging import Logger
from abc import ABC, abstractmethod

import config


class DeliveryChannel(ABC):
    def __init__(self, config: config.Config, logger: Logger):
        self.config = config
        self.logger = logger

    @abstractmethod
    def send_message(self, user, subject: str, message: str):
        pass
