"""Tests for the Mtc class."""
from unittest.mock import patch

from phylm.sources.mtc import Mtc


class TestInit:
    """Tests for the `__init__` method."""

    @patch("phylm.sources.mtc.soupify")
    def test_exact_match(self, mock_soup, matrix_results):
        """
        Given a raw title,
        When there is an exact match from Mtc,
        Then the match is selected and low confidence remains False
        """
        mock_soup.return_value = matrix_results
        mtc = Mtc("The Matrix")

        assert mtc.title() == "The Matrix"
        assert mtc.low_confidence is False

    @patch("phylm.sources.mtc.soupify")
    def test_exact_match_ignoring_case_and_spaces(self, mock_soup, matrix_results):
        """
        Given a raw title,
        When there is an exact match from Mtc,
        Then the match is selected and low confidence remains False
        """
        mock_soup.return_value = matrix_results
        mtc = Mtc(" the matrix ")

        assert mtc.title() == "The Matrix"
        assert mtc.low_confidence is False

    @patch("phylm.sources.mtc.soupify")
    def test_no_exact_match(self, mock_soup, matrix_results):
        """
        Given a raw title,
        When there is no exact match from Mtc,
        Then the first match is selected and low confidence is True
        """
        mock_soup.return_value = matrix_results
        mtc = Mtc("blort")

        assert mtc.title() == "The Matrix"
        assert mtc.low_confidence is True


class TestTitle:
    """Tests for the `title` method"""

    @patch("phylm.sources.mtc.soupify")
    def test_no_results(self, mock_soup, no_results):
        """
        Given a raw title with no results from Mtc,
        When the title is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        mtc = Mtc("blort")

        assert mtc.title() is None


class TestYear:
    """Tests for the `year` method"""

    @patch("phylm.sources.mtc.soupify")
    def test_match(self, mock_soup, matrix_results):
        """
        Given a raw title with a match from Mtc,
        When the year is retrieved,
        Then the year can be returned
        """
        mock_soup.return_value = matrix_results
        mtc = Mtc("The Matrix")

        assert mtc.year() == 1999

    @patch("phylm.sources.mtc.soupify")
    def test_no_results(self, mock_soup, no_results):
        """
        Given a raw title with no results from Mtc,
        When the year is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        mtc = Mtc("blort")

        assert mtc.year() is None

    @patch("phylm.sources.mtc.soupify")
    def test_no_match(self, mock_soup, no_results):
        """
        Given a raw title with results from Mtc but no year data,
        When the year is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        mtc = Mtc("A Glitch in the Matrix")

        assert mtc.low_confidence is False
        assert mtc.year() is None


class TestRating:
    """Tests for the `rating` method"""

    @patch("phylm.sources.mtc.soupify")
    def test_match(self, mock_soup, matrix_results):
        """
        Given a raw title with a match from Mtc,
        When the rating is retrieved,
        Then the rating can be returned
        """
        mock_soup.return_value = matrix_results
        mtc = Mtc("The Matrix")

        assert mtc.rating() == "73"

    @patch("phylm.sources.mtc.soupify")
    def test_no_results(self, mock_soup, no_results):
        """
        Given a raw title with no results from Mtc,
        When the rating is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        mtc = Mtc("blort")

        assert mtc.rating() is None
