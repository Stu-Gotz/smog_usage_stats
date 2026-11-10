class InvalidFormatError(ValueError):
    """The year/month/gen/tier combination can't exist on Smogon."""


class QueryError(Exception):
    """Smogon couldn't be reached, or returned an error page."""


class PageNotFound(Exception):
    """The request was valid, but Smogon has no matching file or Pokemon."""
