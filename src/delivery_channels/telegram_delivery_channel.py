from .base_delivery_channel import DeliveryChannel

import asyncio
from aiogram import Bot, client


BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"


class TelegramDeliveryChannel(DeliveryChannel):
    def __init__(self, config, logger):
        super().__init__(config, logger)
        self.logger = logger
        bot_session = client.session.aiohttp.AiohttpSession(
            api=client.telegram.TelegramAPIServer.from_base(
                f"http://{config.telegram.host}:{config.telegram.port}"
            )
        )
        self.bot = Bot(
            token=BOT_TOKEN,
            session=bot_session
        )

    async def __send_message(self, chat_id: int, text: str):
        await self.bot.send_message(chat_id=chat_id, text=text)

    def send_message(self, user, subject: str, message: str):
        self.logger.debug("telegram send message")

        asyncio.run(self.__send_message(user.telegram_chat_id, message))
