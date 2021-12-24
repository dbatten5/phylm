"""Tests for the Mtc class."""
import pytest
import vcr
from tests.conftest import FIXTURES_DIR

from phylm.sources.mtc import Mtc

VCR_FIXTURES_DIR = f"{FIXTURES_DIR}/mtc"


class TestInit:
    """Tests for the `__init__` method."""

    def test_initial_state(self) -> None:
        """
        When the `Mtc` class is instantiated,
        Then the data is `None`
        """
        mtc = Mtc("Alien")

        assert mtc.title is None

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    def test_exact_match(self) -> None:
        """
        Given a raw title,
        When there is an exact match from Mtc,
        Then the match is selected and low confidence remains False
        """
        mtc = Mtc("The Matrix")
        mtc.load_data()

        assert mtc.title == "The Matrix"
        assert mtc.low_confidence is False

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/fuzzy_matrix.yaml")
    def test_exact_match_ignoring_case_and_spaces(self) -> None:
        """
        Given a raw title with inconsistent case and whitespace,
        When there is an exact match from Mtc,
        Then the match is selected and low confidence remains False
        """
        mtc = Mtc(" the mAtrix ")
        mtc.load_data()

        assert mtc.title == "The Matrix"
        assert mtc.low_confidence is False

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix_low_confidence.yaml")
    def test_no_exact_match(self) -> None:
        """
        Given a raw title,
        When there is no exact match from Mtc,
        Then the first match is selected and low confidence is True
        """
        mtc = Mtc("The Martix")
        mtc.load_data()

        assert mtc.title == "The Matrix"
        assert mtc.low_confidence is True


class TestYearMatching:
    """Tests for the `init` method with a `raw_title`."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/dune_2021.yaml")
    def test_year_match_first_result(self) -> None:
        """
        Given a `raw_title` and `raw_year`
        When the source is instantiated
        Then the year is the preferred method of matching
        """
        mtc = Mtc(raw_title="Dune", raw_year=2021)
        mtc.load_data()

        assert mtc.title == "Dune: Part One"
        assert mtc.year == 2021

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/dune_1984.yaml")
    def test_year_match_not_first_result(self) -> None:
        """
        Given a `raw_title` and `raw_year`
        When the source is instantiated
        Then the year is the preferred method of matching
        """
        mtc = Mtc(raw_title="Dune", raw_year=1984)
        mtc.load_data()

        assert mtc.title == "Dune"
        assert mtc.year == 1984


class TestTitle:
    """Tests for the `title` method"""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    def test_no_results(self) -> None:
        """
        Given a raw title with no results from Mtc,
        When the title is retrieved,
        Then None is returned
        """
        mtc = Mtc("asldkjaskdnlaskdjaslkjdas")
        mtc.load_data()

        assert mtc.title is None


class TestYear:
    """Tests for the `year` method"""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    def test_match(self) -> None:
        """
        Given a raw title with a match from Mtc,
        When the year is retrieved,
        Then the year can be returned
        """
        mtc = Mtc("The Matrix")
        mtc.load_data()

        assert mtc.year == 1999

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    def test_no_results(self) -> None:
        """
        Given a raw title with no results from Mtc,
        When the year is retrieved,
        Then None is returned
        """
        mtc = Mtc("asldkjaskdnlaskdjaslkjdas")
        mtc.load_data()

        assert mtc.year is None

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_year.yaml")
    def test_no_match(self) -> None:
        """
        Given a raw title with results from Mtc but no year data,
        When the year is retrieved,
        Then None is returned
        """
        mtc = Mtc("Inu-oh")
        mtc.load_data()

        assert mtc.low_confidence is False
        assert mtc.year is None


class TestRating:
    """Tests for the `rating` method"""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    def test_match(self) -> None:
        """
        Given a raw title with a match from Mtc,
        When the rating is retrieved,
        Then the rating can be returned
        """
        mtc = Mtc("The Matrix")
        mtc.load_data()

        assert mtc.rating == "73"

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    def test_no_results(self) -> None:
        """
        Given a raw title with no results from Mtc,
        When the rating is retrieved,
        Then None is returned
        """
        mtc = Mtc("asldkjaskdnlaskdjaslkjdas")
        mtc.load_data()

        assert mtc.rating is None


@pytest.mark.asyncio
class TestAsyncLoadData:
    """Tests for the `async_load_data` method."""

    @vcr.use_cassette(f"{VCR_FIXTURES_DIR}/async_matrix.yaml")
    async def test_success(self) -> None:
        """
        Given a raw title with exact match,
        When the `async_load_data` method is invoked,
        Then the match is selected asynchronously
        """
        mtc = Mtc("The Matrix")
        await mtc.async_load_data()

        assert mtc.title == "The Matrix"
