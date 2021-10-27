"""Module to define the Mtc class."""
import re
from typing import Match
from typing import Optional
from typing import Union

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import ResultSet
from bs4.element import Tag

from phylm.utils.web import soupify
from phylm.utils.web import url_encode

MTC_BASE_MOVIE_URL = "https://www.metacritic.com/search/movie"


class Mtc:
    """Class to abstract a Metacritic movie search result."""

    def __init__(self, raw_title: str) -> None:
        """Initialize the object.

        Args:
            raw_title: the given title of the movie
        """
        self.raw_title: str = raw_title
        self.low_confidence: bool = False
        self._mtc_data: Optional[Tag] = self._get_mtc_data()

    def _get_mtc_data(self) -> Optional[Tag]:
        """Scrape mtc for the movie.

        Attempt to find a match with the given `raw_title`. If none is found then select
        the first result and set `low_confidence` to `True`.
        """
        url_encoded_film: str = url_encode(self.raw_title)
        search_url: str = f"{MTC_BASE_MOVIE_URL}/{url_encoded_film}/results"
        soup: BeautifulSoup = soupify(search_url)
        results: ResultSet = soup.find_all("li", {"class": "result"})
        if not results:
            return None
        target = None
        for result in results:
            result_title: str = result.find("a").string.strip()
            if result_title.lower().strip() == self.raw_title.lower().strip():
                target = result
                break
        if target is None:
            target = results[0]
            self.low_confidence = True
        return target

    @property
    def title(self) -> Optional[str]:
        """Return the title.

        Returns:
            the title of the movie
        """
        if not self._mtc_data:
            return None
        title_tag: Optional[Union[Tag, NavigableString]] = self._mtc_data.find("a")
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
        year_tag: Optional[Union[Tag, NavigableString]] = self._mtc_data.find("p")
        if not year_tag:
            return None
        year_search: Optional[Match[str]] = re.search(r"\d{4}", year_tag.get_text())
        if not year_search:
            return None
        return int(year_search.group())

    @property
    def rating(self) -> Optional[str]:
        """Return the rating.

        Returns:
            the mtc rating
        """
        if not self._mtc_data:
            return None
        rating_tag: Optional[Union[Tag, NavigableString]] = self._mtc_data.find(
            "span", {"class": "metascore_w"}
        )
        if not rating_tag:
            return None
        return str(rating_tag.get_text().strip())
