"""Module for `Imdb` tests."""
import pytest
from tests.conftest import FIXTURES_DIR
from tests.conftest import my_vcr

from phylm.sources.imdb import Imdb

VCR_FIXTURES_DIR = f"{FIXTURES_DIR}/imdb"
IMDB_IA_PATH = "phylm.sources.imdb.ia"
pytestmark = pytest.mark.asyncio
my_vcr.serializer = "response_body_compressor"


class TestInit:
    """Tests for the `__init__` method."""

    def test_initial_state(self) -> None:
        """
        When the `Imdb` class is instantiated,
        Then the data is `None`
        """
        imdb = Imdb("Alien")

        assert imdb.title is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_exact_match(
        self,
    ) -> None:
        """
        Given a raw title,
        When there is an exact match from IMDb,
        Then the match is selected and low confidence remains False
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.title == "The Matrix"
        assert imdb.low_confidence is False

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrixy.yaml")
    async def test_no_exact_match(self) -> None:
        """
        Given a raw title,
        When there is no exact match from IMDb,
        Then the first match is selected and low confidence is True
        """
        raw_title = "The Matrixy"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.title == "The Matrix"
        assert imdb.low_confidence is True

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given a raw title,
        When there is no exact match from IMDb,
        Then the first match is selected and low confidence is True
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.title is None


class TestYearMatching:
    """Tests for the `init` method with a `raw_title`."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix_3.yaml")
    async def test_year_match_first_result(self) -> None:
        """
        Given a `raw_title` and `raw_year`
        When the source is instantiated
        Then the year is the preferred method of matching
        """
        imdb = Imdb(raw_title="The Matrix", raw_year=2021)
        await imdb.load_source()

        assert imdb.title == "The Matrix Resurrections"
        assert imdb.year == 2021


class TestGenres:
    """Tests for the `genres` method."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_genres(self) -> None:
        """
        Given a match with genres,
        When the genres are retrieved,
        Then the genres are returned with a given limit
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.genres(1) == ["Action"]

    # @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    # async def test_no_genres(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
    #     """
    #     Given a match with no genres,
    #     When the genres are retrieved,
    #     Then an empty list is returned
    #     """
    #     mock_ia.search_movie.return_value = [the_matrix]

    #     imdb = Imdb("The Matrix")
    #     await imdb.load_data()

    #     assert imdb.genres(1) == []

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given no search results,
        When the genres are retrieved,
        Then an empty list is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.genres(1) == []


class TestCast:
    """Tests for the `cast` method."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_cast(self) -> None:
        """
        Given a match with cast,
        When the cast is retrieved,
        Then the cast is returned with a given limit
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.cast(1) == ["Keanu Reeves"]

    # @patch(IMDB_IA_PATH)
    # async def test_no_cast(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
    #     """
    #     Given a match with no cast,
    #     When the cast is retrieved,
    #     Then an empty list is returned
    #     """
    #     mock_ia.search_movie.return_value = [the_matrix]

    #     imdb = Imdb("The Matrix")
    #     await imdb.load_data()

    #     assert imdb.cast(1) == []

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given no search results,
        When the cast is retrieved,
        Then an empty list is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.cast(1) == []


class TestRuntime:
    """Tests for the `runtime` method."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_runtime(self) -> None:
        """
        Given a match with runtime,
        When the runtime is retrieved,
        Then the runtime is returned
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.runtime == "136"

    #     @patch(IMDB_IA_PATH)
    #     async def test_no_runtime(
    #         self,
    #         mock_ia: MagicMock,
    #         the_matrix: Movie,
    #     ) -> None:
    #         """
    #         Given a match without runtime,
    #         When the runtime is retrieved,
    #         Then None is returned
    #         """
    #         mock_ia.search_movie.return_value = [the_matrix]

    #         imdb = Imdb("The Matrix")
    #         await imdb.load_data()

    #         assert imdb.runtime is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given no search results,
        When the runtime is retrieved,
        Then `None` is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.runtime is None


class TestId:
    """Tests for the `id` property."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """
        Given a match with id,
        When the year is retrieved,
        Then the id is returned
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.id == "0133093"

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given no search results,
        When the id is retrieved,
        Then `None` is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.id is None


class TestYear:
    """Tests for the `year` method."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_year(self) -> None:
        """
        Given a match with year,
        When the year is retrieved,
        Then the year is returned
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.year == 1999

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given no search results,
        When the year is retrieved,
        Then `None` is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.year is None


class TestDirectors:
    """Tests for the `directors` method."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_directors(self) -> None:
        """
        Given a match with directors,
        When the directors are retrieved,
        Then the directors are returned with a given limit
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.directors(1) == ["Lana Wachowski"]

    # @patch(IMDB_IA_PATH)
    # async def test_no_directors(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
    #     """
    #     Given a match with no directors,
    #     When the directors is retrieved,
    #     Then an empty list is returned
    #     """
    #     raw_title = "The Movie"
    #     mock_ia.search_movie.return_value = [the_matrix]

    #     imdb = Imdb(raw_title)
    #     await imdb.load_data()

    #     assert imdb.directors(1) == []

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given no search results,
        When the directors are retrieved,
        Then an empty list is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.directors(1) == []


class TestRating:
    """Tests for the `rating` method."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix.yaml")
    async def test_rating(self) -> None:
        """
        Given a match with a rating,
        When the rating are retrieved,
        Then the rating is returned
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert imdb.rating == 8.7

    # @patch(IMDB_IA_PATH)
    # async def test_no_rating(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
    #     """
    #     Given a match with no rating,
    #     When the rating is retrieved,
    #     Then None is return
    #     """
    #     mock_ia.search_movie.return_value = [the_matrix]

    #     imdb = Imdb("The Matrix")
    #     await imdb.load_data()

    #     assert imdb.rating is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given no search results,
        When the rating is retrieved,
        Then `None` is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.rating is None


class TestPlot:
    """Tests for the `plot` method."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix_by_id.yaml")
    async def test_plot_data_already_retrieved(
        self,
    ) -> None:
        """
        Given a match with existing plot data,
        When the plot is retrieved,
        Then the plot is returned
        """
        imdb = Imdb(movie_id="0133093")
        await imdb.load_source()

        assert isinstance(imdb.plot, str)
        assert "Neo" in imdb.plot

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix_and_plot.yaml")
    async def test_without_plot_data_already_retrieved(self) -> None:
        """
        Given a match without existing plot data,
        When the plot is retrieved,
        Then the plot is fetched and then returned
        """
        imdb = Imdb("The Matrix")
        await imdb.load_source()

        assert isinstance(imdb.plot, str)
        assert "Neo" in imdb.plot

    # @patch(IMDB_IA_PATH)
    # async def test_no_plot_with_plot_data_already_retrieved(
    #     self,
    #     mock_ia: MagicMock,
    # ) -> None:
    #     """
    #     Given a match with existing but empty plot data,
    #     When the plot is retrieved,
    #     Then None is returned
    #     """
    #     raw_title = "The Movie"
    #     mock_movie = MagicMock(current_info=["plot"])
    #     mock_movie.get.return_value = None
    #     mock_ia.search_movie.return_value = [mock_movie]

    #     imdb = Imdb(raw_title)
    #     await imdb.load_data()

    #     assert imdb.plot is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_movie_results(self) -> None:
        """
        Given no match,
        When the plot is retrieved,
        Then None is returned
        """
        raw_title = "asldkjnkasnxlajsnxkasjxnas"

        imdb = Imdb(raw_title)
        await imdb.load_source()

        assert imdb.plot is None


class TestMovieId:
    """Tests for working with an IMDb `movie_id`."""

    async def test_no_raw_title_or_movie_id(self) -> None:
        """
        When an `Imdb` instance is created without a `raw_title` or ` movie_id`,
        Then a `ValueError` is raised
        """
        with pytest.raises(
            ValueError,
            match="At least one of raw_title and movie_id must be given",
        ):
            Imdb()

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/the_matrix_by_id.yaml")
    async def test_valid_movie_id(
        self,
    ) -> None:
        """
        Given a valid `movie_id`,
        When there is a match from IMDb,
        Then the match is selected and `low_confidence` remains False
        """
        imdb = Imdb(movie_id="0133093")
        await imdb.load_source()

        assert imdb.title == "The Matrix"
        assert imdb.low_confidence is False

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results_by_id.yaml")
    async def test_invalid_movie_id_with_no_raw_title(
        self,
    ) -> None:
        """
        Given an unrecognised `movie_id` and no `raw_title` given,
        When there are no matches from IMDb,
        Then data remains as `None`
        """
        imdb = Imdb(movie_id="9999999999999999999999999999")
        await imdb.load_source()

        assert imdb.title is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results_by_id_and_title.yaml")
    async def test_invalid_movie_id_with_raw_title(
        self,
    ) -> None:
        """
        Given an unrecognised `movie_id` and a `raw_title` given,
        When there are no matches from IMDb id search,
        Then the title is used to perform the search
        """
        imdb = Imdb(raw_title="The Matrix", movie_id="9999999999999999999999999999")
        await imdb.load_source()

        assert imdb.title == "The Matrix"


#     @patch(IMDB_IA_PATH)
#     async def test_valid_movie_id_with_raw_title(
#         self,
#         mock_ia: MagicMock,
#         the_matrix: Movie,
#     ) -> None:
#         """
#         Given a recognized `movie_id` and a `raw_title` given,
#         Then the movie_id is used to perform the search
#         """
#         mock_ia.get_movie.return_value = the_matrix

#         imdb = Imdb(movie_id="0133093")
#         await imdb.load_data()

#         assert imdb.title == "The Matrix"
#         mock_ia.search_movie.assert_not_called()
