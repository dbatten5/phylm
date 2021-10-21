"""Tests for the utils module."""
from unittest.mock import Mock
from unittest.mock import patch

from bs4 import BeautifulSoup

from phylm.utils.web import soupify
from phylm.utils.web import url_encode


class TestUrlEncode:
    """Tests for the `url_encode` function."""

    def test_success(self) -> None:
        """
        Given a string with symbols
        When I call the url_encode function on it
        Then I expect the string to url encoded
        """
        string = "A film with a / symbol"

        result = url_encode(string)

        assert result == "A+film+with+a+%2F+symbol"


class TestSoupify:
    """Tests for the `soupify` function."""

    @patch("phylm.utils.web.requests", autospec=True)
    def test_returns_a_bs4_object(self, mock_requests):
        """
        Given a url
        When the soupify function is invoked with it
        Then `BeautifulSoup` object is returned
        """
        url = "https://movies.com/search/the+great+movie"
        resp = "<html><h1>The Great Movie</h1></html>"
        mock_requests.get.return_value = Mock(text=resp)

        result = soupify(url)

        assert isinstance(result, BeautifulSoup)
        assert result.text == "The Great Movie"
        mock_requests.get.assert_called_once_with(
            url=url, headers={"User-agent": "Mozilla/5.0"}
        )
