"""Module to contain the IMDb class definition."""
from typing import List
from typing import Optional

import imdb
from imdb.Movie import Movie

ia = imdb.IMDb()


class Imdb:
    """Class to abstract an IMDb movie object."""

    def __init__(
        self,
        raw_title: Optional[str] = None,
        movie_id: Optional[str] = None,
    ) -> None:
        """Initialize the object.

        Note that at least one of `raw_title` or `movie_id` must be given to be used as
        a search term. `movie_id` is preferred over `raw_title`.

        Args:
            raw_title: the title of the movie
            movie_id: the `IMDb` id of the movie

        Raises:
            ValueError: if neither `raw_title` nor `movie_id` is supplied
        """
        if not (raw_title or movie_id):
            raise ValueError("At least one of raw_title and movie_id must be given")

        self.raw_title: Optional[str] = raw_title
        self.movie_id: Optional[str] = movie_id
        self.low_confidence: bool = False
        self._imdb_data: Optional[Movie] = self._get_imdb_data()

    def _get_imdb_data(self) -> Optional[Movie]:
        """Fetch the data from IMDb.

        If `self.movie_id` exists, prefer that as a search query, falling back to
        `self.raw_title` if that exists. If `movie_id` exists but is unrecognised
        by `IMDb` then we also fall back to the `raw_title`.

        Returns:
            an optional `IMDb` `Movie` object
        """
        if self.movie_id:
            get_movie_result: Movie = ia.get_movie(self.movie_id)
            if get_movie_result:
                return get_movie_result

        if not self.raw_title:
            return None

        results: List[Movie] = ia.search_movie(self.raw_title)
        if not results:
            return None
        target = None
        for result in results:
            if result["title"].lower() == self.raw_title.lower():
                target = result
                break
        if not target:
            target = results[0]
            self.low_confidence = True
        ia.update(target, info=["main"])

        return target

    @property
    def title(self) -> Optional[str]:
        """Return the IMDb title.

        Returns:
            the title of the movie
        """
        if not self._imdb_data:
            return None

        return str(self._imdb_data.get("title"))

    def genres(self, limit: int = 3) -> List[str]:
        """Return the genres.

        Args:
            limit (int): an optional number of genres to return

        Returns:
            a list of the movie's genres
        """
        if not self._imdb_data:
            return []

        return list(self._imdb_data.get("genres", [])[:limit])

    def cast(self, limit: int = 5) -> List[str]:
        """Return the cast.

        Args:
            limit (int): an optional number of cast members to return

        Returns:
            a list of the movie's cast members
        """
        if not self._imdb_data:
            return []

        return [person["name"] for person in self._imdb_data.get("cast", [])[:limit]]

    @property
    def runtime(self) -> Optional[str]:
        """Return the runtime.

        Returns:
            the runtime of the movie
        """
        if not self._imdb_data:
            return None

        runtimes = self._imdb_data.get("runtimes")

        if runtimes:
            return str(runtimes[0])

        return None

    @property
    def year(self) -> Optional[int]:
        """Return the movie's year.

        Returns:
            the year the movie was made
        """
        if not self._imdb_data:
            return None

        year = self._imdb_data.get("year")

        if not year:
            return None

        return int(year)

    def directors(self, limit: int = 3) -> List[str]:
        """Return the director(s).

        Args:
            limit (int): an optional number of director to return

        Returns:
            a list of the movie's directors
        """
        if not self._imdb_data:
            return []

        return [
            person["name"] for person in self._imdb_data.get("directors", [])[:limit]
        ]

    @property
    def rating(self) -> Optional[float]:
        """Return the IMDb rating.

        Returns:
            the rating of the movie
        """
        if not self._imdb_data:
            return None

        rating = self._imdb_data.get("rating")

        if not rating:
            return None

        return float(rating)

    @property
    def plot(self) -> Optional[str]:
        """Return the plot.

        Returns:
            the plot of the movie
        """
        if not self._imdb_data:
            return None

        data = self._imdb_data
        if "plot" not in data.current_info:
            ia.update(data, info=["plot"])

        plot = data.get("plot")

        if not plot:
            return None

        return str(plot[0].split("::")[0])
