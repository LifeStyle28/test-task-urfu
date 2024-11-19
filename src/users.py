from typing import Dict, Set, List
from delivery_channels import validate_channel
from enum import Enum, auto
from themes import validate_theme

import re


class EmailValidationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


# вроде должны фронты такое проверить, но пусть будет и тут
def validate_email(email: str):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise EmailValidationError(f"Email {email} is not valid")


class User:
    class OperationType(Enum):
        ADD = auto()
        REMOVE = auto()

    active_themes_list: Dict[int, Set[str]]

    def __init__(
        self,
        user_id: int,
        email: str,
        telegram_chat_id: int,
        init_themes_list: Dict[int, Set[str]],
    ):
        validate_email(email=email)
        self.email = email
        self.user_id = user_id
        self.telegram_chat_id = telegram_chat_id
        self.active_themes_list = init_themes_list

    def __make_operation_with_communication_channel(
        self, theme_id: int, channels: List[str], type: OperationType
    ):
        validate_theme(theme_id=theme_id)
        if theme_id in self.active_themes_list:
            for channel in channels:
                validate_channel(channel)
                if channel not in self.active_themes_list[theme_id]:
                    if type == self.OperationType.ADD:
                        self.active_themes_list[theme_id].add(channel)
                    elif type == self.OperationType.REMOVE:
                        self.active_themes_list[theme_id].discard(channel)

    def add_communication_channels(self, theme_id: int, channels: List[str]):
        self.__make_operation_with_communication_channel(
            theme_id=theme_id, channels=channels, type=self.OperationType.ADD
        )

    def remove_communication_channel(self, theme_id: int, channels: List[str]):
        self.__make_operation_with_communication_channel(
            theme_id=theme_id,
            channels=channels,
            type=self.OperationType.REMOVE,
        )

    def get_channels_list_by(self, theme_id: int) -> List[str]:
        themes_list = self.active_themes_list.get(theme_id)
        if themes_list is None:
            return []
        return themes_list
