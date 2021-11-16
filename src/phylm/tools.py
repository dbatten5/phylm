"""Module to hold `phylm` tools."""
from typing import Dict
from typing import List
from typing import Union

from imdb.Movie import Movie

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
