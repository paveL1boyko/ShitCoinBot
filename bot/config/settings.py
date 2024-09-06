from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict

logo = """

███    ███ ██    ██ ███████ ██   ██     ███████ ███    ███ ██████  ██ ██████  ███████
████  ████ ██    ██ ██      ██  ██      ██      ████  ████ ██   ██ ██ ██   ██ ██
██ ████ ██ ██    ██ ███████ █████       █████   ██ ████ ██ ██████  ██ ██████  █████
██  ██  ██ ██    ██      ██ ██  ██      ██      ██  ██  ██ ██      ██ ██   ██ ██
██      ██  ██████  ███████ ██   ██     ███████ ██      ██ ██      ██ ██   ██ ███████

"""


class Strategy(str, Enum):
    flexible = "flexible"
    protective = "protective"
    aggressive = "aggressive"
    random = "random"


class League(str, Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platina = "platina"
    diamond = "diamond"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str
    SLEEP_BETWEEN_START: list[int] = [10, 50]
    api_path: str = "https://prodback.shitcoin.cool"
    api_domain: str = "prodback.shitcoin.cool"

    ERRORS_BEFORE_STOP: int = 5
    LOGIN_TIMEOUT: int = 3600
    RANDOM_SLEEP_TIME: int = 5
    USE_PROXY_FROM_FILE: bool = False
    ADD_LOCAL_MACHINE_AS_IP: bool = False

    # taps
    TAPS_ENABLED: bool = True
    TAPS_COUNT: list[int] = [300, 400]
    TAP_ENERGY_THRESHOLD: int = 50
    TAPS_DELAY: list[float] = [0.01, 0.08]
    # bot
    BOT_SLEEP_TIME: list[int] = [1500, 1800]
    REF_ID: str = "0xyoilTXk9NZ4qOcp6E2tg"
    bot_name: str = "ShitCoinTap_Bot"


config = Settings()
