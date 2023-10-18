"""Tests for the utils module."""
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from phylm.utils.web import DEFAULT_HEADERS
from phylm.utils.web import async_soupify
from phylm.utils.web import soupify
from phylm.utils.web import url_encode
from tests.conftest import FIXTURES_DIR
from tests.conftest import my_vcr

VCR_FIXTURES_DIR = f"{FIXTURES_DIR}/utils/web"


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
    def test_returns_a_bs4_object(self, mock_requests: MagicMock) -> None:
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
        mock_requests.get.assert_called_once_with(url=url, headers=DEFAULT_HEADERS)


class TestAsyncSoupify:
    """Tests for the `async_soupify` method."""

    async def test_success(self) -> None:
        """
        Given a url,
        When the `async_soupify` function is invoked,
        Then an async request is made to the url and the bs4 representation is returned
        """
        url = "http://httpbin.org"

        with my_vcr.use_cassette(
            f"{VCR_FIXTURES_DIR}/async_soupify.yaml",
            serializer="response_body_compressor",
        ) as cass:
            result = await async_soupify(url=url)
            assert len(cass.requests) == 1
            assert cass.requests[0].headers == DEFAULT_HEADERS

        assert isinstance(result, BeautifulSoup)

    @my_vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/async_soupify_gzip.yaml",
        serializer="response_body_compressor",
    )
    async def test_success_gzip(self) -> None:
        """
        Given a url with gzip encoded response,
        When the `async_soupify` function is invoked,
        Then an async request is made to the url
        """
        url = "http://httpbin.org/gzip"

        assert await async_soupify(url=url)

    @my_vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/async_soupify_gzip.yaml",
        serializer="response_body_compressor",
    )
    async def test_session_closed(self) -> None:
        """
        Given a url and an instance of `ClientSession`,
        When the `async_soupify` function is invoked,
        Then an async request is made and the session remains open
        """
        session = ClientSession()
        url = "http://httpbin.org/gzip"

        await async_soupify(url=url, session=session)

        assert not session.closed
