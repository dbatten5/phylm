"""Module to contain the `Phylm` class definition."""
from __future__ import annotations

from typing import Optional

from phylm.errors import SourceNotLoadedError
from phylm.errors import UnrecognizedSourceError
from phylm.sources.imdb import Imdb


class Phylm:
    """Main `Phylm` entrypoint."""

    def __init__(self, title: str) -> None:
        """Initialize a `Phylm` object."""
        self.title: str = title
        self._imdb: Optional[Imdb] = None

    @property
    def imdb(self) -> Optional[Imdb]:
        """Return the IMDb data.

        Returns:
            The IMDb data

        Raises:
            SourceNotLoadedError: if the source is not loaded
        """
        if self._imdb is None:
            raise SourceNotLoadedError("The data for Imdb has not yet been loaded")

        return self._imdb

    def load_source(self, source: str) -> Phylm:
        """Load the film data for a source.

        Args:
            source (str): a list of the desired sources

        Returns:
            the instance

        Raises:
            UnrecognizedSourceError: if the source is not recognized
        """
        if source == "imdb":
            self._imdb = Imdb(raw_title=self.title)
            return self

        raise UnrecognizedSourceError(f"{source} is not a recognized source")
