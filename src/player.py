class Player:
    def __init__(self, name, pilotSkills, fighterSkills, merchantSkills,
                 engineerSkills, skillLevel, ship):
        self.name = name
        self.pilot_skills = int(pilotSkills)
        self.fighter_skills = int(fighterSkills)
        self.merchant_skills = int(merchantSkills)
        self.engineer_skills = int(engineerSkills)
        self.skill_level = skillLevel
        self.credits = skillLevel
        if self.skill_level.strip().lower() == 'easy':
            self.credits = 1000
        elif self.skill_level.strip().lower() == 'medium':
            self.credits = 500
        else:
            self.credits = 100
        self.ship = ship
        self.inventory = {}

    def get_engineer_skills(self):
        return int(self.engineer_skills)

    def get_fighter_skills(self):
        return int(self.fighter_skills)

    def get_merchant_skills(self):
        return self.merchant_skills

    def get_skills_used(self):
        return self.pilot_skills + self.fighter_skills + self.merchant_skills + self.pilot_skills

    def get_pilotskills(self):
        return int(self.pilot_skills)

    def get_ship(self):
        return self.ship

    def intojsonform(self):
        json = {
            "PilotSkills": self.get_pilotskills(),
            "Name": self.name,
            "Credits": self.credits
        }
        return json

    def get_inventory(self):
        return self.inventory

    def get_inventorycount(self):
        cargo = 0
        for item in self.inventory:
            cargo += int(self.inventory[item]["Quantity"])
        return cargo

    #takes a JSON of items with Name: and Quantity
    #itemJSON looks like this: [{'Name': 'Berries', 'Quantity': 2}, ...]
    #and adds it to the player inventory
    def add_to_inventory(self, item_json):
        for item in item_json:
            if self.inventory.get(item["Name"]):
                current_amount = int(self.inventory[item["Name"]]["Quantity"])
                add_amount = int(item["Quantity"])
                self.inventory[item["Name"]] = {"Quantity": current_amount + add_amount}
                #subtract cargo space
                if add_amount > self.get_ship().get_cargo(): #not enough space
                    print("You do not have enough space in your ship to hold this item")
                    self.get_ship().cargo = 0
                    return False
                else:
                    self.get_ship().cargo -= add_amount
            else:
                #does not exist in player inventory so we add entry to dictionary
                #print("Not in inventory")
                self.inventory[item["Name"]] = {"Quantity": item["Quantity"]}
        #print("Final Inventory")
        #print(self.inventory)
        return True

    #takes a JSON of items with Name: and Quantity
    #and removes it from the player inventory
    #returns false if item in itemJSON doesn't exist in player inventory
    #or item quantity in itemJSON exceeds player's inventory item quanitty
    def remove_from_inventory(self, item_json):
        #create a temp_inventory and remove from it instead of player inventory
        #in case we return false
        temp_inventory = self.inventory
        for item in item_json:
            if temp_inventory.get(item["Name"]):
                if int(temp_inventory[item["Name"]]["Quantity"]) < int(item["Quantity"]):
                    return False
                else:
                    current_amount = int(temp_inventory[item["Name"]]["Quantity"])
                    remove_amount = int(item["Quantity"])
                    name = item["Name"]
                    temp_inventory[name] = {"Quantity": current_amount - remove_amount}
                    self.get_ship().cargo += remove_amount
                    return True
            else:
                return False
        #the remove request was successful so we update the player's inventory
        self.inventory = temp_inventory
        #print("Final inventory")
        #print(self.inventory)
        return True

    def set_inventory(self, new_inventory):
        self.inventory = new_inventory

    def get_inventory_array_json(self):
        arr = []
        for item in self.inventory:
            json = {
                "Name": item,
                "Quantity": self.inventory[item]["Quantity"]
            }
            arr.append(json)
        return arr

    def get_credits(self):
        return self.credits

    def set_credits(self, new_credits):
        self.credits = new_credits

    def get_name(self):
        return self.name

    def __str__(self):
        return 'Player: ' + self.name + ' has ' + str(self.credits) + ' credits'
