"""Tests for the Rt class."""
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from phylm.sources.rt import Rt


@pytest.fixture(scope="module", name="matrix_results")
def matrix_results_fixture() -> BeautifulSoup:
    """Return the bs4 representation for a RT results page"""
    with open("tests/data/rt/matrix_results.html", "r", encoding="UTF-8") as results:
        return BeautifulSoup(results, "html.parser")


@pytest.fixture(scope="module", name="no_results")
def no_results_fixture() -> BeautifulSoup:
    """Return the bs4 representation for a rt no results page"""
    with open("tests/data/rt/no_results.html", "r", encoding="UTF-8") as results:
        return BeautifulSoup(results, "html.parser")


class TestInit:
    """Tests for the `__init__` method."""

    @patch("phylm.sources.rt.soupify")
    def test_exact_match(
        self, mock_soup: MagicMock, matrix_results: BeautifulSoup
    ) -> None:
        """
        Given a raw title,
        When there is an exact match from Rt,
        Then the match is selected and low confidence remains False
        """
        mock_soup.return_value = matrix_results
        rot_tom = Rt("The Matrix")

        assert rot_tom.title == "The Matrix"
        assert rot_tom.low_confidence is False

    @patch("phylm.sources.rt.soupify")
    def test_fuzzy_exact_match(
        self, mock_soup: MagicMock, matrix_results: BeautifulSoup
    ) -> None:
        """
        Given a raw title with inconsistent case and whitespace,
        When there is an exact match from Rt,
        Then the match is selected
        """
        mock_soup.return_value = matrix_results
        rot_tom = Rt("The Matrix")

        assert rot_tom.title == "The Matrix"
        assert rot_tom.low_confidence is False

    @patch("phylm.sources.rt.soupify")
    def test_no_exact_match(
        self, mock_soup: MagicMock, matrix_results: BeautifulSoup
    ) -> None:
        """
        Given a raw title,
        When there is no exact match from Rt,
        Then the first match with a tomato score is selected and low confidence is True
        """
        mock_soup.return_value = matrix_results
        rot_tom = Rt("blort")

        assert rot_tom.title == "The Matrix Resurrections"
        assert rot_tom.low_confidence is True


class TestTitle:
    """Tests for the `title` method"""

    @patch("phylm.sources.rt.soupify")
    def test_no_results(self, mock_soup: MagicMock, no_results: BeautifulSoup) -> None:
        """
        Given a raw title with no results from rt,
        When the title is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        rot_tom = Rt("blort")

        assert rot_tom.title is None


class TestYear:
    """Tests for the `year` method"""

    @patch("phylm.sources.rt.soupify")
    def test_match(self, mock_soup: MagicMock, matrix_results: BeautifulSoup) -> None:
        """
        Given a raw title with a match from rt,
        When the year is retrieved,
        Then the year can be returned
        """
        mock_soup.return_value = matrix_results
        rot_tom = Rt("The Matrix")

        assert rot_tom.year == "1999"

    @patch("phylm.sources.rt.soupify")
    def test_no_results(self, mock_soup: MagicMock, no_results: BeautifulSoup) -> None:
        """
        Given a raw title with no results from rt,
        When the year is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        rot_tom = Rt("blort")

        assert rot_tom.year is None

    @patch("phylm.sources.rt.soupify")
    def test_no_match(self, mock_soup: MagicMock, no_results: BeautifulSoup) -> None:
        """
        Given a raw title with results from Rt but no year data,
        When the year is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        rot_tom = Rt("A Glitch in the Matrix")

        assert rot_tom.low_confidence is False
        assert rot_tom.year is None


class TestTomatoScore:
    """Tests for the `tomato_score` method"""

    @patch("phylm.sources.rt.soupify")
    def test_match(self, mock_soup: MagicMock, matrix_results: BeautifulSoup) -> None:
        """
        Given a raw title with a match from Rt,
        When the score is retrieved,
        Then the score is returned
        """
        mock_soup.return_value = matrix_results
        rot_tom = Rt("The Matrix")

        assert rot_tom.tomato_score == "88"

    @patch("phylm.sources.rt.soupify")
    def test_no_results(self, mock_soup: MagicMock, no_results: BeautifulSoup) -> None:
        """
        Given a raw title with no results from Rt,
        When the score is retrieved,
        Then None is returned
        """
        mock_soup.return_value = no_results
        rot_tom = Rt("blort")

        assert rot_tom.tomato_score is None
