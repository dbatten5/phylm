"""Module to define the Mtc class."""
import re
from typing import Optional

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from bs4.element import Tag

from phylm.utils.web import async_soupify
from phylm.utils.web import url_encode

MTC_BASE_MOVIE_URL = "https://www.metacritic.com/search/movie"


class Mtc:
    """Class to abstract a Metacritic movie search result."""

    def __init__(self, raw_title: str, raw_year: Optional[int] = None) -> None:
        """Initialize the object.

        Args:
            raw_title: the given title of the movie
            raw_year: an optional year for improved matching
        """
        self.raw_title = raw_title
        self.raw_year = raw_year
        self.low_confidence = False
        self._mtc_data: Optional[Tag] = None

    def _parse_data(self, soup: BeautifulSoup) -> Optional[Tag]:
        results = soup.find_all("li", {"class": "result"})

        if not results:
            return None

        # first try matching on year
        for result in results:
            year = _extract_year(result)
            if self.raw_year and self.raw_year == year:
                return result

        # then try matching on title
        for result in results:
            result_title: str = result.find("a").string.strip()
            if result_title.lower().strip() == self.raw_title.lower().strip():
                return result

        # finally pick the first result
        self.low_confidence = True
        return results[0]

    async def _scrape_data(
        self, session: Optional[ClientSession] = None
    ) -> BeautifulSoup:
        url_encoded_film = url_encode(self.raw_title)
        search_url = f"{MTC_BASE_MOVIE_URL}/{url_encoded_film}/results"
        return await async_soupify(search_url, session)

    async def load_source(self, session: Optional[ClientSession] = None) -> None:
        """Asynchronously load the data from the source.

        Args:
            session: an optional instance of `aiohttp.ClientSession` in which to run the
                request
        """
        raw_data = await self._scrape_data(session=session)
        self._mtc_data = self._parse_data(raw_data)

    @property
    def title(self) -> Optional[str]:
        """Return the title.

        Returns:
            the title of the movie
        """
        if not self._mtc_data:
            return None
        title_tag = self._mtc_data.find("a")
        if title_tag:
            return str(title_tag.get_text()).strip()
        return None

    @property
    def year(self) -> Optional[int]:
        """Return the year.

        Returns:
            the year of the movie
        """
        if not self._mtc_data:
            return None
        return _extract_year(self._mtc_data)

    @property
    def rating(self) -> Optional[str]:
        """Return the rating.

        Returns:
            the mtc rating
        """
        if not self._mtc_data:
            return None
        rating_tag = self._mtc_data.find("span", {"class": "metascore_w"})
        if not rating_tag:
            return None
        return str(rating_tag.get_text().strip())


def _extract_year(tag: Tag) -> Optional[int]:
    """Return the year if it exists in a tag.

    Args:
        tag: the mtc search result bs4 tag to search

    Returns:
        Optional[int]: the year of the movie
    """
    year_tag = tag.find("p")

    if not year_tag:
        return None

    year_search = re.search(r"\d{4}", year_tag.get_text())

    if not year_search:
        return None

    return int(year_search.group())
