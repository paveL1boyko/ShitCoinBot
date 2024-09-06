import asyncio
import random
from collections.abc import Callable
from functools import wraps

from bot.config.settings import config


def error_handler(delay=3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                await asyncio.sleep(random.randint(delay, delay * 2))
                raise

        return wrapper

    return decorator


def handle_request(
    endpoint: str,
    full_url: bool = False,
    method: str = "POST",
    raise_for_status: bool = True,
    json_body: dict | None = None,
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            url = kwargs.get("url")
            endpoint_ = url or endpoint
            url = endpoint_ if full_url else config.api_path + endpoint_
            if method.upper() == "GET":
                response = await self.http_client.get(url)
            else:
                _json_body = kwargs.get("json_body") or json_body or {}
                response = await self.http_client.request(method, url, json=_json_body)
            if raise_for_status:
                response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                response_data = await response.json()
            elif "text/" in content_type:
                response_data = await response.text()
            else:
                response_data = await response.read()
            return await func(self, response_json=response_data, **kwargs)

        return wrapper

    return decorator
