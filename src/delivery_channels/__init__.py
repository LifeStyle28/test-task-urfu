from logging import Logger

from .base_delivery_channel import DeliveryChannel
from .email_delivery_channel import EmailDeliveryChannel
from .telegram_delivery_channel import TelegramDeliveryChannel
from .personal_account_delivery_channel import PersonalAccountDeliveryChannel

from config import Config


channels_map = {
    "email": EmailDeliveryChannel,
    "telegram": TelegramDeliveryChannel,
    "personal_account": PersonalAccountDeliveryChannel,
}


class ChannelValidationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


def validate_channel(channel_type: str):
    if channel_type not in channels_map:
        raise ChannelValidationError(f"Channel type {channel_type} is not supported")


def get_delivery_channel(channel_type: str, config: Config, logger: Logger) -> DeliveryChannel:
    validate_channel(channel_type=channel_type)
    channel = channels_map.get(channel_type)
    return channel(config, logger)
