"""Module for `Imdb` tests."""
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from imdb import IMDb
from imdb.Movie import Movie

from phylm.sources.imdb import Imdb

IMDB_IA_PATH = "phylm.sources.imdb.ia"

ia = IMDb()


@pytest.fixture(scope="module", name="the_matrix")
def the_matrix_fixture() -> Movie:
    """Return The Matrix IMDb Movie object"""
    return ia.search_movie("The Matrix")[0]


@pytest.fixture(scope="module", name="the_matrix_full")
def the_matrix_full_fixture() -> Movie:
    """Return The Matrix IMDb Movie object"""
    return ia.get_movie("0133093")


@pytest.fixture(scope="module", name="alien")
def alien_fixture() -> Movie:
    """Return The Matrix IMDb Movie object"""
    return ia.search_movie("Alien")[0]


class TestInit:
    """Tests for the `__init__` method."""

    @patch(IMDB_IA_PATH)
    def test_exact_match(
        self,
        mock_ia: MagicMock,
        the_matrix: Movie,
        alien: Movie,
    ) -> None:
        """
        Given a raw title,
        When there is an exact match from IMDb,
        Then the match is selected and low confidence remains False
        """
        mock_ia.search_movie.return_value = [the_matrix, alien]

        imdb = Imdb("Alien")

        assert imdb.title == "Alien"
        assert imdb.low_confidence is False

    @patch(IMDB_IA_PATH)
    def test_no_exact_match(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a raw title,
        When there is no exact match from IMDb,
        Then the first match is selected and low confidence is True
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb(raw_title)

        assert imdb.title == "The Matrix"
        assert imdb.low_confidence is True

    @patch(IMDB_IA_PATH)
    def test_no_results(self, mock_ia: MagicMock) -> None:
        """
        Given a raw title,
        When there is no exact match from IMDb,
        Then the first match is selected and low confidence is True
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = []

        imdb = Imdb(raw_title)

        assert imdb.title is None


class TestGenres:
    """Tests for the `genres` method."""

    @patch(IMDB_IA_PATH)
    def test_genres(self, mock_ia: MagicMock, the_matrix_full: Movie) -> None:
        """
        Given a match with genres,
        When the genres are retrieved,
        Then the genres are returned with a given limit
        """
        mock_ia.search_movie.return_value = [the_matrix_full]

        imdb = Imdb("The Matrix")

        assert imdb.genres(1) == ["Action"]

    @patch(IMDB_IA_PATH)
    def test_no_genres(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a match with no genres,
        When the genres are retrieved,
        Then an empty list is returned
        """
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb("The Matrix")

        assert imdb.genres(1) == []

    @patch(IMDB_IA_PATH)
    def test_no_results(self, mock_ia: MagicMock) -> None:
        """
        Given no search results,
        When the genres are retrieved,
        Then an empty list is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Matrix")

        assert imdb.genres(1) == []


class TestCast:
    """Tests for the `cast` method."""

    @patch(IMDB_IA_PATH)
    def test_cast(self, mock_ia: MagicMock, the_matrix_full: Movie) -> None:
        """
        Given a match with cast,
        When the cast is retrieved,
        Then the cast is returned with a given limit
        """
        mock_ia.search_movie.return_value = [the_matrix_full]

        imdb = Imdb("The Matrix")

        assert imdb.cast(1) == ["Keanu Reeves"]

    @patch(IMDB_IA_PATH)
    def test_no_cast(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a match with no cast,
        When the cast is retrieved,
        Then an empty list is returned
        """
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb("The Matrix")

        assert imdb.cast(1) == []

    @patch(IMDB_IA_PATH)
    def test_no_results(self, mock_ia: MagicMock) -> None:
        """
        Given no search results,
        When the cast is retrieved,
        Then an empty list is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Matrix")

        assert imdb.cast(1) == []


class TestRuntime:
    """Tests for the `runtime` method."""

    @patch(IMDB_IA_PATH)
    def test_runtime(self, mock_ia: MagicMock, the_matrix_full: Movie) -> None:
        """
        Given a match with runtime,
        When the runtime is retrieved,
        Then the runtime is returned
        """
        mock_ia.search_movie.return_value = [the_matrix_full]

        imdb = Imdb("The Matrix")

        assert imdb.runtime == "136"

    @patch(IMDB_IA_PATH)
    def test_no_runtime(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a match without runtime,
        When the runtime is retrieved,
        Then None is returned
        """
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb("The Matrix")

        assert imdb.runtime is None

    @patch(IMDB_IA_PATH)
    def test_no_results(self, mock_ia: MagicMock) -> None:
        """
        Given no search results,
        When the runtime is retrieved,
        Then `None` is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Matrix")

        assert imdb.runtime is None


class TestYear:
    """Tests for the `year` method."""

    @patch(IMDB_IA_PATH)
    def test_year(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a match with year,
        When the year is retrieved,
        Then the year is returned
        """
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb("The Matrix")

        assert imdb.year == 1999

    @patch(IMDB_IA_PATH)
    def test_no_year(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a match with year,
        When the year is retrieved,
        Then the year is returned
        """
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb("The Matrix")

        assert imdb.year == 1999

    @patch(IMDB_IA_PATH)
    def test_no_results(self, mock_ia: MagicMock) -> None:
        """
        Given no search results,
        When the year is retrieved,
        Then `None` is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Matrix")

        assert imdb.year is None


class TestDirectors:
    """Tests for the `directors` method."""

    @patch(IMDB_IA_PATH)
    def test_directors(self, mock_ia: MagicMock, the_matrix_full: Movie) -> None:
        """
        Given a match with directors,
        When the directors are retrieved,
        Then the directors are returned with a given limit
        """
        mock_ia.search_movie.return_value = [the_matrix_full]

        imdb = Imdb("The Matrix")

        assert imdb.directors(1) == ["Lana Wachowski"]

    @patch(IMDB_IA_PATH)
    def test_no_directors(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a match with no directors,
        When the directors is retrieved,
        Then an empty list is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb(raw_title)

        assert imdb.directors(1) == []

    @patch(IMDB_IA_PATH)
    def test_no_results(self, mock_ia: MagicMock) -> None:
        """
        Given no search results,
        When the directors are retrieved,
        Then an empty list is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Matrix")

        assert imdb.directors(1) == []


class TestRating:
    """Tests for the `rating` method."""

    @patch(IMDB_IA_PATH)
    def test_rating(self, mock_ia: MagicMock, the_matrix_full: Movie) -> None:
        """
        Given a match with a rating,
        When the rating are retrieved,
        Then the rating is returned
        """
        mock_ia.search_movie.return_value = [the_matrix_full]

        imdb = Imdb("The Matrix")

        assert imdb.rating == 8.7

    @patch(IMDB_IA_PATH)
    def test_no_rating(self, mock_ia: MagicMock, the_matrix: Movie) -> None:
        """
        Given a match with no rating,
        When the rating is retrieved,
        Then None is return
        """
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb("The Matrix")

        assert imdb.rating is None

    @patch(IMDB_IA_PATH)
    def test_no_results(self, mock_ia: MagicMock) -> None:
        """
        Given no search results,
        When the rating is retrieved,
        Then `None` is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Matrix")

        assert imdb.rating is None


class TestPlot:
    """Tests for the `plot` method."""

    @patch(IMDB_IA_PATH)
    def test_plot_data_already_retrieved(self, mock_ia: MagicMock) -> None:
        """
        Given a match with existing plot data,
        When the plot is retrieved,
        Then the plot is returned
        """
        raw_title = "The Movie"
        mock_movie = MagicMock(current_info=["plot"])
        movie_data = {"title": raw_title, "plot": ["the plot::author"]}
        mock_movie.get.return_value = movie_data["plot"]
        mock_ia.search_movie.return_value = [mock_movie]

        imdb = Imdb(raw_title)

        assert imdb.plot == "the plot"
        mock_movie.get.assert_called_once_with("plot")

    @patch(IMDB_IA_PATH)
    def test_without_plot_data_already_retrieved(self, mock_ia: MagicMock) -> None:
        """
        Given a match without existing plot data,
        When the plot is retrieved,
        Then the plot is fetched and then returned
        """
        raw_title = "The Movie"
        mock_movie = MagicMock()
        movie_data = {"title": "The Movie", "plot": ["the plot::author"]}
        mock_movie.get.return_value = movie_data["plot"]
        mock_ia.search_movie.return_value = [mock_movie]

        imdb = Imdb(raw_title)

        assert imdb.plot == "the plot"
        mock_ia.update.assert_called_with(mock_movie, info=["plot"])

    @patch(IMDB_IA_PATH)
    def test_no_plot_with_plot_data_already_retrieved(self, mock_ia: MagicMock) -> None:
        """
        Given a match with existing but empty plot data,
        When the plot is retrieved,
        Then None is returned
        """
        raw_title = "The Movie"
        mock_movie = MagicMock(current_info=["plot"])
        mock_movie.get.return_value = None
        mock_ia.search_movie.return_value = [mock_movie]

        imdb = Imdb(raw_title)

        assert imdb.plot is None

    @patch(IMDB_IA_PATH)
    def test_no_movie_results(self, mock_ia: MagicMock) -> None:
        """
        Given no match,
        When the plot is retrieved,
        Then None is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Movie")

        assert imdb.plot is None


class TestMovieId:
    """Tests for working with an IMDb `movie_id`."""

    def test_no_raw_title_or_movie_id(self) -> None:
        """
        When an `Imdb` instance is created without a `raw_title` or ` movie_id`,
        Then a `ValueError` is raised
        """
        with pytest.raises(
            ValueError,
            match="At least one of raw_title and movie_id must be given",
        ):
            Imdb()

    @patch(IMDB_IA_PATH)
    def test_valid_movie_id(
        self,
        mock_ia: MagicMock,
        the_matrix_full: Movie,
    ) -> None:
        """
        Given a valid `movie_id`,
        When there is a match from IMDb,
        Then the match is selected and `low_confidence` remains False
        """
        mock_ia.get_movie.return_value = the_matrix_full

        imdb = Imdb(movie_id="0133093")

        assert imdb.title == "The Matrix"
        assert imdb.low_confidence is False

    def test_invalid_movie_id_with_no_raw_title(
        self,
    ) -> None:
        """
        Given an unrecognised `movie_id` and no `raw_title` given,
        When there are no matches from IMDb,
        Then data remains as `None`
        """
        imdb = Imdb(movie_id="9999999999999999999999999999")

        assert imdb.title is None

    @patch(IMDB_IA_PATH)
    def test_invalid_movie_id_with_raw_title(
        self,
        mock_ia: MagicMock,
        the_matrix: Movie,
    ) -> None:
        """
        Given an unrecognised `movie_id` and a `raw_title` given,
        When there are no matches from IMDb id search,
        Then the title is used to perform the search
        """
        mock_ia.get_movie.return_value = Movie(movieID="9999999999999999999999999999")
        mock_ia.search_movie.return_value = [the_matrix]

        imdb = Imdb(raw_title="The Matrix", movie_id="9999999999999999999999999999")

        assert imdb.title == "The Matrix"

    @patch(IMDB_IA_PATH)
    def test_valid_movie_id_with_raw_title(
        self,
        mock_ia: MagicMock,
        the_matrix: Movie,
    ) -> None:
        """
        Given a recognized `movie_id` and a `raw_title` given,
        Then the movie_id is used to perform the search
        """
        mock_ia.get_movie.return_value = the_matrix

        imdb = Imdb(movie_id="0133093")

        assert imdb.title == "The Matrix"
        mock_ia.search_movie.assert_not_called()
