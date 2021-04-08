"""Module for Mtc source tests"""

from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from phylm.sources.mtc import Mtc


@pytest.fixture(scope="module")
def matrix_results():
    """Return the bs4 representation for a Mtc results page"""
    with open('tests/data/mtc/matrix_results.html', 'r') as results:
        return BeautifulSoup(results, 'html.parser')


@pytest.fixture(scope="module")
def no_results():
    """Return the bs4 representation for a Mtc no results page"""
    with open('tests/data/mtc/no_results.html', 'r') as results:
        return BeautifulSoup(results, 'html.parser')


def test_exact_match(matrix_results):
    """
    Given a raw title,
    When there is an exact match from Mtc,
    Then the match is selected and low confidence remains False
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = matrix_results
        mtc = Mtc('The Matrix')
    assert mtc.title() == 'The Matrix'
    assert mtc.low_confidence is False


def test_exact_match_ignoring_case_and_spaces(matrix_results):
    """
    Given a raw title,
    When there is an exact match from Mtc,
    Then the match is selected and low confidence remains False
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = matrix_results
        mtc = Mtc(' the matrix ')
    assert mtc.title() == 'The Matrix'
    assert mtc.low_confidence is False


def test_no_exact_match(matrix_results):
    """
    Given a raw title,
    When there is no exact match from Mtc,
    Then the first match is selected and low confidence is True
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = matrix_results
        mtc = Mtc('blort')
    assert mtc.title() == 'The Matrix'
    assert mtc.low_confidence is True


def test_title_no_results(no_results):
    """
    Given a raw title with no results from Mtc,
    When the title is retrieved,
    Then None is returned
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = no_results
        mtc = Mtc('blort')
    assert mtc.title() is None


def test_year(matrix_results):
    """
    Given a raw title with a match from Mtc,
    When the year is retrieved,
    Then the year can be returned
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = matrix_results
        mtc = Mtc('The Matrix')
    assert mtc.year() == 1999


def test_no_results_year(no_results):
    """
    Given a raw title with no results from Mtc,
    When the year is retrieved,
    Then None is returned
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = no_results
        mtc = Mtc('blort')
    assert mtc.year() is None


def test_results_no_year(no_results):
    """
    Given a raw title with results from Mtc but no year data,
    When the year is retrieved,
    Then None is returned
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = no_results
        mtc = Mtc('A Glitch in the Matrix')
    assert mtc.low_confidence is False
    assert mtc.year() is None


def test_score(matrix_results):
    """
    Given a raw title with a match from Mtc,
    When the score is retrieved,
    Then the score can be returned
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = matrix_results
        mtc = Mtc('The Matrix')
    assert mtc.score() == '73'


def test_no_results_score(no_results):
    """
    Given a raw title with no results from Mtc,
    When the score is retrieved,
    Then None is returned
    """
    with patch('phylm.sources.mtc.soupify') as mock_soup:
        mock_soup.return_value = no_results
        mtc = Mtc('blort')
    assert mtc.score() is None
