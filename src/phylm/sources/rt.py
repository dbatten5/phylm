"""Module to hold the Rt class definition."""
from typing import Optional

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from bs4.element import Tag

from phylm.utils.web import async_soupify
from phylm.utils.web import url_encode

RT_BASE_MOVIE_URL = "https://www.rottentomatoes.com/search"


class Rt:
    """Class to abstract a Rotten Tomatoes result."""

    def __init__(self, raw_title: str, raw_year: Optional[int] = None) -> None:
        """Initialize the object.

        Args:
            raw_title: the given title of the movie
            raw_year: an optional year for improved matching
        """
        self.raw_title = raw_title
        self.raw_year = raw_year
        self.low_confidence = False
        self._rt_data: Optional[Tag] = None

    def _parse_data(self, soup: BeautifulSoup) -> Optional[Tag]:
        results = soup.find_all("search-page-media-row")

        if not results:
            return None

        # first try matching on year
        for result in results:
            release_year = result["releaseyear"]
            if self.raw_year and str(self.raw_year) == release_year:
                return result

        # then try matching on title
        for result in results:
            result_title: str = result.find_all("a")[-1].string.strip()
            if result_title.lower() == self.raw_title.lower().strip():
                return result

        # finally pick the first result
        self.low_confidence = True
        return results[0]

    async def _scrape_data(
        self, session: Optional[ClientSession] = None
    ) -> BeautifulSoup:
        url_encoded_film = url_encode(self.raw_title)
        search_url = f"{RT_BASE_MOVIE_URL}?search={url_encoded_film}"
        return await async_soupify(search_url, session)

    async def load_source(self, session: Optional[ClientSession] = None) -> None:
        """Asynchronously load the data from the source.

        Args:
            session: an optional instance of `aiohttp.ClientSession` in which to run the
                request
        """
        raw_data = await self._scrape_data(session=session)
        self._rt_data = self._parse_data(raw_data)

    @property
    def title(self) -> Optional[str]:
        """Return the title.

        Returns:
            the title of the movie
        """
        if not self._rt_data:
            return None

        title_tag = self._rt_data.find_all("a")[-1]

        if title_tag:
            return str(title_tag.get_text()).strip()

        return None

    @property
    def year(self) -> Optional[str]:
        """Return the year.

        Returns:
            the year of the movie
        """
        if not self._rt_data:
            return None

        return str(self._rt_data["releaseyear"])

    @property
    def tomato_score(self) -> Optional[str]:
        """Return the Tomatometer Score.

        Returns:
            the tomatometer score
        """
        if not self._rt_data:
            return None

        return str(self._rt_data["tomatometerscore"])
