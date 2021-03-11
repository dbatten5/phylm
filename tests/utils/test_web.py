"""Tests for the utils module"""

from bs4 import BeautifulSoup
from phylm.utils.web import url_encode, soupify


def test_url_encode():
    """Given a string
    When I call the url_encode function on it
    Then I expect the string to url encoded
    """
    string = 'A film with a / symbol'
    assert url_encode(string) == 'A+film+with+a+%2F+symbol'



def test_soupify_returns_a_bs4_object(requests_mock):
    """Given a url
    When I call the soupify function on it
    Then I expect to receive a Beautiful Soup object
    """
    url = 'https://movies.com/search/the+great+movie'
    resp = '<html><h1>The Great Movie</h1></html>'
    requests_mock.register_uri(
        'GET',
        url,
        request_headers={'User-agent': 'Mozilla/5.0'},
        text=resp,
    )
    soup = soupify(url)
    assert isinstance(soup, BeautifulSoup)
    assert soup.text == 'The Great Movie'
