"""Module to hold `phylm` tools."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from imdb.Movie import Movie

from phylm.clients.tmdb import initialize_tmdb_client
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
    query: str, api_key: Optional[str] = None, region: str = "us"
) -> List[Dict[str, Any]]:
    """Search for movies on TMDb.

    Args:
        query: the query string
        api_key: an api_key can either be provided here or through a TMDB_API_KEY env
            var
        region: an optional region to provide with the search request, affects the
            release_date value returned, must be provided in ISO 3166-1 format (eg.
            "us" or "gb")

    Returns:
        List[Dict[str, Any]]: the search results
    """
    client = initialize_tmdb_client(api_key=api_key)

    return client.search_movies(query=query, region=region)


def get_streaming_providers(
    tmdb_movie_id: str,
    regions: List[str],
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Return a list of streaming providers for a given movie.

    Args:
        tmdb_movie_id: the tmdb id of the movie
        regions: a list of regions to trim down the return list
        api_key: an api_key can either be provided here or through a TMDB_API_KEY env
            var

    Returns:
        Dict[str, Any]: a dictionary of streaming providers, keyed by region name
    """
    client = initialize_tmdb_client(api_key=api_key)

    return client.get_streaming_providers(movie_id=tmdb_movie_id, regions=regions)
