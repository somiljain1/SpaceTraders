from market import Market
from player import Player
class MarketPlayerHandler():
    def __init__(self, market, player):
        self.market = market
        self.player = player

    def buy_order(self, item_json, inventory):
        for item in item_json:
            if inventory.get(item["Name"]):
                print("In inventory")
                inventory[item["Name"]] = {"Quantity": int(inventory[item["Name"]]["Quantity"])
                                                       + int(item["Quantity"])}
            else:
                print("Not in inventory")
                inventory[item["Name"]] = {"Quantity": item["Quantity"]}
        print("Final Inventory")
        print(inventory)
        return inventory

    def sell_order(self, item_json, inventory):
            for item in item_json:
                if inventory.get(item["Name"]):
                    if int(inventory[item["Name"]]["Quantity"]) < int(item["Quantity"]):
                        return False
                    else:
                        inventory[item["Name"]] = {"Quantity": int(inventory[item["Name"]]["Quantity"])
                                                            - int(item["Quantity"])}
                else:
                    return False
            print("Final inventory")
            print(inventory)
            return inventory
