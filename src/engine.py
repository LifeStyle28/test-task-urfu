from logging import Logger
from delivery_channels import get_delivery_channel, ChannelValidationError
from mock import users_map, random_theme_and_message

from themes import themes_map, ThemeValidationError
from config import Config
import time
import aiogram
from metrics import MetricsManager


class Engine:
    def __init__(self, config: Config, logger: Logger):
        self.cfg = config
        self.logger = logger
        self.metrics_manager = MetricsManager(self.cfg.graphite)

    def run(self):
        while True:
            self.do_run()
            time.sleep(5)
            self.metrics_manager.send_all_rps()

    def do_run(self):
        try:
            theme_id, message = random_theme_and_message(
                1, 10
            )  # как будто с обмена пришло что-то

            self.logger.debug(f"Theme id {theme_id} with message {message}")

            # отправляем рассылку всем юзерам
            for user in users_map.values():
                for channel_type in user.get_channels_list_by(
                    theme_id=theme_id
                ):
                    channel = get_delivery_channel(
                        channel_type=channel_type,
                        config=self.cfg,
                        logger=self.logger,
                    )
                    description = themes_map.get(theme_id).get_description
                    channel.send_message(
                        user=user, subject=description, message=message
                    )
        except aiogram.exceptions.AiogramError as e:
            self.logger.info(f"Error: {e}")
            self.metrics_manager.add_new_batch_size(
                type=self.metrics_manager.MetricErrorsTypes.AIOGRAM_ERROR,
                new_batch_size=1
            )
        except ThemeValidationError as e:
            self.logger.info(f"Error: {e}")
            self.metrics_manager.add_new_batch_size(
                type=self.metrics_manager.MetricErrorsTypes.THEME_ERROR,
                new_batch_size=1
            )
        except ChannelValidationError as e:
            self.logger.info(f"Error: {e}")
            self.metrics_manager.add_new_batch_size(
                type=self.metrics_manager.MetricErrorsTypes.DELIVERY_CHANNEL_ERROR,
                new_batch_size=1
            )
        except Exception as e:
            self.logger.info(f"Error: {e}")
            self.metrics_manager.add_new_batch_size(
                type=self.metrics_manager.MetricErrorsTypes.OTHER_ERROR,
                new_batch_size=1
            )
