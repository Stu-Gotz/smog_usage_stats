from datetime import datetime

types = [
    "normal",
    " fire",
    " water",
    " grass",
    " flying",
    " fighting",
    " poison",
    " electric",
    " ground",
    " rock",
    " psychic",
    " ice",
    " bug",
    " ghost",
    " steel",
    " dragon",
    " dark",
    " fairy",
]


class Validations:
    def __init__(self, validation_object: dict) -> None:
        self.validation_object = validation_object

    def validate(self, isMonotype: bool = False) -> bool:
        """
        Runs the validation checks, if any of them return False, this also returns False.
        """
        if isMonotype:
            if self.typing not in types:
                return False
            if not (self._is_valid_date(self.validation_object)):
                return False
        else:
            if not (self._is_correct_gen(self.validation_object)):
                print("Generation choice is invalid")
                return False
            if not (self._is_valid_date(self.validation_object)):
                print("Date and generation combination is invalid.")
                return False
        return True

    @staticmethod
    def is_modern_format(validation_object: dict) -> bool:
        """Checks if the date submitted uses the old non-standardized labeling or not. Anything before Jul 2017 uses non-standard."""
        if (int(validation_object["date"].year) == 2017) and (
            int(validation_object["date"].month) <= 6
        ):
            return False
        elif int(validation_object["date"].year) < 2017:
            return False
        return True

    @staticmethod
    def _is_correct_gen(validation_object: dict) -> bool:
        """Checks if the generation is valid for the date submitted."""
        cutoff_dates = {
            "7": datetime.strptime("2016-11", "%Y-%m"),
            "8": datetime.strptime("2020-11", "%Y-%m"),
            "9": datetime.strptime("2022-11", "%Y-%m"),
        }
        # something like having an object of dates this is where it makes sense to
        # have dt objects rather than strings
        # if they fail, return false.

        if int(validation_object["gen"]) <= 6:
            return True
        elif (int(validation_object["gen"]) > 6) and (
            validation_object["date"] < cutoff_dates[str(validation_object["gen"])]
        ):
            return False
        else:
            return True

    @staticmethod
    def _is_valid_date(validation_object: dict) -> bool:
        """Makes sure theres no date submitted before Nov 2014, as there is no data available before then."""
        year = int(validation_object["date"].year)
        month = int(validation_object["date"].month)

        if year < 2014:
            return False
        elif year == 2014:
            if month != (11 | 12):
                return False
        else:
            return True
