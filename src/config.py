from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class MailSettings:
    host: str
    port: int


@dataclass(slots=True, kw_only=True)
class ApiSettings:
    url: str
    port: int


@dataclass(slots=True, kw_only=True)
class CommonSettings:
    level: str


@dataclass(slots=True, kw_only=True)
class TelegramSettings:
    host: str
    port: int


@dataclass(slots=True, kw_only=True)
class GraphiteConfig:
    prefix: str
    host: str
    port: int
    timeout: float = 2.0
    enabled: bool = True


@dataclass(slots=True, kw_only=True)
class Config:
    mail: MailSettings
    api: ApiSettings
    telegram: TelegramSettings
    common: CommonSettings
    graphite: GraphiteConfig
