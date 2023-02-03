"""Module to define Tmdb class."""
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from aiohttp import ClientSession

from phylm.tools import initialize_tmdb_client


class Tmdb:
    """Class to abstract a TMDB result."""

    def __init__(
        self,
        raw_title: Optional[str] = None,
        movie_id: Optional[str] = None,
        raw_year: Optional[int] = None,
        api_key: Optional[str] = None,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize the object.

        Note that at least one of `raw_title` or `movie_id` must be given to be used as
        a search term. `movie_id` is preferred over `raw_title`.

        Args:
            raw_title: the title of the movie. Note that TMDB doesn't support fuzzy
                search.
            movie_id: the TMDB id of the movie.
            raw_year: an optional year for improved matching if only title is given.
            api_key: a TMDB api key. Must be supplied here or as an env var
            session: a `aiohttp.ClientSession` instance. One will be created if not
                supplied.

        Raises:
            ValueError: if neither `raw_title` nor `movie_id` is supplied.
        """
        if not (raw_title or movie_id):
            raise ValueError("At least one of raw_title and movie_id must be given")

        self.raw_title = raw_title
        self.movie_id = movie_id
        self.raw_year = raw_year
        self.low_confidence = False
        self.session = session
        self._api_key = api_key
        self._tmdb_data: Dict[str, Any] = {}

        self._client = initialize_tmdb_client(api_key, async_session=session)

    async def _get_tmdb_data(self) -> Dict[str, Any]:
        if self.movie_id:
            return await self._client.get_movie(self.movie_id)

        results = await self._client.search_movies_async(
            self.raw_title, year=self.raw_year  # type: ignore
        )

        if not results:
            return {}

        return await self._client.get_movie(results[0]["id"])

    async def load_source(self, session: Optional[ClientSession] = None) -> None:
        """Asynchronously load the data for from the source.

        Args:
            session: an optional `aiohttp.ClientSession` instance
        """
        if session:
            self._client = initialize_tmdb_client(self._api_key, async_session=session)

        self._tmdb_data = await self._get_tmdb_data()

    @property
    def title(self) -> Optional[str]:
        """Return the TMDB title.

        Returns:
            the title of the movie
        """
        return self._tmdb_data.get("title")

    @property
    def id(self) -> Optional[str]:
        """Return the TMDB id.

        Returns:
            the id of the movie
        """
        return str(self._tmdb_data.get("id"))

    @property
    def imdb_id(self) -> Optional[str]:
        """Return the IMDb id.

        Returns:
            the IMDb id of the movie
        """
        return str(self._tmdb_data.get("imdb_id"))

    def genres(self, limit: int = 3) -> List[str]:
        """Return the genres.

        Args:
            limit (int): an optional number of genres to return

        Returns:
            a list of the movie's genres
        """
        return [g["name"] for g in self._tmdb_data.get("genres", [])[:limit]]

    @property
    def runtime(self) -> Optional[int]:
        """Return the runtime.

        Returns:
            the runtime of the movie
        """
        runtime = self._tmdb_data.get("runtime")

        if not runtime:
            return None

        return int(runtime)

    @property
    def release_date(self) -> Optional[str]:
        """Return the movie's release_date.

        Returns:
            the release date of the movie
        """
        return self._tmdb_data.get("release_date")

    @property
    def year(self) -> Optional[int]:
        """Return the movie's year.

        Returns:
            the year the movie was made
        """
        release_date = self._tmdb_data.get("release_date")

        if not release_date:
            return None

        date = datetime.strptime(release_date, "%Y-%m-%d")
        return int(date.year)

    @property
    def rating(self) -> Optional[float]:
        """Return the TMDB rating.

        Returns:
            the rating of the movie
        """
        rating = self._tmdb_data.get("vote_average")

        if not rating:
            return None

        return float(rating)

    @property
    def plot(self) -> Optional[str]:
        """Return the plot.

        Returns:
            the plot of the movie
        """
        return self._tmdb_data.get("overview")
