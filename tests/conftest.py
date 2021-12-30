"""Module to hold fixtures etc. for pytest."""
import pytest
import vcr
from tests.utils.vcr_serializers import ResponseBodyCompressor

my_vcr = vcr.VCR()
my_vcr.register_serializer("response_body_compressor", ResponseBodyCompressor())


@pytest.fixture(name="my_vcr")
def my_vcr_fixture() -> vcr.VCR:
    """Return the custom instantiation of vcr.VCR."""
    return my_vcr


FIXTURES_DIR = "tests/fixtures/vcr_cassettes"
