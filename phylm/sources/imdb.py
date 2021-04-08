"""Module to contain IMDb class definition"""

from typing import Optional, Union

import imdb
from imdb.Movie import Movie

class Imdb:
    """Class to abstract an IMDb movie object"""
    ia = imdb.IMDb()

    def __init__(self, raw_title) -> None:
        self.raw_title = raw_title
        self.low_confidence = False
        self._imdb_data = self._get_imdb_data()

    def _get_imdb_data(self) -> Union[dict, Movie]:
        results = Imdb.ia.search_movie(self.raw_title)
        if not results:
            return {}
        target = {}
        for result in results:
            if result['title'].lower() == self.raw_title.lower():
                target = result
                break
        if not target:
            target = results[0]
            self.low_confidence = True
        Imdb.ia.update(target, info=['main'])
        return target

    def title(self) -> Optional[str]:
        """Return the title"""
        return self._imdb_data.get('title')

    def genres(self, limit: int = 3) -> list[Optional[str]]:
        """Return the genres"""
        return self._imdb_data.get('genres', [])[:limit]

    def cast(self, limit: int = 5) -> list[Optional[str]]:
        """Return the cast"""
        return [person['name'] for person in self._imdb_data.get('cast', [])[:limit]]

    def runtime(self) -> Optional[int]:
        """Return the runtime"""
        return self._imdb_data.get('runtimes', [None])[0]

    def year(self) -> Optional[int]:
        """Return the year"""
        return self._imdb_data.get('year')

    def directors(self, limit: int = 3) -> list[Optional[str]]:
        """Return the directors"""
        return [person['name'] for person in self._imdb_data.get('directors', [])[:limit]]

    def score(self) -> Optional[str]:
        """Return the score"""
        return self._imdb_data.get('rating')

    def plot(self) -> Optional[str]:
        """Return the plot"""
        if not self._imdb_data:
            return None
        data = self._imdb_data
        if 'plot' not in data.current_info:
            Imdb.ia.update(data, info=['plot'])
        plot = data.get('plot')
        if not plot:
            return None
        return plot[0].split('::')[0]
