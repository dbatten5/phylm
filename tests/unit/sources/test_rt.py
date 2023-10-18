"""Tests for the Rt class."""
import pytest

from phylm.sources.rt import Rt
from tests.conftest import FIXTURES_DIR
from tests.conftest import my_vcr

VCR_FIXTURES_DIR = f"{FIXTURES_DIR}/rt"
pytestmark = pytest.mark.asyncio
my_vcr.serializer = "response_body_compressor"


class TestInit:
    """Tests for the `__init__` method."""

    def test_initial_state(self) -> None:
        """
        When the `Mtc` class is instantiated,
        Then the data is `None`
        """
        rot_tom = Rt("Alien")

        assert rot_tom.title is None

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    async def test_exact_match(self) -> None:
        """
        Given a raw title,
        When there is an exact match from Rt,
        Then the match is selected and low confidence remains False
        """
        rot_tom = Rt("The Matrix")
        await rot_tom.load_source()

        assert rot_tom.title == "The Matrix"
        assert rot_tom.low_confidence is False

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/fuzzy_matrix.yaml")
    async def test_fuzzy_exact_match(self) -> None:
        """
        Given a raw title with inconsistent case and whitespace,
        When there is an exact match from Rt,
        Then the match is selected
        """
        rot_tom = Rt("  The mAtrix  ")
        await rot_tom.load_source()

        assert rot_tom.title == "The Matrix"
        assert rot_tom.low_confidence is False

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix_low_confidence.yaml")
    async def test_no_exact_match(self) -> None:
        """
        Given a raw title,
        When there is no exact match from Rt,
        Then the first match with a tomato score is selected and low confidence is True
        """
        rot_tom = Rt("The Matrix Resuur")
        await rot_tom.load_source()

        assert rot_tom.title == "The Matrix Resurrections"
        assert rot_tom.low_confidence is True


class TestYearMatching:
    """Tests for the `init` method with a `raw_title`."""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/dune_2021.yaml")
    async def test_year_match_first_result(self) -> None:
        """
        Given a `raw_title` and `raw_year`
        When the source is instantiated
        Then the year is the preferred method of matching
        """
        rot_tom = Rt(raw_title="Dune", raw_year=2021)
        await rot_tom.load_source()

        assert rot_tom.title == "Dune"
        assert rot_tom.year == "2021"

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/dune_1984.yaml")
    async def test_year_match_not_first_result(self) -> None:
        """
        Given a `raw_title` and `raw_year`
        When the source is instantiated
        Then the year is the preferred method of matching
        """
        rot_tom = Rt(raw_title="Dune", raw_year=1984)
        await rot_tom.load_source()

        assert rot_tom.title == "Dune"
        assert rot_tom.year == "1984"


class TestTitle:
    """Tests for the `title` method"""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given a raw title with no results from rt,
        When the title is retrieved,
        Then None is returned
        """
        rot_tom = Rt("asldkjaskdnlaskdjaslkjdas")
        await rot_tom.load_source()

        assert rot_tom.title is None


class TestYear:
    """Tests for the `year` method"""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    async def test_match(self) -> None:
        """
        Given a raw title with a match from rt,
        When the year is retrieved,
        Then the year can be returned
        """
        rot_tom = Rt("The Matrix")
        await rot_tom.load_source()

        assert rot_tom.year == "1999"

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given a raw title with no results from rt,
        When the year is retrieved,
        Then None is returned
        """
        rot_tom = Rt("asldkjaskdnlaskdjaslkjdas")
        await rot_tom.load_source()

        assert rot_tom.year is None


class TestTomatoScore:
    """Tests for the `tomato_score` method"""

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/matrix.yaml")
    async def test_match(self) -> None:
        """
        Given a raw title with a match from Rt,
        When the score is retrieved,
        Then the score is returned
        """
        rot_tom = Rt("The Matrix")
        await rot_tom.load_source()

        assert rot_tom.tomato_score == "88"

    @my_vcr.use_cassette(f"{VCR_FIXTURES_DIR}/no_results.yaml")
    async def test_no_results(self) -> None:
        """
        Given a raw title with no results from Rt,
        When the score is retrieved,
        Then None is returned
        """
        rot_tom = Rt("asldkjaskdnlaskdjaslkjdas")
        await rot_tom.load_source()

        assert rot_tom.tomato_score is None
