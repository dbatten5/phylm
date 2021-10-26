"""Tests for the `Phylm` module."""
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
    def test_recognized_source(self, mock_imdb) -> None:
        """
        Given a `Phylm` instance,
        When the `load_source` method is invoked with a recognized source name,
        Then the source is loaded
        """
        phylm = Phylm(title="bar")
        with pytest.raises(
            SourceNotLoadedError, match="The data for Imdb has not been loaded"
        ):
            assert phylm.imdb is None

        phylm.load_source("imdb")

        assert phylm.imdb == mock_imdb.return_value
        mock_imdb.assert_called_once_with(raw_title="bar")
