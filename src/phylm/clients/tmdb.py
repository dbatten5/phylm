"""Client to interact with The Movie DB (TMDB)."""
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from aiohttp import ClientSession
from requests import Session

from phylm.errors import NoTMDbApiKeyError


class TmdbClient:
    """Class to abstract to the Tmdb API."""

    def __init__(
        self, api_key: str, async_session: Optional[ClientSession] = None
    ) -> None:
        """Initialize the client.

        Args:
            api_key: an api_key for authentication
            async_session: an optional instance of `aiohttp.ClientSession`
        """
        self.session = Session()
        self.async_session = async_session or ClientSession()
        self.api_key = api_key
        self._base_url = "https://api.themoviedb.org/3"

    def search_movies(self, query: str, region: str = "us") -> List[Dict[str, Any]]:
        """Search for movies.

        Args:
            query: the search query
            region: the region for the query, affects the release date value

        Returns:
            List[Dict[str, Any]]: the search results
        """
        payload = {
            "api_key": self.api_key,
            "language": "en-US",
            "query": query,
            "include_adult": "false",
            "region": region.upper(),
        }
        res = self.session.get(f"{self._base_url}/search/movie", params=payload)

        res.raise_for_status()

        results: List[Dict[str, Any]] = res.json()["results"]
        return results

    async def search_movies_async(
        self, query: str, region: str = "us", year: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search for movies async.

        Args:
            query: the search query
            region: the region for the query, affects the release date value
            year: the year of the movie

        Returns:
            List[Dict[str, Any]]: the search results
        """
        params: Dict[str, Union[str, int]] = {
            "api_key": self.api_key,
            "language": "en-US",
            "query": query,
            "include_adult": "false",
            "region": region.upper(),
            "page": 1,
        }

        if year:
            params["year"] = year

        async with self.async_session.get(
            f"{self._base_url}/search/movie", params=params
        ) as resp:
            results = await resp.json()

        movies: List[Dict[str, Any]] = results["results"]
        return movies

    async def get_movie(self, movie_id: str) -> Dict[str, Any]:
        """Return a movie by id.

        Args:
            movie_id: the tmdb id of the movie

        Returns:
            Dict[str, Any]: a dictionary of the movie data
        """
        params = {
            "api_key": self.api_key,
            "language": "en-US",
        }

        async with self.async_session.get(
            f"{self._base_url}/movie/{movie_id}", params=params
        ) as resp:
            movie: Dict[str, Any] = await resp.json()

        return movie

    def get_streaming_providers(
        self, movie_id: str, regions: List[str]
    ) -> Dict[str, Any]:
        """Return a list of streaming providers for a given movie.

        Args:
            movie_id: the tmdb id of the movie
            regions: a list of regions to trim down the return list

        Returns:
            Dict[str, Any]: a dictionary of streaming providers, keyed by region name
        """
        payload = {"api_key": self.api_key}

        res = self.session.get(
            f"{self._base_url}/movie/{movie_id}/watch/providers", params=payload
        )

        res.raise_for_status()

        results: Dict[str, Any] = res.json()["results"]

        return {key: results.get(key.upper(), {}) for key in regions}


def initialize_tmdb_client(
    api_key: Optional[str] = None,
    async_session: Optional[ClientSession] = None,
) -> TmdbClient:
    """Initialize and return a TmdbClient.

    Args:
        api_key: an optional api_key to take precedence over an env var key
        async_session: an optional aiohttp ClienSession

    Raises:
        NoTMDbApiKeyError: when no api_key has been provided

    Returns:
        TmdbClient: an authorized Tmdb client
    """
    tmdb_api_key = api_key or os.environ.get("TMDB_API_KEY")

    if not tmdb_api_key:
        raise NoTMDbApiKeyError("An `api_key` must be provided to use this service")

    return TmdbClient(api_key=tmdb_api_key, async_session=async_session)
