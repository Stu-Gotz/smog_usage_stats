import sys
import os

# import smog_usage_stats.Search as Search
# import smog_usage_stats.Validation as Validation
# import smog_usage_stats.UsageStatsLookup as UsageStatsLookup
# import smog_usage_stats.IndividualLookup as IndividualLookup

# from smog_usage_stats.Search import Search
# from smog_usage_stats.UsageStatsLookup import StatsSearch, BaseStatsSearch, MonotypeStatsSearch
# from smog_usage_stats.IndividualLookup import ChaosSearch, BaseChaosSearch, MonotypeChaosSearch, IndividualStatsSearch
# from smog_usage_stats.Validation import Validations
# from smog_usage_stats.Update import Updater
# from smog_usage_stats.SQLInterface import SQLInterface

__version__ = "1.0.5"
__author__ = "Alan Nardo"

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to sys.path
sys.path.append(parent_dir)
