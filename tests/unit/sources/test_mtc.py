"""Tests for the Mtc class."""
import pytest
from tests.conftest import FIXTURES_DIR
from tests.conftest import my_vcr

from phylm.sources.mtc import Mtc

VCR_FIXTURES_DIR = f"{FIXTURES_DIR}/mtc"
pytestmark = pytest.mark.asyncio
my_vcr.serializer = "response_body_compressor"


class TestInit:
    """Tests for the `__init__` method."""

    def test_initial_state(self) -> None:
        """
        When the `Mtc` class is instantiated,
        Then the data is `None`
        """
        mtc = Mtc("Alien")

        assert mtc.title is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    async def test_exact_match(self) -> None:
        """
        Given a raw title,
        When there is an exact match from Mtc,
        Then the match is selected and low confidence remains False
        """
        mtc = Mtc("The Matrix")
        await mtc.load_source()

        assert mtc.title == "The Matrix"
        assert mtc.low_confidence is False

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/fuzzy_matrix.yaml")
    async def test_exact_match_ignoring_case_and_spaces(self) -> None:
        """
        Given a raw title with inconsistent case and whitespace,
        When there is an exact match from Mtc,
        Then the match is selected and low confidence remains False
        """
        mtc = Mtc(" the mAtrix ")
        await mtc.load_source()

        assert mtc.title == "The Matrix"
        assert mtc.low_confidence is False

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix_low_confidence.yaml")
    async def test_no_exact_match(self) -> None:
        """
        Given a raw title,
        When there is no exact match from Mtc,
        Then the first match is selected and low confidence is True
        """
        mtc = Mtc("The Martix")
        await mtc.load_source()

        assert mtc.title == "The Matrix"
        assert mtc.low_confidence is True


class TestYearMatching:
    """Tests for the `init` method with a `raw_title`."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/dune_2021.yaml")
    async def test_year_match_first_result(self) -> None:
        """
        Given a `raw_title` and `raw_year`
        When the source is instantiated
        Then the year is the preferred method of matching
        """
        mtc = Mtc(raw_title="Dune", raw_year=2021)
        await mtc.load_source()

        assert mtc.title == "Dune: Part One"
        assert mtc.year == 2021

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/dune_1984.yaml")
    async def test_year_match_not_first_result(self) -> None:
        """
        Given a `raw_title` and `raw_year`
        When the source is instantiated
        Then the year is the preferred method of matching
        """
        mtc = Mtc(raw_title="Dune", raw_year=1984)
        await mtc.load_source()

        assert mtc.title == "Dune"
        assert mtc.year == 1984


class TestTitle:
    """Tests for the `title` method"""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given a raw title with no results from Mtc,
        When the title is retrieved,
        Then None is returned
        """
        mtc = Mtc("asldkjaskdnlaskdjaslkjdas")
        await mtc.load_source()

        assert mtc.title is None


class TestYear:
    """Tests for the `year` method"""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    async def test_match(self) -> None:
        """
        Given a raw title with a match from Mtc,
        When the year is retrieved,
        Then the year can be returned
        """
        mtc = Mtc("The Matrix")
        await mtc.load_source()

        assert mtc.year == 1999

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given a raw title with no results from Mtc,
        When the year is retrieved,
        Then None is returned
        """
        mtc = Mtc("asldkjaskdnlaskdjaslkjdas")
        await mtc.load_source()

        assert mtc.year is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_year.yaml")
    async def test_no_match(self) -> None:
        """
        Given a raw title with results from Mtc but no year data,
        When the year is retrieved,
        Then None is returned
        """
        mtc = Mtc("Inu-oh")
        await mtc.load_source()

        assert mtc.low_confidence is False
        assert mtc.year is None


class TestRating:
    """Tests for the `rating` method"""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    async def test_match(self) -> None:
        """
        Given a raw title with a match from Mtc,
        When the rating is retrieved,
        Then the rating can be returned
        """
        mtc = Mtc("The Matrix")
        await mtc.load_source()

        assert mtc.rating == "73"

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given a raw title with no results from Mtc,
        When the rating is retrieved,
        Then None is returned
        """
        mtc = Mtc("asldkjaskdnlaskdjaslkjdas")
        await mtc.load_source()

        assert mtc.rating is None
