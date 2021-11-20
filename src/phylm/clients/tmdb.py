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
        res = self.session.get(f"{self._base}/search/movie", params=payload)

        res.raise_for_status()

        results: List[Dict[str, Any]] = res.json()["results"]
        return results

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
            f"{self._base}/movie/{movie_id}/watch/providers", params=payload
        )

        res.raise_for_status()

        results: Dict[str, Any] = res.json()["results"]

        return {key: results[key.upper()] for key in regions}
