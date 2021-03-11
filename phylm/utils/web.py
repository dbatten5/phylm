"""Module to contain some web helper functions"""

from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup


def soupify(url):
    """Get a webpage and return the BeautifulSoup representation"""
    user_agent = {'User-agent': 'Mozilla/5.0'}
    search = requests.get(url, headers=user_agent).text
    return BeautifulSoup(search, 'html.parser')


def url_encode(string):
    """URL encode a string to be used in search queries"""
    return quote_plus(string)
