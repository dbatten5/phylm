"""Module to hold fixtures etc. for pytest."""
import pytest
from bs4 import BeautifulSoup


@pytest.fixture(scope="module")
def matrix_results() -> BeautifulSoup:
    """Return the bs4 representation for a Mtc results page"""
    with open("tests/data/mtc/matrix_results.html", "r", encoding="UTF-8") as results:
        return BeautifulSoup(results, "html.parser")


@pytest.fixture(scope="module")
def no_results() -> BeautifulSoup:
    """Return the bs4 representation for a Mtc no results page"""
    with open("tests/data/mtc/no_results.html", "r", encoding="UTF-8") as results:
        return BeautifulSoup(results, "html.parser")
