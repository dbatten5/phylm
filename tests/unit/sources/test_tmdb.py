"""Module for TMDB tests."""
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from phylm.sources.tmdb import Tmdb
from tests.conftest import FIXTURES_DIR
from tests.conftest import vcr

MODULE_PATH = "phylm.sources.tmdb"
VCR_FIXTURES_DIR = f"{FIXTURES_DIR}/tmdb"
pytestmark = pytest.mark.asyncio


class TestInit:
    """Tests for TMDB init."""

    def test_no_raw_title_or_movie_id(self) -> None:
        """An error is raised if no title or movie_id."""
        with pytest.raises(
            ValueError,
            match="At least one of raw_title and movie_id must be given",
        ):
            Tmdb()

    async def test_initial_state(self) -> None:
        """All data points start out as none."""
        tmdb = Tmdb("Alien")

        assert tmdb.title is None

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_exact_match(self) -> None:
        """Exact title match and `low_confidence` remains `False`."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.title == "The Matrix"
        assert tmdb.low_confidence is False

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """No matches are handled"""
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        tmdb = Tmdb(raw_title)
        await tmdb.load_source()

        assert tmdb.title is None


class TestYearMatching:
    """Tests for the using year with title method."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix_3.yaml")
    async def test_year_match_first_result(self) -> None:
        """Year data is correctly used for getting search results."""
        tmdb = Tmdb(raw_title="The Matrix", raw_year=2021)
        await tmdb.load_source()

        assert tmdb.title == "The Matrix Resurrections"
        assert tmdb.year == 2021


class TestLoadSource:
    """Tests for the `load_source` method."""

    @patch(f"{MODULE_PATH}.initialize_tmdb_client")
    async def test_movie_id(self, mock_initialize_client: MagicMock) -> None:
        """`movie_id` is used to get result."""
        get_movie_mock = AsyncMock()
        mock_initialize_client.return_value.get_movie = get_movie_mock

        tmdb = Tmdb(movie_id="abc")

        await tmdb.load_source()

        get_movie_mock.assert_awaited_once_with("abc")

    @patch(f"{MODULE_PATH}.initialize_tmdb_client")
    async def test_title_and_year(self, mock_initialize_client: MagicMock) -> None:
        """`raw_title` and `raw_year` are used to get result."""
        tmdb_client = mock_initialize_client.return_value

        search_movies_mock = AsyncMock()
        search_movies_mock.return_value = [{"id": "abc"}]
        tmdb_client.search_movies_async = search_movies_mock

        get_movie_mock = AsyncMock()
        tmdb_client.get_movie = get_movie_mock

        tmdb = Tmdb(raw_title="The Matrix", raw_year=1999)

        await tmdb.load_source()

        search_movies_mock.assert_awaited_once_with("The Matrix", year=1999)
        get_movie_mock.assert_awaited_once_with("abc")

    @patch(f"{MODULE_PATH}.initialize_tmdb_client")
    async def test_no_results(self, mock_initialize_client: MagicMock) -> None:
        """No results are returned."""
        tmdb_client = mock_initialize_client.return_value

        search_movies_mock = AsyncMock()
        search_movies_mock.return_value = []
        tmdb_client.search_movies_async = search_movies_mock

        get_movie_mock = AsyncMock()
        tmdb_client.get_movie = get_movie_mock

        tmdb = Tmdb(raw_title="The Matrix", raw_year=1999)

        await tmdb.load_source()

        search_movies_mock.assert_awaited_once_with("The Matrix", year=1999)
        get_movie_mock.assert_not_awaited()

    @patch(f"{MODULE_PATH}.initialize_tmdb_client")
    async def test_new_session(self, mock_initialize_client: MagicMock) -> None:
        """A supplied session is used."""
        get_movie_mock = AsyncMock()
        mock_initialize_client.return_value.get_movie = get_movie_mock

        tmdb = Tmdb(movie_id="abc")

        mock_session = Mock()
        await tmdb.load_source(session=mock_session)

        assert mock_initialize_client.call_count == 2
        assert mock_initialize_client.call_args_list[1][1] == {
            "async_session": mock_session
        }


class TestId:
    """Tests for the `id` property."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """The TMDB id can be returned."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.id == "603"


class TestImdbId:
    """Tests for the `imdb_id` property."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """The IMDb id can be returned."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.imdb_id == "tt0133093"


class TestGenres:
    """Tests for the `genres` method."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """The IMDb id can be returned."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.genres() == ["Action", "Science Fiction"]


class TestRuntime:
    """Tests for the `runtime` property."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """The runtime can be returned."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.runtime == 136


class TestReleaseDate:
    """Tests for the `release_date` property."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """The release date can be returned."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.release_date == "1999-03-30"


class TestRating:
    """Tests for the `rating` property."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """The rating can be returned."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.rating == 8.2


class TestPlot:
    """Tests for the `plot` property."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """The plot can be returned."""
        tmdb = Tmdb("The Matrix")
        await tmdb.load_source()

        assert tmdb.plot
