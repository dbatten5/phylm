"""Tests for the Tmdb client."""
import vcr
from tests.conftest import FIXTURES_DIR

from phylm.clients.tmdb import TmdbClient

VCR_FIXTURES_DIR = f"{FIXTURES_DIR}/clients/tmdb"


class TestSearchMovies:
    """Tests for the `search_movies` method."""

    @vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/the_matrix.yaml", filter_query_parameters=["api_key"]
    )
    def test_results(self) -> None:
        """
        Given a search query,
        When the `search_movies` method is invoked with the query,
        Then search results are returned from the api
        """
        client = TmdbClient(api_key="dummy_key")

        results = client.search_movies(query="The Matrix")

        assert len(results)
        assert results[0]["title"] == "The Matrix"
        assert results[0]["release_date"] == "1999-06-11"

    @vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/no_results.yaml", filter_query_parameters=["api_key"]
    )
    def test_no_results(self) -> None:
        """
        Given a search query with no results,
        When the `search_movies` method is invoked with the query,
        Then an empty list is returned from the api
        """
        client = TmdbClient(api_key="dummy_key")

        results = client.search_movies(query="aslkdjaskldjaslkdjaslkdjasd")

        assert len(results) == 0
