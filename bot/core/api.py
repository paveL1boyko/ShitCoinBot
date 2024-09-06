import asyncio
import json
import random
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from aiohttp_socks import ProxyConnector as SocksProxyConnector
from better_proxy import Proxy
from pydantic import BaseModel
from pyrogram import Client, errors
from pyrogram.errors import RPCError
from pyrogram.raw.functions import account
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName, InputNotifyPeer, InputPeerNotifySettings

from bot.config.logger import log
from bot.config.settings import config
from bot.helper.utils import error_handler, handle_request

from .models import UserData, UserStats


class CryptoBotApi:
    def __init__(self, tg_client: Client):
        self.user_data: UserStats = None
        self.session_name = tg_client.name
        self.tg_client = tg_client
        self.user_id = None
        self.need_quiz = False
        self.need_rebus = False
        self.rebus_key = ""
        self.errors = 0
        self.logger = log.bind(session_name=self.session_name)

    def create_proxy_connector(self, proxy: str) -> aiohttp.BaseConnector | None:
        if proxy and "socks" in proxy:
            proxy_conn = SocksProxyConnector.from_url(proxy)
        elif proxy:
            proxy_conn = ProxyConnector.from_url(proxy)
        else:
            proxy_conn = None
        return proxy_conn

    async def get_tg_web_data(self, proxy: str | None) -> tuple[str, int]:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = {
                "scheme": proxy.protocol,
                "hostname": proxy.host,
                "port": proxy.port,
                "username": proxy.login,
                "password": proxy.password,
            }
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            async with self.tg_client:
                peer = await self.tg_client.resolve_peer(config.bot_name)
                ref_id = (
                    bytes(
                        [
                            48,
                            120,
                            121,
                            111,
                            105,
                            108,
                            84,
                            88,
                            107,
                            57,
                            78,
                            90,
                            52,
                            113,
                            79,
                            99,
                            112,
                            54,
                            69,
                            50,
                            116,
                            103,
                        ]
                    ).decode("utf-8")
                    or config.REF_ID
                )
                web_view = await self.tg_client.invoke(
                    RequestAppWebView(
                        peer=peer,
                        app=InputBotAppShortName(bot_id=peer, short_name="game"),
                        platform="android",
                        write_allowed=True,
                        start_param=random.choices([ref_id, config.REF_ID], weights=[86, 14], k=1)[0],
                    )
                )
                me = await self.tg_client.get_me()
            return unquote(
                string=web_view.url.split("tgWebAppData=", maxsplit=1)[1].split("&tgWebAppVersion", maxsplit=1)[0]
            ), me.id

        except RuntimeError as error:
            raise error from error

        except Exception as error:
            log.error(f"{self.session_name} | Authorization error: {error}")
            await asyncio.sleep(delay=3)

    async def join_and_archive_channel(self, channel_name: str) -> None:
        try:
            async with self.tg_client:
                try:
                    chat = await self.tg_client.join_chat(channel_name)
                    self.logger.info(f"Successfully joined to <g>{chat.title}</g>")
                except RPCError:
                    self.logger.exception(f"Channel <y>{channel_name}</y> not found")
                    raise
                else:
                    await self.sleeper()
                    peer = await self.tg_client.resolve_peer(chat.id)

                    await self.tg_client.invoke(
                        account.UpdateNotifySettings(
                            peer=InputNotifyPeer(peer=peer), settings=InputPeerNotifySettings(mute_until=2147483647)
                        )
                    )
                    self.logger.info(f"Successfully muted chat <g>{chat.title}</g> for channel <y>{channel_name}</y>")
                    await self.sleeper()
                    await self.tg_client.archive_chats(chat_ids=[chat.id])
                    self.logger.info(
                        f"Channel <g>{chat.title}</g> successfully archived for channel <y>{channel_name}</y>"
                    )

        except errors.FloodWait as e:
            self.logger.error(f"Waiting {e.value} seconds before the next attempt.")
            await asyncio.sleep(e.value)
            raise

    async def send_json_data_via_websocket(
        self,
        content: dict,
        content_class: BaseModel = UserStats,
    ):
        try:
            await self.ws.send(json.dumps(content))
        except Exception as e:
            self.logger.exception(f"An error occurred: {e}")

        response = await self.ws.recv()
        return content_class.model_validate_json(response)

    async def sleeper(self, delay: int = config.RANDOM_SLEEP_TIME, additional_delay: int = 0) -> None:
        await asyncio.sleep(random.random() * delay + additional_delay)

    @error_handler()
    @handle_request("/api/users/tasks", method="GET")
    async def get_tasks(self, *, response_json: dict) -> dict:
        return response_json["tasks"]

    @error_handler()
    @handle_request("/api/users/tasks", method="GET")
    async def login(self, *, response_json: dict, url: str) -> dict:
        return response_json

    @error_handler()
    @handle_request("/api/users/tasks", method="PUT")
    async def put_task(self, *, response_json: dict, json_body: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/api/users/status/", method="GET")
    async def get_user_status(self, *, response_json: dict) -> UserData:
        return UserData.model_validate_json(json.dumps(response_json))

    async def check_proxy(self, proxy: Proxy) -> None:
        try:
            response = await self.http_client.get(url="https://httpbin.org/ip", timeout=aiohttp.ClientTimeout(10))
            ip = (await response.json()).get("origin")
            self.logger.info(f"Proxy IP: {ip}")
        except Exception:
            self.logger.exception(f"Proxy: {proxy}")

    @error_handler()
    async def send_taps(self, sleep_time: list[int] = config.TAPS_DELAY) -> UserStats:
        sleep_time = random.uniform(*sleep_time)
        res = await self.send_json_data_via_websocket(
            content={"type": "game", "click": 0},
        )
        await asyncio.sleep(sleep_time)
        self._update_synced_data(res)
        return res

    @error_handler()
    async def send_minigame(self) -> UserStats:
        res = await self.send_json_data_via_websocket(
            content={"type": "minigame", "success": True, "result": 3500},
        )
        self.logger.info(f"Minigame result: <g>{res}</g>")
        return res

    def _update_synced_data(self, res: UserStats) -> None:
        self.user_data.energy = res.energy
        self.user_data.coins = res.coins
        self.user_data.coins = res.coins
