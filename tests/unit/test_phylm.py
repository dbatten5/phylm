"""Tests for the `Phylm` module."""
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from phylm import Phylm
from phylm.errors import SourceNotLoadedError
from phylm.errors import UnrecognizedSourceError


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


class TestLoadSource:
    """Tests for the `load_source` method."""

    def test_source_not_found(self) -> None:
        """
        Given an unrecognized source,
        When the `load_source` method is invoked with the source,
        Then a `UnrecognizedSource` is raised
        """
        phylm = Phylm(title="foo")

        with pytest.raises(
            UnrecognizedSourceError, match="bar is not a recognized source"
        ):
            phylm.load_source("bar")

    @patch("phylm.phylm.Imdb", autospec=True)
    def test_recognized_source_imdb(self, mock_imdb: MagicMock) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with the `imdb` source,
        Then the source is loaded
        """
        phylm = Phylm(title="bar")
        with pytest.raises(
            SourceNotLoadedError, match="The data for Imdb has not yet been loaded"
        ):
            assert phylm.imdb is None

        phylm.load_source("imdb")

        assert phylm.imdb == mock_imdb.return_value
        mock_imdb.assert_called_once_with(raw_title="bar")

    @patch("phylm.phylm.Mtc", autospec=True)
    def test_recognized_source_mtc(self, mock_mtc: MagicMock) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with the `mtc` source,
        Then the source is loaded
        """
        phylm = Phylm(title="bar")
        with pytest.raises(
            SourceNotLoadedError,
            match="The data for Metacritic has not yet been loaded",
        ):
            assert phylm.mtc is None

        phylm.load_source("mtc")

        assert phylm.mtc == mock_mtc.return_value
        mock_mtc.assert_called_once_with(raw_title="bar")

    @patch("phylm.phylm.Rt", autospec=True)
    def test_recognized_source_rt(self, mock_rt: MagicMock) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with the `rt` source,
        Then the source is loaded
        """
        phylm = Phylm(title="bar")
        with pytest.raises(
            SourceNotLoadedError,
            match="The data for Rotten Tomatoes has not yet been loaded",
        ):
            assert phylm.rt is None

        phylm.load_source("rt")

        assert phylm.rt == mock_rt.return_value
        mock_rt.assert_called_once_with(raw_title="bar")


class TestLoadSources:
    """Tests for the `load_sources` method."""

    @patch("phylm.phylm.Mtc", autospec=True)
    @patch("phylm.phylm.Rt", autospec=True)
    def test_success(self, mock_rt: MagicMock, mock_mtc: MagicMock) -> None:
        """
        Given a list of sources,
        When the `load_sources` is invoked with the list,
        Then the sources are loaded
        """
        phylm = Phylm(title="foo")

        phylm.load_sources(["rt", "mtc"])

        assert phylm.rt == mock_rt.return_value
        assert phylm.mtc == mock_mtc.return_value
        with pytest.raises(SourceNotLoadedError):
            assert phylm.imdb is None

    @patch("phylm.phylm.Rt", autospec=True)
    def test_one_source_not_recognised(self, mock_rt: MagicMock) -> None:
        """
        Given a list of sources where one is unrecognised,
        When the `load_sources` is invoked with the list,
        Then a UnrecognizedSourceError is raised
        """
        phylm = Phylm(title="foo")

        with pytest.raises(UnrecognizedSourceError):
            phylm.load_sources(["rt", "blort"])

        assert phylm.rt == mock_rt.return_value
