from random import random, randint

modifier = .25

class Police:
    def __init__(self):
        self.requested_items = []

    def generate_requested_items(self, player_inventory):
        #get the number of items that do not have 0 quantity
        non_zero_player_items = 0
        for value in player_inventory:
            if int(player_inventory[value]["Quantity"]) != 0:
                non_zero_player_items += 1

        num_items_taken = min(2, non_zero_player_items)
        demand = []
        chosen_item_indices = [] #holds the indices of all items wanted so no duplicates

        #_ is when we don't care what variable is
        for _ in range(num_items_taken):
            #20 to 40 percent
            percentage_taken = randint(2, 4) / 10

            random_item = randint(0, len(player_inventory) - 1)
            item_quantity = int(list(player_inventory.items())[random_item][1]["Quantity"])

            #choose new item that hasn't been chosen by police or if quantity of chosen item is 0
            while random_item in chosen_item_indices or item_quantity == 0:
                #print("Duplicate item or zero quantity")
                #print(list(player_inventory.items())[randomItem][0])
                random_item = randint(0, len(player_inventory) - 1)
                item_quantity = int(list(player_inventory.items())[random_item][1]["Quantity"])

            chosen_item_indices.append(random_item)

            item = list(player_inventory.items())[random_item]
            item_name = item[0]
            demanded_item_quantity = round(item_quantity * percentage_taken)

            json = {
                "Name": item_name,
                "Quantity": max(1, demanded_item_quantity)
            }
            demand.append(json)

        print(demand)
        return demand

    def get_result(self, player_skills, is_fight):
        print(player_skills)
        if is_fight:
            #weight fighter skills higher as they only are used for this
            #and pilot skills are more universal
            player_skills *= 2
        rand = random()
        print(rand)
        print(player_skills)

        chance = modifier + player_skills / 16
        print(chance)

        return chance > rand
