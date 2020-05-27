market_items = [
    ["Berries", 0],
    ["Club", 0],
    ["Bread", 1],
    ["Gold", 1],
    ["Sword", 2],
    ["Rifle", 4],
    ["Medicine", 5],
    ["Protein Shake", 6],
    ["Laser Pistol", 6],
    ["Quantum Computer", 6]
]

base_sellpercentage = .25

class Market():
    #techlevelnum represents the tech level of the region
    def __init__(self, techlevelnum, mskills, player_name, is_winning_region):
        
        self.region_market_items = []
        for i in range(0, len(market_items)):
            if market_items[i][1] <= techlevelnum:
                self.region_market_items.append(market_items[i][0])

        def calculate_prices(self, techlevelnum, mskills, player_name, is_winning_region):
            item_prices = {}
            base_price = 20
            skill_multiplier = 1 / (1 + mskills)
            for i in range(0, len(self.region_market_items)):
                region_multiplier = i / (1 + techlevelnum)
                buy_price = round(skill_multiplier * (1 + region_multiplier) * base_price)
                sell_price = round(buy_price * (base_sellpercentage + mskills/32))
                item = {
                    "buy_price" : buy_price,
                    "sell_price" : sell_price
                }
                item_prices[self.region_market_items[i]] = item

            if is_winning_region:
                #generate the winning item and add it
                item_name = player_name + "'s Universe"
                item_data = {
                    "buy_price": 500,
                    "sell_price": "none"
                }
                item_prices[item_name] = item_data

            return item_prices

        self.prices = calculate_prices(self, techlevelnum, mskills, player_name, is_winning_region)

    def intoarrayjsonform(self):
        array = []
        for item in self.prices:
            json = {
                "Name": item,
                "Buy_Price": self.prices[item]['buy_price'],
                "Sell_Price": self.prices[item]['sell_price']
            }
            array.append(json)
        return array

    def get_items(self):
        return self.region_market_items

    def get_itemprices(self):
        return self.prices

    def calculate_cost(self, item_json, order_type):
        cost = 0
        for item in item_json:
            #print(self.prices[item["Name"]])
            #print(self.prices[item["Name"]]["order_type"])
            cost = cost + int(self.prices[item["Name"]][order_type]) * int(item["Quantity"])
        print(cost)
        return cost

    #update the player inventory and return as a JSON
    #itemJSON looks like this: [{'Name': 'Berries', 'Quantity': 2}, ...]
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
