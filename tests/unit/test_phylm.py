"""Tests for the `Phylm` module."""
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from phylm import Phylm
from phylm.errors import SourceNotLoadedError
from phylm.errors import UnrecognizedSourceError

MODULE_PATH = "phylm.phylm"


class AsyncMock(MagicMock):
    """Extend `MagicMock` to accept async actions."""

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Overload the `__call__` method to make it async."""
        return super().__call__(*args, **kwargs)


class TestInit:
    """Tests for the __init__ method."""

    def test_init_instance_variables(self) -> None:
        """
        Given a title,
        When a `Phylm` object is created with the title,
        Then title is added as an instance variable
        """
        title = "foo"

        phylm = Phylm(title=title)

        assert phylm.title == title

    def test_imdb_id(self) -> None:
        """
        Given an `imdb_id`,
        When a `Phylm` object is created with the id,
        Then `imdb_id` is added as an instance variable
        """
        imdb_id = "bar"

        phylm = Phylm(title="foo", imdb_id=imdb_id)

        assert phylm.imdb_id == imdb_id

    def test_tmdb_id(self) -> None:
        """TMDB id can be passed through"""
        tmdb_id = "bar"

        phylm = Phylm(title="foo", tmdb_id=tmdb_id)

        assert phylm.tmdb_id == tmdb_id


class TestRepr:
    """Tests for the __repr__ method."""

    def test_repr(self) -> None:
        """
        Given a `Phylm` object,
        When the string representation is retrieved,
        Then a informative string is returned
        """
        phylm = Phylm(title="foo")

        assert repr(phylm) == "<class 'Phylm' title:'foo'>"
        assert str(phylm) == "<class 'Phylm' title:'foo'>"


@pytest.mark.asyncio
class TestLoadSource:
    """Tests for the `load_source` method."""

    async def test_source_not_found(self) -> None:
        """
        Given an unrecognized source,
        When the `load_source` method is invoked with the source,
        Then a `UnrecognizedSource` is raised
        """
        phylm = Phylm(title="foo")

        with pytest.raises(
            UnrecognizedSourceError, match="bar is not a recognized source"
        ):
            await phylm.load_source("bar")

    async def test_recognized_source_imdb(self) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with the `imdb` source,
        Then the source is loaded
        """
        phylm = Phylm(title="bar", year=2000)
        with pytest.raises(
            SourceNotLoadedError, match="The data for Imdb has not yet been loaded"
        ):
            assert phylm.imdb is None

        with patch(f"{MODULE_PATH}.Imdb", autospec=True) as mock_imdb:
            mock_imdb.return_value.load_source = AsyncMock()
            await phylm.load_source("imdb")

            assert phylm.imdb == mock_imdb.return_value
            mock_imdb.assert_called_once_with(
                raw_title="bar", movie_id=None, raw_year=2000
            )

    async def test_recognized_source_imdb_with_movie_id(self) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with the `imdb` source
            and a `movie_id`,
        Then the source is loaded with the `movie_id`
        """
        phylm = Phylm(title="bar")

        with patch(f"{MODULE_PATH}.Imdb", autospec=True) as mock_imdb:
            mock_imdb.return_value.load_source = AsyncMock()
            await phylm.load_source("imdb", imdb_id="abc")

            assert phylm.imdb == mock_imdb.return_value
            mock_imdb.assert_called_once_with(
                raw_title="bar", movie_id="abc", raw_year=None
            )

    async def test_recognized_source_imdb_with_movie_id_instance_variable(self) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with an `imdb_id` provided at `init`,
        Then the source is loaded with the `movie_id` instance variable
        """
        phylm = Phylm(title="foo", imdb_id="abc")

        with patch(f"{MODULE_PATH}.Imdb", autospec=True) as mock_imdb:
            mock_imdb.return_value.load_source = AsyncMock()
            await phylm.load_source("imdb")

            assert phylm.imdb == mock_imdb.return_value
            mock_imdb.assert_called_once_with(
                raw_title="foo", movie_id="abc", raw_year=None
            )

    async def test_recognized_source_mtc(self) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with the `mtc` source,
        Then the source is loaded
        """
        phylm = Phylm(title="bar", year=2000)
        with pytest.raises(
            SourceNotLoadedError,
            match="The data for Metacritic has not yet been loaded",
        ):
            assert phylm.mtc is None

        with patch(f"{MODULE_PATH}.Mtc", autospec=True) as mock_mtc:
            mock_mtc.return_value.load_source = AsyncMock()
            await phylm.load_source("mtc")

            assert phylm.mtc == mock_mtc.return_value
            mock_mtc.assert_called_once_with(raw_title="bar", raw_year=2000)

    async def test_recognized_source_rt(self) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with the `rt` source,
        Then the source is loaded
        """
        phylm = Phylm(title="bar", year=2000)
        with pytest.raises(
            SourceNotLoadedError,
            match="The data for Rotten Tomatoes has not yet been loaded",
        ):
            assert phylm.rt is None

        with patch(f"{MODULE_PATH}.Rt", autospec=True) as mock_rt:
            mock_rt.return_value.load_source = AsyncMock()
            await phylm.load_source("rt")

            assert phylm.rt == mock_rt.return_value
            mock_rt.assert_called_once_with(raw_title="bar", raw_year=2000)

    async def test_recognized_source_tmdb(self) -> None:
        """Can load `tmdb` source."""
        phylm = Phylm(title="bar", year=2000)
        with pytest.raises(
            SourceNotLoadedError, match="The data for TMDB has not yet been loaded"
        ):
            assert phylm.tmdb is None

        with patch(f"{MODULE_PATH}.Tmdb", autospec=True) as mock_tmdb:
            mock_tmdb.return_value.load_source = AsyncMock()
            await phylm.load_source("tmdb")

            assert phylm.tmdb == mock_tmdb.return_value
            mock_tmdb.assert_called_once_with(
                raw_title="bar", movie_id=None, raw_year=2000
            )

    async def test_recognized_source_tmdb_with_movie_id(self) -> None:
        """Can load `tmdb` source with a `movie_id`."""
        phylm = Phylm(title="bar")

        with patch(f"{MODULE_PATH}.Tmdb", autospec=True) as mock_tmdb:
            mock_tmdb.return_value.load_source = AsyncMock()
            await phylm.load_source("tmdb", tmdb_id="abc")

            assert phylm.tmdb == mock_tmdb.return_value
            mock_tmdb.assert_called_once_with(
                raw_title="bar", movie_id="abc", raw_year=None
            )

    async def test_recognized_source_tmdb_with_movie_id_instance_variable(self) -> None:
        """Can load `tmdb` source with a `movie_id` instance variable."""
        phylm = Phylm(title="foo", tmdb_id="abc")

        with patch(f"{MODULE_PATH}.Tmdb", autospec=True) as mock_tmdb:
            mock_tmdb.return_value.load_source = AsyncMock()
            await phylm.load_source("tmdb")

            assert phylm.tmdb == mock_tmdb.return_value
            mock_tmdb.assert_called_once_with(
                raw_title="foo", movie_id="abc", raw_year=None
            )

    @pytest.mark.parametrize("source_class", ("Rt", "Mtc", "Imdb", "Tmdb"))
    async def test_source_already_loaded(self, source_class: str) -> None:
        """
        Given phylm instance with a source already loaded,
        When `load_source` is invoked with the same source,
        Then nothing happens
        """
        phylm = Phylm(title="foo")

        with patch(f"{MODULE_PATH}.{source_class}") as mock_source:
            mock_source.return_value.load_source = AsyncMock()
            source_name = source_class.lower()
            await phylm.load_source(source_name)
            await phylm.load_source(source_name)

        assert mock_source.call_count == 1

    @pytest.mark.parametrize("source_class", ("Rt", "Mtc", "Tmdb"))
    async def test_with_given_session(self, source_class: str) -> None:
        """
        Given phylm instance,
        When `load_source` is invoked with a `session`,
        Then the `session` is passed to the source `load_source` method
        """
        phylm = Phylm(title="foo")
        session = MagicMock()

        with patch(f"{MODULE_PATH}.{source_class}") as mock_source:
            mock_source.return_value.load_source = AsyncMock()
            source_name = source_class.lower()
            await phylm.load_source(source_name, session=session)

        mock_source.return_value.load_source.assert_called_once_with(session=session)


@pytest.mark.asyncio
class TestLoadSources:
    """Tests for the `load_sources` method."""

    async def test_success(self) -> None:
        """
        Given a list of sources,
        When the `load_sources` is invoked with the list,
        Then the sources are loaded
        """
        phylm = Phylm(title="foo")

        with patch(f"{MODULE_PATH}.Mtc", autospec=True) as mock_mtc, patch(
            f"{MODULE_PATH}.Rt", autospec=True
        ) as mock_rt:
            mock_mtc.return_value.load_source = AsyncMock()
            mock_rt.return_value.load_source = AsyncMock()

            await phylm.load_sources(["rt", "mtc"])

        assert phylm.rt == mock_rt.return_value
        assert phylm.mtc == mock_mtc.return_value
        with pytest.raises(SourceNotLoadedError):
            assert phylm.imdb is None

    async def test_one_source_not_recognised(self) -> None:
        """
        Given a list of sources where one is unrecognised,
        When the `load_sources` is invoked with the list,
        Then a UnrecognizedSourceError is raised
        """
        phylm = Phylm(title="foo")

        with pytest.raises(UnrecognizedSourceError), patch(
            f"{MODULE_PATH}.Rt", autospec=True
        ) as mock_rt:
            mock_rt.return_value.load_source = AsyncMock()
            await phylm.load_sources(["rt", "blort"])

        assert phylm.rt == mock_rt.return_value
