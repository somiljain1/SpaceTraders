import random

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

class Trader:
    def __init__(self):
        self.item = random.choice(market_items)
        self.item_to_sell = self.item[0]
        self.random_amount = random.randint(2, 10)
        self.item_price = random.randint(2, 20)

    def get_item_to_sell(self):
        return self.item_to_sell

    def get_random_amount(self):
        return self.random_amount

    def get_item_price(self):
        return self.item_price

    # def get_price():
    #     return item_to_sell
