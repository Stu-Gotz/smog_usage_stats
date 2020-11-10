import requests

GENS = ['gen8', 'gen7', 'gen6', 'gen5', 'gen4', 'gen3', 'gen2', 'gen1']


class Lookup:

    def __init__(self):

        self.source_data = {}

        self._abilities_src = None
        self._spreads_src = None
        self._moves_src = None
        self._teammates_src = None
        self._checks_src = None

        self.__abilities()
        self.

    def search(self, gen, tier, mon):
        if gen not in GENS:
            raise ValueError("Please enter a valid gen, ex: (gen4).")

        base = "https://smogon-usage-stats.herokuapp.com/"
        base += gen+tier+'/'+mon

        result = requests.get(base)
        result = result.json()
        if len(result.keys()) < 11:
            raise ValueError("Incorrect input. Perhaps your pokemon or tier "
                             "is invalid?")
        else:
            self.source_data.update(result)
            self._abilities_src = self.source_data['abilities']
            self._spreads_src =  self.source_data['spreads']
            self._moves_src = self.source_data['moves']
            self._teammates_src = self.source_data['teammates']
            self._checks_src = self.source_data['checks']

    def __abilities(self):
        #returns tuple of tuples of abilities and their corresponding usage

        abilities_used = tuple(self._abilities.keys())
        abilities_used_pct = tuple(self._abilities.values())
        return tuple([abilities_used, abilities_used_pct])

    def __spreads(self):
        #blank lists to fill with keys, values and subvalues
        nature_used = []
        spreads_used = []
        spreads_used_pct = []

        for key, value in self._spreads.items():
            if type(value) is dict:
                for k,v in value.items():
                    nature_used.append(key)
                    spreads_used.append(k)
                    spreads_used_pct.append(v)
            else:
                nature_used.append(key)
                spreads_used_pct.append(value)

        #convert to tuples to prevent meddling
        nature_used=tuple(nature_used)
        spreads_used=tuple(spreads_used)
        spreads_used_pct=tuple(spreads_used_pct)

        return tuple([nature_used,spreads_used,spreads_used_pct])

    def __moves(self):

        moves_used = tuple(self._moves.keys())
        moves_used_pct = tuple(self._moves.values())

        return tuple([moves_used, moves_used_pct])

    def __teammates(self):

        teammates_used = tuple(self._teammates.keys())
        teammates_used_pct = tuple(self._teammates.values())

        return tuple([teammates_used, teammates_used_pct])

    def __checks(self):

        checks_used = []
        checks_used_pct = []

        for key, value in self._checks.items():
            if type(value) is dict:
                for k, v in value.items():
                    checks_used.append(tuple([key,k]))
                    checks_used_pct.append(v)
            else:
                checks_used.append(key)
                checks_used_pct.append(value)
        checks_used = tuple(checks_used)
        checks_used_pct = tuple(checks_used_pct)

        return tuple([checks_used,checks_used_pct])

        # valid data has 11 keys, use to deconflict "bad" queries (i.e.
        # charizard lc usage stats)

        # for k, v in source_data.items():
        #     if k == 'abilities':
        #         for key, value in v.items():
        #             self.abilities.update(v)


if __name__ == '__main__':

    l = Lookup()
    l.search('gen8','ou','clefable')

    abilities_ = l.abilities()
    print(abilities_)
    spreads_=l.spreads()
    print(spreads_)
    moves_ = l.moves()
    print(moves_)
    teammates_ = l.teammates()
    print(teammates_)
    checks_ = l.checks()
    print(checks_)