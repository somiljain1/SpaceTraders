class Ship:
    def __init__(self, ship_type):
        self.ship_type = ship_type.strip()

        if ship_type == 'Jet':
            self.max_cargo = 50
            self.max_fuel = 50
            self.max_health = 100
        elif ship_type == 'Starship':
            self.max_cargo = 60
            self.max_fuel = 70
            self.max_health = 70
        elif ship_type == 'Cargo Plane':
            self.max_cargo = 100
            self.max_fuel = 50
            self.max_health = 50
        elif ship_type == 'Lady Bug':
            self.max_cargo = 30
            self.max_fuel = 140
            self.max_health = 30
        elif ship_type == 'Yellow Jacket':
            self.max_cargo = 30
            self.max_fuel = 50
            self.max_health = 120

        self.cargo = self.max_cargo #denotes cargo remaining
        self.fuel = self.max_fuel
        self.health = self.max_health

    def get_ship_type(self):
        return self.ship_type

    def get_cargo(self):
        return self.cargo

    def set_cargo(self, cargo):
        self.cargo = cargo

    def get_fuel(self):
        return int(self.fuel) 

    def set_fuel(self, newfuel):
        self.fuel = newfuel

    def get_health(self):
        return self.health

    def set_health(self, new_health):
        self.health = new_health

    def __str__(self):
        return "Your ship is a " + self.ship_type

    def intojsonform(self):
        json = {
            "Fuel": self.fuel,
            "ShipType": self.ship_type,
            "Cargo": self.cargo,
            "Health": self.health
        }
        return json
