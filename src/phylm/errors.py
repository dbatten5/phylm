"""Module to hold custom error definitions."""


class UnrecognizedSourceError(Exception):
    """Raised when an unrecognized source is given."""


class SourceNotLoadedError(Exception):
    """Raised when data from an unloaded source is retreived."""
