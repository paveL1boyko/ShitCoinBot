import asyncio
import base64
import random

import aiohttp
import websockets
from pyrogram import Client

from bot.config.headers import headers
from bot.config.logger import log
from bot.config.settings import config

from .api import CryptoBotApi
from .models import SessionData


class CryptoBot(CryptoBotApi):
    def __init__(self, tg_client: Client, additional_data: dict) -> None:
        super().__init__(tg_client)
        self.authorized = False
        self.id_counter: int = 0
        self.settings_was_set = False
        self.sleep_time = config.BOT_SLEEP_TIME
        self.additional_data: SessionData = SessionData.model_validate(
            {k: v for d in additional_data for k, v in d.items()}
        )

    async def login_to_app(self, proxy: str | None) -> bool:
        if self.authorized:
            return True
        tg_web_data, user_id = await self.get_tg_web_data(proxy=proxy)
        self.init_data_base64 = base64.b64encode(tg_web_data.encode()).decode()
        self.user_id = user_id
        self.authorized = True

        return self.authorized

    async def perform_taps(self) -> None:
        tap_count = random.randint(*config.TAPS_COUNT)
        tapped_count = 0
        self.logger.info("Performing taps...")
        while self.synced_data.energy:
            res = await self.send_taps()
            tapped_count += 1
            if self.synced_data.energy % config.TAP_ENERGY_THRESHOLD == 0:
                self.logger.info(f"Tapped balance total: <y>+{res.coins}</y>. Energy: <blue>{res.energy}</blue>")
            if tapped_count > tap_count:
                break

    async def check_and_complete_tasks(self) -> None:
        tasks = await self.get_tasks()
        for task in tasks:
            if (task_id := task["id"]) in [1, 2, 3, 4, 7] and not task["completed"]:
                await self.put_task(json_body={"task": task_id})
                self.logger.info(
                    f"Task <g>{task['type']}</g> completed Reward coins: <y>{task['revards_coins']}</y> Energy: <blue>{task['revards_energy']}</blue>"
                )
                await self.sleeper()

    async def run(self, proxy: str | None) -> None:
        proxy = proxy or self.additional_data.proxy

        async with aiohttp.ClientSession(
            headers=headers,
            connector=self.create_proxy_connector(proxy),
            timeout=aiohttp.ClientTimeout(total=60),
        ) as http_client:
            self.http_client = http_client
            if proxy:
                await self.check_proxy(proxy=proxy)

            while True:
                if self.errors >= config.ERRORS_BEFORE_STOP:
                    self.logger.error("Bot stopped (too many errors)")
                    break
                try:
                    await self.login_to_app(proxy)

                    http_client.headers["Init-Data"] = self.init_data_base64
                    # await self.login(
                    #     url=f"{config.api_path}/api/users/{self.user_id}/actions?init-data={self.init_data_base64}"
                    # )
                    await self.check_and_complete_tasks()
                    self.logger.info("Bot started")
                    ws_url = (
                        f"wss://{config.api_domain}/api/users/{self.user_id}/actions?init-data={self.init_data_base64}"
                    )
                    async with websockets.connect(ws_url) as ws:
                        self.ws = ws
                        self.synced_data = await self.send_taps()

                        if config.TAPS_ENABLED:
                            await self.perform_taps()
                        if self.synced_data.minigame:
                            await self.send_minigame()
                        sleep_time = random.randint(*config.BOT_SLEEP_TIME)
                        self.logger.info(f"Sleeping <c>{sleep_time}</c>")
                    await asyncio.sleep(sleep_time)

                except RuntimeError as error:
                    raise error from error
                except Exception:
                    self.errors += 1
                    self.authorized = False
                    self.logger.exception("Unknown error")
                    self.logger.info(f"Sleeping before retrying <y>{self.errors * 10}</y> seconds")
                    await self.sleeper(additional_delay=self.errors * 10)
                else:
                    self.errors = 0
                    self.authorized = False


async def run_bot(tg_client: Client, proxy: str | None, additional_data: dict) -> None:
    try:
        await CryptoBot(tg_client=tg_client, additional_data=additional_data).run(proxy=proxy)
    except RuntimeError:
        log.bind(session_name=tg_client.name).exception("Session error")
