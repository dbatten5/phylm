"""Module to contain the IMDb class definition."""
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import imdb
from imdb.Movie import Movie


class Imdb:
    """Class to abstract an IMDb movie object."""

    ia = imdb.IMDb()

    def __init__(self, raw_title: str) -> None:
        """Initialize the object."""
        self.raw_title = raw_title
        self.low_confidence = False
        self._imdb_data = self._get_imdb_data()

    def _get_imdb_data(self) -> Union[Dict, Movie]:
        results: List[Movie] = Imdb.ia.search_movie(self.raw_title)
        if not results:
            return {}
        target = {}
        for result in results:
            if result["title"].lower() == self.raw_title.lower():
                target = result
                break
        if not target:
            target = results[0]
            self.low_confidence = True
        Imdb.ia.update(target, info=["main"])
        return target

    def title(self) -> Optional[str]:
        """Return the IMDb title.

        Returns:
            the title of the movie
        """
        return self._imdb_data.get("title")

    def genres(self, limit: int = 3) -> List[str]:
        """Return the genres.

        Args:
            limit (int): an optional number of genres to return

        Returns:
            a list of the movie's genres
        """
        return self._imdb_data.get("genres", [])[:limit]

    def cast(self, limit: int = 5) -> List[str]:
        """Return the cast.

        Args:
            limit (int): an optional number of cast members to return

        Returns:
            a list of the movie's cast members
        """
        return [person["name"] for person in self._imdb_data.get("cast", [])[:limit]]

    def runtime(self) -> Optional[str]:
        """Return the runtime.

        Returns:
            the runtime of the movie
        """
        return self._imdb_data.get("runtimes", [None])[0]

    def year(self) -> Optional[int]:
        """Return the movie's year.

        Returns:
            the year the movie was made
        """
        return self._imdb_data.get("year")

    def directors(self, limit: int = 3) -> List[str]:
        """Return the director(s).

        Args:
            limit (int): an optional number of director to return

        Returns:
            a list of the movie's directors
        """
        return [
            person["name"] for person in self._imdb_data.get("directors", [])[:limit]
        ]

    def rating(self) -> Optional[float]:
        """Return the IMDb rating.

        Returns:
            the rating of the movie
        """
        return self._imdb_data.get("rating")

    def plot(self) -> Optional[str]:
        """Return the plot.

        Returns:
            the plot of the movie
        """
        if not self._imdb_data:
            return None
        data = self._imdb_data
        if "plot" not in data.current_info:
            Imdb.ia.update(data, info=["plot"])
        plot = data.get("plot")
        if not plot:
            return None
        return plot[0].split("::")[0]
