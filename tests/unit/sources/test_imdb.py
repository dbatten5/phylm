"""Module for `Imdb` tests."""
from unittest.mock import MagicMock
from unittest.mock import patch

from phylm.sources.imdb import Imdb

IMDB_IA_PATH = "phylm.sources.imdb.Imdb.ia"


class TestInit:
    """Tests for the `__init__` method."""

    @patch(IMDB_IA_PATH)
    def test_exact_match(self, mock_ia: MagicMock) -> None:
        """
        Given a raw title,
        When there is an exact match from IMDb,
        Then the match is selected and low confidence remains False
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {"title": "Another Movie"},
            {"title": raw_title},
        ]

        imdb = Imdb(raw_title)

        assert imdb.title() == raw_title
        assert imdb.low_confidence is False

    @patch(IMDB_IA_PATH)
    def test_no_exact_match(self, mock_ia: MagicMock) -> None:
        """
        Given a raw title,
        When there is no exact match from IMDb,
        Then the first match is selected and low confidence is True
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {"title": "A Movie"},
            {"title": "Another Movie"},
        ]

        imdb = Imdb(raw_title)

        assert imdb.title() == "A Movie"
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

        assert imdb.title() is None


class TestGenres:
    """Tests for the `genres` method."""

    @patch(IMDB_IA_PATH)
    def test_genres(self, mock_ia: MagicMock) -> None:
        """
        Given a match with genres,
        When the genres are retrieved,
        Then the genres are returned with a given limit
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {"title": raw_title, "genres": ["Action", "Comedy"]}
        ]

        imdb = Imdb(raw_title)

        assert imdb.genres(1) == ["Action"]

    @patch(IMDB_IA_PATH)
    def test_no_genres(self, mock_ia: MagicMock) -> None:
        """
        Given a match with no genres,
        When the genres are retrieved,
        Then an empty list is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [{"title": raw_title}]

        imdb = Imdb(raw_title)

        assert imdb.genres(1) == []


class TestCast:
    """Tests for the `cast` method."""

    @patch(IMDB_IA_PATH)
    def test_cast(self, mock_ia: MagicMock) -> None:
        """
        Given a match with cast,
        When the cast is retrieved,
        Then the cast is returned with a given limit
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {
                "title": raw_title,
                "cast": [{"name": "Tom"}, {"name": "Dick"}],
            }
        ]

        imdb = Imdb(raw_title)

        assert imdb.cast(1) == ["Tom"]

    @patch(IMDB_IA_PATH)
    def test_no_cast(self, mock_ia: MagicMock) -> None:
        """
        Given a match with no cast,
        When the cast is retrieved,
        Then an empty list is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [{"title": raw_title}]
        imdb = Imdb(raw_title)
        assert imdb.cast(1) == []


class TestRuntime:
    """Tests for the `runtime` method."""

    @patch(IMDB_IA_PATH)
    def test_runtime(self, mock_ia: MagicMock) -> None:
        """
        Given a match with runtime,
        When the runtime is retrieved,
        Then the runtime is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {
                "title": raw_title,
                "runtimes": ["100", "90"],
            }
        ]

        imdb = Imdb(raw_title)

        assert imdb.runtime() == "100"

    @patch(IMDB_IA_PATH)
    def test_no_runtime(self, mock_ia: MagicMock) -> None:
        """
        Given a match without runtime,
        When the runtime is retrieved,
        Then None is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [{"title": raw_title}]

        imdb = Imdb(raw_title)

        assert imdb.runtime() is None


class TestYear:
    """Tests for the `year` method."""

    @patch(IMDB_IA_PATH)
    def test_year(self, mock_ia: MagicMock) -> None:
        """
        Given a match with year,
        When the year is retrieved,
        Then the year is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {
                "title": raw_title,
                "year": 2000,
            }
        ]

        imdb = Imdb(raw_title)

        assert imdb.year() == 2000

    @patch(IMDB_IA_PATH)
    def test_no_year(self, mock_ia: MagicMock) -> None:
        """
        Given a match without year,
        When the year is retrieved,
        Then None is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [{"title": raw_title}]

        imdb = Imdb("The Movie")

        assert imdb.year() is None


class TestDirectors:
    """Tests for the `directors` method."""

    @patch(IMDB_IA_PATH)
    def test_directors(self, mock_ia: MagicMock) -> None:
        """
        Given a match with directors,
        When the directors are retrieved,
        Then the directors are returned with a given limit
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {
                "title": raw_title,
                "directors": [{"name": "Tom"}, {"name": "Dick"}],
            }
        ]

        imdb = Imdb(raw_title)

        assert imdb.directors(1) == ["Tom"]

    @patch(IMDB_IA_PATH)
    def test_no_directors(self, mock_ia: MagicMock) -> None:
        """
        Given a match with no directors,
        When the directors is retrieved,
        Then an empty list is returne
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [{"title": raw_title}]

        imdb = Imdb(raw_title)

        assert imdb.directors(1) == []


class TestRating:
    """Tests for the `rating` method."""

    @patch(IMDB_IA_PATH)
    def test_rating(self, mock_ia: MagicMock) -> None:
        """
        Given a match with a rating,
        When the rating are retrieved,
        Then the rating is returned
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [
            {
                "title": raw_title,
                "rating": 8.1,
            }
        ]

        imdb = Imdb(raw_title)

        assert imdb.rating() == 8.1

    @patch(IMDB_IA_PATH)
    def test_no_rating(self, mock_ia: MagicMock) -> None:
        """
        Given a match with no rating,
        When the rating is retrieved,
        Then None is return
        """
        raw_title = "The Movie"
        mock_ia.search_movie.return_value = [{"title": raw_title}]

        imdb = Imdb(raw_title)

        assert imdb.rating() is None


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

        assert imdb.plot() == "the plot"
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

        assert imdb.plot() == "the plot"
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

        assert imdb.plot() is None

    @patch(IMDB_IA_PATH)
    def test_no_movie_results(self, mock_ia: MagicMock) -> None:
        """
        Given no match,
        When the plot is retrieved,
        Then None is returned
        """
        mock_ia.search_movie.return_value = []

        imdb = Imdb("The Movie")

        assert imdb.plot() is None
