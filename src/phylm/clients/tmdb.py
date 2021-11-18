"""Client to interact with The Movie DB (TMDB)."""
from typing import Any

from requests import Session


class TmdbClient(Session):
    """Class to abstract to the Tmdb API."""

    def __init__(self, api_key: str) -> None:
        """Initialize the client.

        Args:
            api_key: an api_key for authentication
        """
        super().__init__()
        self.api_key = api_key
        self._base = "https://api.themoviedb.org/3"

    def search_movies(self, query: str) -> Any:
        """Search for movies.

        Args:
            query: the search query

        Returns:
            Any: the search results
        """
        payload = {
            "api_key": self.api_key,
            "language": "en-GB",
            "query": query,
            "include_adult": False,
            "region": "GB",
        }
        res = self.get(f"{self._base}/search/movie", params=payload)  # type: ignore
        return res.json()["results"]
