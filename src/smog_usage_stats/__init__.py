from .api import (
    extended_stats,
    chaos_url,
    single_stats,
    usage_stats,
    usage_url,
)
from .errors import QueryError, InvalidFormatError, PageNotFound
from .metagame import Metagame
from .transformer import Usage
from .compat import (
    BaseStatsSearch,
    BaseChaosSearch,
    MonotypeStatsSearch,
    MonotypeChaosSearch,
    StatsSearch,
)

__version__ = "2.0.0"
__author__ = "Alan Nardo"
__app_name__ = "smog_usage_stats"


__all__ = [
    "Metagame",
    "Usage",
    "usage_stats",
    "single_stats",
    "extended_stats",
    "usage_url",
    "chaos_url",
    "InvalidFormatError",
    "QueryError",
    "PageNotFound",
    "BaseStatsSearch",
    "BaseChaosSearch",
    "MonotypeStatsSearch",
    "MonotypeChaosSearch",
    "StatsSearch",
]
