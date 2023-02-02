"""Tests for the Tmdb client."""
import pytest
import vcr
from requests.exceptions import HTTPError
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
        assert results[0]["release_date"] == "1999-03-30"

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

    @vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/different_region.yaml", filter_query_parameters=["api_key"]
    )
    def test_override_region(self) -> None:
        """
        When the `search_movies` method is invoked with the region,
        Then the region is passed to the api request
        """
        client = TmdbClient(api_key="dummy_key")

        results = client.search_movies(query="The Matrix", region="gb")

        assert results[0]["release_date"] == "2021-12-22"

    @vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/invalid_key.yaml", filter_query_parameters=["api_key"]
    )
    def test_api_error(self) -> None:
        """
        When the `search_movies` method is invoked with an invalid api_key,
        Then an HTTP error is raised
        """
        client = TmdbClient(api_key="not_a_key")

        with pytest.raises(HTTPError):
            client.search_movies(query="The Matrix")


class TestSearchMoviesAsync:
    """Tests for the `search_movies_async` method."""

    @pytest.mark.asyncio
    async def test_success(self) -> None:
        """Movies search results are returned."""
        client = TmdbClient(api_key="not_a_key")

        with vcr.use_cassette(
            f"{VCR_FIXTURES_DIR}/the_matrix_async.yaml",
            filter_query_parameters=["api_key"],
        ) as cass:
            results = await client.search_movies_async(query="The Matrix")

            assert results[0]["title"] == "The Matrix Resurrections"

        cass.rewind()

        assert len(cass) == 1
        assert cass.requests[0].query == [
            ("include_adult", "false"),
            ("language", "en-US"),
            ("query", "The Matrix"),
            ("region", "US"),
        ]

    @pytest.mark.asyncio
    async def test_success_year(self) -> None:
        """Movies search results filtered by year are returned."""
        client = TmdbClient(api_key="not_a_key")

        with vcr.use_cassette(
            f"{VCR_FIXTURES_DIR}/the_matrix_year_async.yaml",
            filter_query_parameters=["api_key"],
        ) as cass:
            results = await client.search_movies_async(query="The Matrix", year=1999)

            breakpoint()
            assert results[0]["title"] == "The Matrix"

        cass.rewind()

        assert len(cass) == 1
        assert cass.requests[0].query == [
            ("include_adult", "false"),
            ("language", "en-US"),
            ("query", "The Matrix"),
            ("region", "US"),
            ("year", "1999"),
        ]

    @pytest.mark.asyncio
    async def test_no_results(self) -> None:
        """Empty list is returned for no results."""
        client = TmdbClient(api_key="not_a_key")

        with vcr.use_cassette(
            f"{VCR_FIXTURES_DIR}/search_no_results.yaml",
            filter_query_parameters=["api_key"],
        ):
            results = await client.search_movies_async(query="askdjhashdaskdasljd")

        assert results == []


class TestGetMovie:
    """Tests for the `get_movie` method."""

    @pytest.mark.asyncio
    async def test_success(self) -> None:
        """Movie result is returned."""
        client = TmdbClient(api_key="not_a_key")

        with vcr.use_cassette(
            f"{VCR_FIXTURES_DIR}/get_the_matrix.yaml",
            filter_query_parameters=["api_key"],
        ) as cass:
            results = await client.get_movie("603")

        assert results["title"] == "The Matrix"

        cass.rewind()

        assert len(cass) == 1
        assert cass.requests[0].query == [
            ("language", "en-US"),
        ]

    @pytest.mark.asyncio
    async def test_not_found(self) -> None:
        """Unrecognised movie id is handled."""
        client = TmdbClient(api_key="not_a_key")

        with vcr.use_cassette(
            f"{VCR_FIXTURES_DIR}/get_invalid_id.yaml",
            filter_query_parameters=["api_key"],
        ):
            results = await client.get_movie("xxxxx")

        assert results["success"] is False


class TestStreamingProviders:
    """Tests for the `get_streaming_providers` method."""

    @vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/matrix_providers.yaml", filter_query_parameters=["api_key"]
    )
    def test_results(self) -> None:
        """
        Given a movie id,
        When the `get_streaming_providers` method is invoked with the id,
        Then search results are returned from the api and keyed by region name
        """
        client = TmdbClient(api_key="dummy_key")

        results = client.get_streaming_providers(movie_id="603", regions=["gb", "fr"])

        assert "fr" in results
        assert "gb" in results
        assert "flatrate" in results["gb"]
        assert len(results["gb"]["flatrate"])

    @vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/no_data_providers.yaml",
        filter_query_parameters=["api_key"],
    )
    def test_results_no_data(self) -> None:
        """
        Given a movie id with no streaming data,
        When the `get_streaming_providers` method is invoked with the id,
        Then the issue is caught and an empty dictionary is returned
        """
        client = TmdbClient(api_key="dummy_key")

        results = client.get_streaming_providers(
            movie_id="674324",
            regions=["gb", "fr"],
        )

        assert "fr" in results
        assert "gb" in results
        assert results["gb"] == {}

    @vcr.use_cassette(
        f"{VCR_FIXTURES_DIR}/no_results_providers.yaml",
        filter_query_parameters=["api_key"],
    )
    def test_no_results(self) -> None:
        """
        Given an unrecognized movie id,
        When the `get_streaming_providers` method is invoked with the id,
        Then search results are returned from the api
        """
        client = TmdbClient(api_key="dummy_key")

        with pytest.raises(HTTPError):
            client.get_streaming_providers(movie_id="-1", regions=["gb"])
