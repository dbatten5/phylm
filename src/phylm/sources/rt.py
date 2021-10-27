"""Module to hold the Rt class definition."""
from typing import Optional
from typing import Union

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from bs4.element import ResultSet
from bs4.element import Tag

from phylm.utils.web import soupify
from phylm.utils.web import url_encode

RT_BASE_MOVIE_URL = "https://www.rottentomatoes.com/search"


class Rt:
    """Class to abstract a Rotten Tomatoes result."""

    def __init__(self, raw_title: str) -> None:
        """Initialize the object.

        Args:
            raw_title: the given title of the movie
        """
        self.raw_title: str = raw_title
        self.low_confidence: bool = False
        self._rt_data: Optional[Tag] = self._get_rt_data()

    def _get_rt_data(self) -> Optional[Tag]:
        """Scrape rt for the movie.

        Attempt to find a match with the given `raw_title`. If none is found then select
        the first result and set `low_confidence` to `True`.
        """
        url_encoded_film: str = url_encode(self.raw_title)
        search_url: str = f"{RT_BASE_MOVIE_URL}?search={url_encoded_film}"
        soup: BeautifulSoup = soupify(search_url)
        results: ResultSet = soup.find_all("search-page-media-row")
        if not results:
            return None
        target = None
        for result in results:
            result_title: str = result.find_all("a")[-1].string.strip()
            if result_title.lower() == self.raw_title.lower().strip():
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
        if not self._rt_data:
            return None

        title_tag: Optional[Union[Tag, NavigableString]] = self._rt_data.find_all("a")[
            -1
        ]

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
