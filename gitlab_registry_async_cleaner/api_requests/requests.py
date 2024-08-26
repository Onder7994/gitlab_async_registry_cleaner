"""request module."""

import asyncio
from typing import Optional

import httpx

from gitlab_registry_async_cleaner.logger.logger import Logging

logger = Logging(__name__)


async def send_api_get_request(**kwargs) -> httpx.Response | None:
    """Send GET request to URL with some re-try."""
    async with httpx.AsyncClient(verify=kwargs.get("verify", False)) as client:
        for _ in range(int(kwargs.get("max_retries", 5))):
            try:
                response = await client.get(
                    url=kwargs.get("url"),
                    headers=kwargs.get("headers", None),
                    timeout=int(kwargs.get("timeout", 20)),
                    params=kwargs.get("params", None),
                )
                return response
            except httpx.RequestError as err:
                logger.error(
                    "Failed GET request on %s. Error: %s",
                    kwargs.get("url"),
                    err,
                )
            await asyncio.sleep(5)
        logger.error(
            "Failed GET request after %s retries on %s",
            kwargs.get("max_retries", 5),
            kwargs.get("url"),
        )
    return None


async def send_api_post_request(**kwargs) -> Optional[httpx.Response]:
    """Send POST request to URL with some re-try."""
    async with httpx.AsyncClient(verify=kwargs.get("verify", False)) as client:
        for _ in range(int(kwargs.get("max_retries", 5))):
            try:
                response = await client.post(
                    url=kwargs.get("url"),
                    json=kwargs.get("json", None),
                    headers=kwargs.get("headers", None),
                    data=kwargs.get("data", None),
                    timeout=int(kwargs.get("timeout", 20)),
                )
                return response
            except httpx.RequestError as err:
                logger.error(
                    "Failed POST request on %s. Error: %s",
                    kwargs.get("url"),
                    err,
                )
            await asyncio.sleep(5)
        logger.error(
            "Failed POST request after %s retries on %s",
            kwargs.get("max_retries", 5),
            kwargs.get("url"),
        )
    return None


async def send_api_delete_request(**kwargs) -> Optional[httpx.Response]:
    """Send DELETE request to URL with some re-try."""
    async with httpx.AsyncClient(verify=kwargs.get("verify", False)) as client:
        for _ in range(int(kwargs.get("max_retries", 5))):
            try:
                response = await client.delete(
                    url=kwargs.get("url"),
                    headers=kwargs.get("headers", None),
                    timeout=int(kwargs.get("timeout", 20)),
                )
                return response
            except httpx.RequestError as err:
                logger.error(
                    "Failed DELETE request on %s. Error: %s",
                    kwargs.get("url"),
                    err,
                )
            await asyncio.sleep(5)
        logger.error(
            "Failed DELETE request after %s retries on %s",
            kwargs.get("max_retries", 5),
            kwargs.get("url"),
        )
    return None
