"""Module to hold custom error definitions."""


class UnrecognizedSourceError(Exception):
    """Raised when an unrecognized source is given."""


class SourceNotLoadedError(Exception):
    """Raised when data from an unloaded source is retreived."""


class NoTMDbApiKeyError(Exception):
    """Raised when requests are made to TMDb but no api_key has be provided."""
