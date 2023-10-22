from datetime import datetime


class Validations:
    def __init__(self, validation_object: dict) -> None:
        self.validation_object = validation_object

    def validate(self) -> bool:
        '''
        Runs the validation checks, if any of them return False, this also returns False.
        '''
        if not (self._is_correct_gen(self.validation_object)) or not (
            self._is_valid_date(self.validation_object)
        ):
            return False
        else:
            return True

    @staticmethod
    def is_modern_format(validation_object: dict) -> bool:
        '''Checks if the date submitted uses the old non-standardized labeling or not. Anything before Jul 2017 uses non-standard.'''
        if (int(validation_object["date"].year) == 2017) and (
            validation_object["date"].month <= 6
        ):
            return False
        elif int(validation_object["date"].year) < 2017:
            return False
        return True

    @staticmethod
    def _is_correct_gen(validation_object: dict) -> bool:
        '''Checks if the generation is valid for the date submitted.'''
        cutoff_dates = {
            7: datetime.strptime("2016-11", "%Y-%m"),
            8: datetime.strptime("2020-11", "%Y-%m"),
            9: datetime.strptime("2022-11", "%Y-%m"),
        }
        # something like having an object of dates this is where it makes sense to
        # have dt objects rather than strings
        # if they fail, return false. good case for switch statements

        if validation_object["gen"] <= 6:
            return True
        elif (validation_object["gen"] > 6) and (
            validation_object["date"].date()
            < cutoff_dates[validation_object["gen"]].date()
        ):
            return False

    @staticmethod
    def _is_valid_date(validation_object: dict) -> bool:
        '''Makes sure theres no date submitted before Nov 2014, as there is no data available before then.'''
        year = validation_object["date"].year
        month = validation_object["date"].month

        if year < 2014:
            return False
        elif (year == 2014) and (month != (11 | 12)):
            return False
        else:
            return True
