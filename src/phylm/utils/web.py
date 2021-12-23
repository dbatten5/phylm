"""Module to contain some web helper functions."""
from typing import Optional
from urllib.parse import quote_plus

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {"User-agent": "Mozilla/5.0"}


def soupify(url: str) -> BeautifulSoup:
    """Get a webpage and return the BeautifulSoup representation.

    Args:
        url (str): the url for scraping

    Returns:
        a `BeautifulSoup` representation of the given url
    """
    search = requests.get(url, headers=DEFAULT_HEADERS).text
    return BeautifulSoup(search, "html.parser")


async def async_soupify(
    url: str, session: Optional[ClientSession] = None
) -> BeautifulSoup:
    """Asynchronously get a webpage and return the BeautifulSoup representation.

    Args:
        url: the url for scraping
        session: an optional instance of `aiohttp.ClientSession` in which to run the
            request. If a session is passed here then it will remain open after this
            function returns.

    Returns:
        a `BeautifulSoup` representation of the given url
    """
    keep_session = False
    if session:
        keep_session = True

    session = session or ClientSession()
    async with session.get(url, headers=DEFAULT_HEADERS) as resp:
        html = await resp.text()

    if not keep_session:
        await session.close()

    return BeautifulSoup(html, "html.parser")


def url_encode(string: str) -> str:
    """URL encode a string to be used in search queries.

    Args:
        string (str): the string to be url encoded

    Returns:
        a url encoded string
    """
    return quote_plus(string)
