from universe import Universe

class Game:
    planet_names = ["Iscandar", "Xerxes", "Gamilon", "Simpkins", "YeetCode", "Collins",
                    "Apply Online", "Orbit", "Flipside", "Robert Alfred Morgan IV"]
    techLevels = ["PRE-AG", "AGRICULTURE", "MEDIEVAL", "RENAISSANCE",
                  "INDUSTRIAL", "MODERN", "FUTURISTIC"]

    def __init__(self):
        self.difficulty = ""
        self.player = ""
        self.region_list = []
        self.universe = []
        self.market = ""
        self.encounter_type = ""
        self.mechanic_price = []

        #stores potential region and fuel in the chance we need them
        self.potential_region = ""
        self.potential_fuel = ""

        self.current_npc = ""

    #absolutely brilliant.
    def reset(self):
        self.difficulty = ""
        self.player = ""
        self.region_list = []
        self.universe = []
        self.market = ""
        self.encounter_type = ""
        self.potential_region = ""
        self.potential_fuel = ""
        self.current_npc = ""

    def create_universe(self):
        if len(self.region_list) == 0:
            self.universe = Universe(Game.planet_names, Game.techLevels)
            self.region_list = self.universe.get_regionlist()

    def initialize_player(self, player):
        self.player = player

    def get_player(self):
        return self.player

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def get_difficulty(self):
        return self.difficulty

    def get_universe(self):
        return self.universe

    def get_regions(self):
        return self.region_list

    def get_techlevels(self):
        return Game.techLevels

    def get_planetnames(self):
        return Game.planet_names

    def set_market(self, market):
        self.market = market

    def get_market(self):
        return self.market

    def set_encounter_type(self, encounter_type):
        self.encounter_type = encounter_type

    def get_encounter_type(self):
        return self.encounter_type

    def init_trader(self, trader):
        self.trader = trader

    def get_trader(self):
        return self.trader

    def init_bandit(self, bandit):
        self.bandit = bandit

    def get_bandit(self):
        return self.bandit

    def store_potential_region(self, region):
        self.potential_region = region

    def get_potential_region(self):
        return self.potential_region

    def store_potential_fuel(self, fuel):
        self.potential_fuel = fuel

    def get_potential_fuel(self):
        return self.potential_fuel

    def get_npc(self):
        return self.current_npc

    def set_npc(self, npc):
        self.current_npc = npc

    def get_mechanic_prices(self):
        return self.mechanic_price
    
    def set_mechanic_prices(self, mechanic_price):
        self.mechanic_price = mechanic_price
