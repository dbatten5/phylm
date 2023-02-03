"""Tests for the `tools` module."""
import os
from typing import List
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from imdb import IMDb
from imdb.Movie import Movie

from phylm.errors import NoTMDbApiKeyError
from phylm.tools import get_streaming_providers
from phylm.tools import search_movies
from phylm.tools import search_tmdb_movies

TOOLS_MODULE_PATH = "phylm.tools"


@pytest.fixture(scope="module", name="imdb_ia")
def imdb_ia_fixture() -> IMDb:
    """Return the IMDb class."""
    return IMDb()


@pytest.fixture(scope="module", name="the_matrix")
def the_matrix_fixture(imdb_ia: IMDb) -> List[Movie]:
    """Return The Matrix IMDb Movie object."""
    return list(imdb_ia.search_movie("The Matrix"))


class TestSearchMovies:
    """Tests for the `search_movies` function."""

    @patch(f"{TOOLS_MODULE_PATH}.ia", autospec=True)
    def test_results(self, mock_ia: MagicMock, the_matrix: List[Movie]) -> None:
        """
        Given a search query,
        When the `search_movies` function is invoked with the query,
        Then a list of search results is returned
        """
        mock_ia.search_movie.return_value = the_matrix[:3]

        result: List[Movie] = search_movies("the matrix")

        assert len(result)
        assert result[0]["imdb_id"] == "0133093"
        assert result[0]["title"] == "The Matrix"
        assert result[0]["year"] == 1999
        assert result[0]["cover_photo"]


class TestSearchTmdbMovies:
    """Tests for the `search_tmdb_movies` method."""

    @patch.dict(os.environ, {"TMDB_API_KEY": ""}, clear=True)
    def test_no_api_key(self) -> None:
        """
        Given no api key,
        When the `search_tmdb_movies` function is invoked,
        Then a NoTMDbApiKeyError is raised
        """
        with pytest.raises(NoTMDbApiKeyError):
            search_tmdb_movies(query="The Matrix")

    @patch(f"{TOOLS_MODULE_PATH}.initialize_tmdb_client", autospec=True)
    def test_with_api_key_as_arg(self, mock_initialize_tmdb_client: MagicMock) -> None:
        """
        Given an api_key supplied as an arg,
        When the `search_tmdb_movies` function is invoked,
        Then the api_key is used in the client
        """
        api_key = "nice_key"
        mock_tmdb_client = mock_initialize_tmdb_client.return_value
        mock_tmdb_client.search_movies.return_value = [{"title": "The Matrix"}]

        results = search_tmdb_movies(query="The Matrix", api_key=api_key)

        assert results == [{"title": "The Matrix"}]
        mock_initialize_tmdb_client.assert_called_once_with(api_key=api_key)
        mock_tmdb_client.search_movies.assert_called_once_with(
            query="The Matrix", region="us"
        )

    @patch(f"{TOOLS_MODULE_PATH}.initialize_tmdb_client", autospec=True)
    def test_different_region(self, mock_initialize_tmdb_client: MagicMock) -> None:
        """
        Given a region supplied as an arg,
        When the `search_tmdb_movies` function is invoked,
        Then the region is passed to the `search_movies` method
        """
        api_key = "nice_key"
        mock_tmdb_client = mock_initialize_tmdb_client.return_value
        mock_tmdb_client.search_movies.return_value = [{"title": "The Matrix"}]

        results = search_tmdb_movies(query="The Matrix", api_key=api_key, region="gb")

        assert results == [{"title": "The Matrix"}]
        mock_tmdb_client.search_movies.assert_called_once_with(
            query="The Matrix", region="gb"
        )


class TestGetStreamingProviders:
    """Tests for the `get_streaming_providers` method."""

    @patch(f"{TOOLS_MODULE_PATH}.initialize_tmdb_client", autospec=True)
    def test_success(
        self,
        mock_initialize_client: MagicMock,
    ) -> None:
        """
        Given an api_key supplied as an arg,
        When the `get_streaming_providers` function is invoked,
        Then the results are returned
        """
        api_key = "nice_key"
        mock_tmdb_client = mock_initialize_client.return_value
        mock_tmdb_client.get_streaming_providers.return_value = {"gb": "Netflix"}

        results = get_streaming_providers(
            tmdb_movie_id="123",
            regions=["gb"],
            api_key=api_key,
        )

        assert results == {"gb": "Netflix"}
        mock_initialize_client.assert_called_once_with(api_key=api_key)
