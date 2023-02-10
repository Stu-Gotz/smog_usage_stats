class TypeChart():
    def typechart(self):
        return [
            {"bug":{"weakness":["fire","fighting","poison","flying","ghost","steel","fairy"], "strength":["grass", "psychic", "dark"]}},
            {"dark":{"weakness":["fighting", "bug","fairy"], "strength":["ghost", "psychic"]}},
            {"dragon":{"weakness":[], "strength":[]}},
            "electric",
            "fairy",
            "fighting",
            "fire",
            "flying",
            "ghost",
            "grass",
            "ground",
            "ice",
            "normal",
            "poison",
            "psychic",
            "rock",
            "steel",
            "water"
        ]
    
    # def immune_abilities(self):
    #     return ['dry skin','flash fire','levitate','lightningrod','sap sipper',
    #             'motor drive','storm drain','water absorb','wonder guard']
    
    # def immune_ability_matchup(self):
    #     return {
    #         'dry skin':'water', 
    #         'flash fire':'fire',
    #         'levitate':'ground', 
    #         'lightningrod':'electric',
    #         'sap sipper':'grass', 
    #         'motor drive':'electric', 
    #         'storm drain':'water', 
    #         'water absorb':'water',
    #         'wonder guard':""
    #       }
    
    # def damage_abilities(self):
    #     return {}