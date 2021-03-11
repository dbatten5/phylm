import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus


def soupify(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    search = requests.get(url, headers=user_agent).text
    return BeautifulSoup(search, 'html.parser')


def url_encode(string):
    return quote_plus(string)
