from pydantic_settings import BaseSettings, SettingsConfigDict

logo = """
   _____ _     _ _        _____      _
  / ____| |   (_) |      / ____|    (_)
 | (___ | |__  _| |_ ___| |     _ __ _ _ __
  \\___ \\| '_ \\| | __/ _ \\ |    | '__| | '_ \
  ____) | | | | | ||  __/ |____| |  | | | | |
 |_____/|_| |_|_|\\__\\___|\\_____|_|  |_|_| |_|
"""


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
    TAPS_COUNT: list[int] = [200, 300]
    TAP_ENERGY_THRESHOLD: int = 50
    TAPS_DELAY: list[float] = [0.01, 0.08]
    # bot
    BOT_SLEEP_TIME: list[int] = [500, 1000]
    REF_ID: str = "0xyoilTXk9NZ4qOcp6E2tg"
    bot_name: str = "ShitCoinTap_Bot"


config = Settings()
