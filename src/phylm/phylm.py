"""Module to contain the `Phylm` class definition."""
import asyncio
from typing import List
from typing import Optional

from aiohttp import ClientSession

from phylm.errors import SourceNotLoadedError
from phylm.errors import UnrecognizedSourceError
from phylm.sources import Imdb
from phylm.sources import Mtc
from phylm.sources import Rt


class Phylm:
    """Main `Phylm` entrypoint."""

    def __init__(
        self,
        title: str,
        imdb_id: Optional[str] = None,
        year: Optional[int] = None,
    ) -> None:
        """Initialize a `Phylm` object.

        Args:
            title: the title of the movie
            imdb_id: an optional `IMDb` ID of the movie
            year: an optional year of the movie
        """
        self.title = title
        self.imdb_id = imdb_id
        self.year = year
        self._imdb: Optional[Imdb] = None
        self._mtc: Optional[Mtc] = None
        self._rt: Optional[Rt] = None

    def __repr__(self) -> str:
        """Return the string representation.

        Returns:
            the string representation
        """
        return f"<class '{self.__class__.__name__}' title:'{self.title}'>"

    def __str__(self) -> str:
        """Return the string representation."""
        return self.__repr__()

    @property
    def imdb(self) -> Imdb:
        """Return the IMDb data.

        Returns:
            The IMDb data

        Raises:
            SourceNotLoadedError: if the source is not loaded
        """
        if self._imdb is None:
            raise SourceNotLoadedError("The data for Imdb has not yet been loaded")

        return self._imdb

    @property
    def mtc(self) -> Mtc:
        """Return the Metacritic data.

        Returns:
            The Metacritic data

        Raises:
            SourceNotLoadedError: if the source is not loaded
        """
        if self._mtc is None:
            raise SourceNotLoadedError(
                "The data for Metacritic has not yet been loaded"
            )

        return self._mtc

    @property
    def rt(self) -> Rt:
        """Return the Rotten Tomatoes data.

        Returns:
            The Rotten Tomatoes data

        Raises:
            SourceNotLoadedError: if the source is not loaded
        """
        if self._rt is None:
            raise SourceNotLoadedError(
                "The data for Rotten Tomatoes has not yet been loaded"
            )

        return self._rt

    async def load_source(
        self,
        source: str,
        imdb_id: Optional[str] = None,
        session: Optional[ClientSession] = None,
    ) -> "Phylm":
        """Asynchronously load the film data for a source.

        Args:
            source: the desired source
            imdb_id: an optional `IMDb` id which will be used to load the imdb data
                instead of a basic search on the title
            session: an optional instance of `aiohttp.ClientSession` in which to run the
                request

        Returns:
            the instance

        Raises:
            UnrecognizedSourceError: if the source is not recognized
        """
        if source == "imdb":
            if not self._imdb:
                movie_id = imdb_id or self.imdb_id
                self._imdb = Imdb(
                    raw_title=self.title,
                    movie_id=movie_id,
                    raw_year=self.year,
                )
                await self._imdb.load_source()
            return self

        if source == "mtc":
            if not self._mtc:
                self._mtc = Mtc(raw_title=self.title, raw_year=self.year)
                await self._mtc.load_source(session=session)
            return self

        if source == "rt":
            if not self._rt:
                self._rt = Rt(raw_title=self.title, raw_year=self.year)
                await self._rt.load_source(session=session)
            return self

        raise UnrecognizedSourceError(f"{source} is not a recognized source")

    async def load_sources(
        self,
        sources: List[str],
    ) -> "Phylm":
        """Asynchronously load multiple sources.

        Args:
            sources: a list of the desired sources

        Returns:
            the instance
        """
        session = ClientSession()

        try:
            await asyncio.gather(
                *[self.load_source(source, session=session) for source in sources]
            )
        finally:
            await session.close()

        return self
