"""Module to contain Mtc class definition"""

from typing import Optional

import re

from phylm.utils.web import soupify, url_encode


class Mtc:
    """Class to abstract a Metacritic movie search result"""
    def __init__(self, raw_title):
        self.raw_title = raw_title
        self.low_confidence = False
        self._mtc_data = self._get_mtc_data()

    def _get_mtc_data(self):
        url_encoded_film = url_encode(self.raw_title)
        search_url = (
            f"https://www.metacritic.com/search/movie/{url_encoded_film}/results"
        )
        soup = soupify(search_url)
        results = soup.find_all("li", {"class": "result"})
        if not results:
            return None
        target = None
        for result in results:
            result_title = result.find("a").string.strip()
            if result_title.lower().strip() == self.raw_title.lower().strip():
                target = result
                break
        if target is None:
            target = results[0]
            self.low_confidence = True
        return target

    def title(self) -> Optional[str]:
        """Return the title"""
        if not self._mtc_data:
            return None
        return self._mtc_data.find("a").string.strip()

    def year(self) -> Optional[int]:
        """Return the year"""
        if not self._mtc_data:
            return None
        year_meta = self._mtc_data.find("p").string
        year_search = re.search(r'\d{4}', year_meta)
        if not year_search:
            return None
        return int(year_search.group())

    def score(self) -> Optional[str]:
        """Return the score"""
        if not self._mtc_data:
            return None
        return self._mtc_data.find('span', {'class': 'metascore_w'}).text
