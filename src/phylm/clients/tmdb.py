"""Client to interact with The Movie DB (TMDB)."""
from typing import Any
from typing import Dict
from typing import List

from requests import Session


class TmdbClient:
    """Class to abstract to the Tmdb API."""

    def __init__(self, api_key: str) -> None:
        """Initialize the client.

        Args:
            api_key: an api_key for authentication
        """
        super().__init__()
        self.session = Session()
        self.api_key = api_key
        self._base = "https://api.themoviedb.org/3"

    def search_movies(self, query: str) -> List[Dict[str, Any]]:
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
        res = self.session.get(f"{self._base}/search/movie", params=payload)
        results: List[Dict[str, Any]] = res.json()["results"]
        return results
