from typing import Any

import aiohttp
import pytest_asyncio

from tests.config.settings import test_settings


@pytest_asyncio.fixture
async def make_post_request():
    # Make get request
    async def inner(
        path: str,
        query_data: dict[str, Any] = {},
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            headers=headers,
            cookies=cookies,
            trust_env=True,
        )

        async with session.post(url, json=query_data) as response:
            status = response.status
            cookies = response.cookies
            body = await response.json()
        return body, status, cookies

    return inner


@pytest_asyncio.fixture
async def make_get_request():
    # Make get request
    async def inner(
        path: str,
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            headers=headers,
            cookies=cookies,
            trust_env=True,
        )

        async with session.get(url) as response:
            status = response.status
            cookies = response.cookies
            body = await response.json()
        return body, status, cookies

    return inner


@pytest_asyncio.fixture
async def make_put_request():
    # Make get request
    async def inner(
        path: str,
        query_data: dict[str, Any] = {},
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            headers=headers,
            cookies=cookies,
            trust_env=True,
        )

        async with session.put(url, json=query_data) as response:
            status = response.status
            cookies = response.cookies
            body = await response.json()
        return body, status, cookies

    return inner


@pytest_asyncio.fixture
async def make_delete_request():
    # Make get request
    async def inner(
        path: str,
        query_data: dict[str, Any] = {},
        headers: dict[str, str] = {},
        cookies: dict[str, str] = {},
    ):
        url = "http://" + test_settings.SERVICE_URL + path
        session = aiohttp.ClientSession(
            headers=headers,
            cookies=cookies,
            trust_env=True,
        )

        async with session.delete(url, json=query_data) as response:
            status = response.status
            cookies = response.cookies
            body = await response.json()
        return body, status, cookies

    return inner
