from typing import Literal


class Search:
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        self.year = year
        self.month = month
        self.gen = gen

    @property
    def year(self) -> str | int:
        return self._years

    @property
    def month(self) -> str:
        return self._months

    @property
    def gen(self) -> str | int:
        return self._gens

    @year.setter
    def year(self, value):
        self._years = value

    @month.setter
    def month(self, value):
        self._months = value

    @gen.setter
    def gen(self, value):
        self._gens = value