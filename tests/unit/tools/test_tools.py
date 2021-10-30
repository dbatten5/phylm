"""Tests for the `tools` module."""
from typing import List
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from imdb import IMDb
from imdb.Movie import Movie

from phylm.tools import search_movies

ia = IMDb()


TOOLS_MODULE_PATH = "phylm.tools"


@pytest.fixture(scope="module", name="the_matrix")
def the_matrix_fixture() -> List[Movie]:
    """Return The Matrix IMDb Movie object."""
    return list(ia.search_movie("The Matrix"))


class TestSearchMovies:
    """Tests for the `search_movies` function."""

    @patch(f"{TOOLS_MODULE_PATH}.ia", autospec=True)
    def test_results(self, mock_ia: MagicMock, the_matrix: List[Movie]) -> None:
        """
        Given a search query,
        When the `search_movies` function is invoked with the query,
        Then a list of search results is returned
        """
        mock_ia.search_movie.return_value = the_matrix

        result: List[Movie] = search_movies("the matrix")

        assert len(result)
        assert result[0]["imdb_id"] == "0133093"
        assert result[0]["title"] == "The Matrix"
        assert result[0]["year"] == 1999
        assert result[0]["cover url"]
