import UsageStatsLookup as StatsSearch
import IndividualLookup as IndividualSearch
from SQLInterface import SQLInterface


class Updater:

    @staticmethod
    def set_query(param_dict: dict) -> StatsSearch.BaseStatsSearch:

        match param_dict['branch']:
            case 'BaseStats':
                new_query = StatsSearch.BaseStatsSearch(
                    year=param_dict['year'],
                    month=param_dict['month'],
                    gen=param_dict['gen'],
                    tier=param_dict['branch_param']
                )
                return new_query
            case 'MonoStats':
                new_query = StatsSearch.MonotypeStatsSearch(
                    year=param_dict['year'],
                    month=param_dict['month'],
                    gen=param_dict['gen'],
                    typing=param_dict['branch_param']
                )
            case 'BaseChaos':
                new_query = IndividualSearch.BaseChaosSearch(
                    year=param_dict['year'],
                    month=param_dict['month'],
                    gen=param_dict['gen'],
                    tier=param_dict['branch_param']
                )
            case 'MonoChaos':
                new_query = IndividualSearch.MonotypeChaosSearch(
                    year=param_dict['year'],
                    month=param_dict['month'],
                    gen=param_dict['gen'],
                    typing=param_dict['branch_param']
                )
        return new_query
    
    @staticmethod
    def search_and_save(query: StatsSearch.BaseStatsSearch, target_table: str):
        query.search_and_save(pathname=target_table)
        return print("Successfully saved file.")

    @staticmethod
    def update_database():
        sqli = SQLInterface()
        sqli.connect()
        sqli.update_tables()
        for i in ('current', 'previous', 'tma'):
            sqli.load_data_to_table(i)

        sqli.close_connection()
        return print("Database successfully updated.")