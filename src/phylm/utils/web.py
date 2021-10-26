"""Module to contain some web helper functions."""
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


def soupify(url: str) -> BeautifulSoup:
    """Get a webpage and return the BeautifulSoup representation.

    Args:
        url (str): the url for scraping

    Returns:
        a `BeautifulSoup` representation of the given url
    """
    user_agent = {"User-agent": "Mozilla/5.0"}
    search = requests.get(url, headers=user_agent).text
    return BeautifulSoup(search, "html.parser")


def url_encode(string: str) -> str:
    """URL encode a string to be used in search queries.

    Args:
        string (str): the string to be url encoded

    Returns:
        a url encoded string
    """
    return quote_plus(string)
