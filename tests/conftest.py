"""Module to hold fixtures etc. for pytest."""
from typing import AsyncGenerator

import pytest
import vcr
from aiohttp import ClientSession
from tests.utils.vcr_serializers import ResponseBodyCompressor

my_vcr = vcr.VCR()
my_vcr.register_serializer("response_body_compressor", ResponseBodyCompressor())


@pytest.fixture(name="my_vcr")
def my_vcr_fixture() -> vcr.VCR:
    """Return the custom instantiation of vcr.VCR."""
    return my_vcr


@pytest.fixture(name="async_session")
async def async_session() -> AsyncGenerator[ClientSession, None]:
    """Return a client session and close the session after tests."""
    session = ClientSession()
    yield session
    await session.close()


FIXTURES_DIR = "tests/fixtures/vcr_cassettes"
