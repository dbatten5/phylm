"""Module to hold `phylm` tools."""
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from imdb.Movie import Movie

from phylm.clients.tmdb import TmdbClient
from phylm.errors import NoTMDbApiKeyError
from phylm.sources.imdb import ia


def search_movies(query: str) -> List[Dict[str, Union[str, int]]]:
    """Return a list of search results for a query.

    Args:
        query: the search query

    Returns:
        a list of search results
    """
    results: List[Movie] = ia.search_movie(query)

    return [
        {
            "title": r.data.get("title"),
            "kind": r.data.get("kind"),
            "year": r.data.get("year"),
            "imdb_id": r.movieID,
            "cover_photo": r.data.get("cover url"),
        }
        for r in results
    ]


def search_tmdb_movies(
    query: str, api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for movies on TMDb.

    Args:
        query: the query string
        api_key: an api_key can either be provided here or through a TMDB_API_KEY env
            var

    Raises:
        NoTMDbApiKeyError: when no api_key has been provided

    Returns:
        List[Dict[str, Any]]: the search results
    """
    tmdb_api_key = api_key or os.environ.get("TMDB_API_KEY")

    if not tmdb_api_key:
        raise NoTMDbApiKeyError("An `api_key` must be provided to use this service")

    client = TmdbClient(api_key=tmdb_api_key)

    return client.search_movies(query=query)
