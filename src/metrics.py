import socket
from datetime import datetime

import config

from enum import Enum, auto


def send_service_metric(
    cfg: config.GraphiteConfig, metric_name: str, metric_value: float
):
    if not cfg.enabled:
        return

    now_ts = int(datetime.now().timestamp())

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.settimeout(cfg.timeout)

        server_address = (cfg.host, cfg.port)
        udp_sock.connect(server_address)

        metric = (
            f"{cfg.prefix}{metric_name} {metric_value:.4f} {now_ts}\n".encode()
        )
        udp_sock.send(metric)


class RpsCalculator:
    avg_rps = 0
    batch_size = 0

    def __init__(self, cfg: config.GraphiteConfig, metric_name: str):
        self.cfg = cfg
        self.last_update = datetime.now()
        self.metric_name = metric_name

    def send_rps(self, new_batch_size: int = 0):
        self.batch_size += new_batch_size

        now = datetime.now()
        diff = (now - self.last_update).total_seconds()
        if diff >= 60:
            self.avg_rps = self.batch_size / diff
            self.last_update = now
            self.batch_size = 0
        send_service_metric(self.cfg, self.metric_name, self.avg_rps)


class MetricsManager:
    class MetricErrorsTypes(Enum):
        AIOGRAM_ERROR = auto()
        THEME_ERROR = auto()
        DELIVERY_CHANNEL_ERROR = auto()
        OTHER_ERROR = auto()

    def __init__(self, cfg: config.GraphiteConfig):
        self.metrics = {
            self.MetricErrorsTypes.AIOGRAM_ERROR: RpsCalculator(cfg, "aiogram_errors_rps"),
            self.MetricErrorsTypes.THEME_ERROR: RpsCalculator(cfg, "theme_errors_rps"),
            self.MetricErrorsTypes.DELIVERY_CHANNEL_ERROR: RpsCalculator(cfg, "delivery_channel_errors_rps"),
            self.MetricErrorsTypes.OTHER_ERROR: RpsCalculator(cfg, "other_errors_rps")
        }

    def add_new_batch_size(self, type: MetricErrorsTypes, new_batch_size):
        if type in self.metrics:
            self.metrics[type].send_rps(new_batch_size=new_batch_size)

    def send_all_rps(self):
        for metric in self.metrics.values():
            metric.send_rps()
