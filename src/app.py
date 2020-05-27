import random
from flask import Flask, render_template, request, json #, url_for
from game import Game
from player import Player
from police import Police
from ship import Ship
from market import Market
from trader import Trader
from bandit import Bandit

game = Game() #the object where all relevant info is stored
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    #name = request.args.get("name", "World")
    return render_template('home.html')

@app.route("/config")
def config():
    return render_template('about.html', title='Configure Screen')

@app.route("/display", methods=['GET', 'POST'])
def display():
    if request.method == "POST":
        name = request.form['name']
        difficulty = request.form['selecteddifficulty']
        pilotskills = request.form['ps']
        fighterskills = request.form['fs']
        merchantskills = request.form['ms']
        engineerskills = request.form['es']

        ship_type = request.form['selectedship']
        ship = Ship(ship_type)

        player = Player(name, pilotskills, fighterskills,
                        merchantskills, engineerskills, difficulty, ship)

        game.initialize_player(player)
        game.set_difficulty(difficulty)

        ship_type = game.get_player().get_ship().get_ship_type()
        fuel = game.get_player().get_ship().get_fuel()
        cargo = game.get_player().get_ship().get_cargo()
        health = game.get_player().get_ship().get_health()


        return render_template('display.html',
                               name=name,
                               difficulty=difficulty,
                               pilotskills=pilotskills,
                               fighterskills=fighterskills,
                               merchantskills=merchantskills,
                               engineerskills=engineerskills,
                               ship=ship,
                               ship_type=ship_type,
                               fuel=fuel,
                               cargo=cargo,
                               health=health,
                               title='Display screen')
        #We access name = request.form['name'] in the html using {{ name }}
    else:
        return render_template('about.html', title='Configure Screen')

@app.route("/universe", methods=['GET', 'POST'])
def universe():
    game.create_universe()
    player = game.get_player()
    inventory = player.get_inventory()
    #s = Ship()
    #turns region list into JSON-format
    #print(json.dumps(u.intoarrayjsonform()))
    return render_template('universe.html', title='Universe',
                           player=json.dumps(player.intojsonform()),
                           ship=json.dumps(player.get_ship().intojsonform()),
                           inventory=inventory,
                           universe=json.dumps(game.get_universe().intoarrayjsonform()))

@app.route("/calc_distance", methods=['POST'])
def calc_distance():
    universe = game.get_universe()
    planetnames = game.get_planetnames()
    regions = game.get_regions()
    r_1 = regions[planetnames.index(request.form["r1"])]
    r_2 = regions[planetnames.index(request.form["r2"])]
    distance = universe.calc_distance(r_1, r_2)

    return json.dumps({"distance": distance})

@app.route("/current_region", methods=["GET"])
def current_region():
    current_region = game.get_universe().get_currentregion()
    return json.dumps({"name": current_region.get_name(),
                       "coordinates": current_region.get_coords(),
                       "techlevel": current_region.get_techlevel()})

#updates current region and the ship fuel stat
@app.route("/update_stats", methods=["POST"])
def update_stats():
    universe = game.get_universe()
    regions = game.get_regions()
    planetnames = game.get_planetnames()

    universe.set_currentregion(regions[planetnames.index(request.form["nextRegionName"])])

    ship = game.get_player().get_ship()
    ship.set_fuel(request.form["fuel"])

    return "Success"


@app.route("/market", methods=['GET', 'POST'])
def market():
    player = game.get_player()
    techlevels = game.get_techlevels()

    is_winning_region = game.get_universe().get_winningitem_region() == game.get_universe().get_currentregion()

    #admin cheats :)
    print("ADMIN CHEATS")
    print(game.get_universe().get_winningitem_region().get_name())
    print(game.get_universe().get_currentregion().get_name())
    print(is_winning_region)

    market = Market(techlevels.index(request.form['techlevel']), player.get_merchant_skills(), player.get_name(), is_winning_region)
    game.set_market(market)

    print(player.get_inventory())

    empty_inventory = False
    if player.get_inventory() == {}:
        empty_inventory = True

    return render_template('market.html',
                           market=json.dumps(market.intoarrayjsonform()),
                           techlevel=request.form['techlevel'],
                           credits=player.get_credits(),
                           inventory=json.dumps(player.get_inventory_array_json()),
                           inventory_status=empty_inventory)
                           #player=json.dumps(player.intojsonform()))
                           #ideally return credits and inventory here

@app.route("/buy", methods=['POST'])
def buy():
    print("REQUEST FORM BUY")
    #print(request.form)
    items = request.form["items"]
    parsed_items = json.loads(items)
    #print(items)
    #print(json.loads(items)[0])

    market = game.get_market()
    player = game.get_player()
    cost = market.calculate_cost(parsed_items, "buy_price")
    if cost <= player.get_credits():
        player.set_credits(player.get_credits() - cost)
        #don't uncomment
        # player.set_inventory(market.buy_order(parsed_items, player.get_inventory()))
        player.add_to_inventory(parsed_items)

        for item in parsed_items:
            #if the player bought the universe, they win
            if "Universe" in item.get("Name"):
                return json.dumps({"result": "winner"})

        print(player.get_inventory())

        return json.dumps({"inventory": json.dumps(player.get_inventory_array_json()),
                           "credits": player.get_credits()})
    else:
        return json.dumps({"result": "fail"})

@app.route("/sell", methods=['POST'])
def sell():
    print("REQUEST FORM SELL")
    print(request.form)
    items = request.form["items"]
    parsed_items = json.loads(items)
    print(items)
    print(json.loads(items)[0])

    market = game.get_market()
    player = game.get_player()

    if not player.remove_from_inventory(parsed_items):
        return json.dumps({"result": "fail"})
    else:
        player.set_credits(player.get_credits() + market.calculate_cost(parsed_items, "sell_price"))
        return json.dumps({"inventory": json.dumps(player.get_inventory_array_json()),
                           "credits": player.get_credits()})

@app.route("/chance_NPC", methods=['POST'])
def chance_NPC():
    regions = game.get_regions()
    planetnames = game.get_planetnames()

    #store the possible new region and fuel counts in game
    game.store_potential_region(regions[planetnames.index(request.form["region"])])
    game.store_potential_fuel(request.form["fuel"])

    print("calculating chance of NPC encounter")
    difficulty = game.get_difficulty().strip().lower()

    #change chance of encounter to 10, 20, 30%
    if difficulty == "easy":
        num = 2
    elif difficulty == "medium":
        num = 4
    else:
        num = 6

    #determines if encounter occurs
    random_num = random.randint(0, 9)
    encounter = random_num < num

    print("ENCOUNTER")
    print(encounter)
    #encounter has happened, determines if police, bandit, or trader shows up
    if encounter:

        #if the player's inventory is empty we shouldn't get police
        if game.get_player().get_inventorycount() == 0:
            random_npc = random.randint(0, 1)
        else:
            random_npc = random.randint(0, 2)

        if random_npc == 0:
            encounter_type = 'bandit'
        elif random_npc == 1:
            encounter_type = 'trader'
        else:
            encounter_type = 'police'

        game.set_encounter_type(encounter_type)

        return json.dumps({"result": "npc", "page": game.get_encounter_type()})

    return json.dumps({"result": "noNpc"})

@app.route("/bandit", methods=['GET', 'POST'])
def bandit():
    bandit = Bandit()
    game.init_bandit(bandit)
    player = game.get_player()
    return render_template('bandit.html', credits_demanded=bandit.get_credits_demanded(),
                           fskills=player.get_fighter_skills(), pskills=player.get_pilotskills())

@app.route("/bandit_pay", methods=['POST'])
def bandit_pay():
    bandit = game.get_bandit()
    credits_demanded = bandit.get_credits_demanded()
    player = game.get_player()

    universe = game.get_universe()
    universe.set_currentregion(game.get_potential_region())
    ship = game.get_player().get_ship()
    ship.set_fuel(game.get_potential_fuel())

    if credits_demanded < player.get_credits():
        player.set_credits(player.get_credits() - credits_demanded)
        return json.dumps({"result": "lose_credits", "credits": player.get_credits()})
    elif player.get_inventory() is not None:
        player.set_inventory({})
        return json.dumps({"result": "lose_inventory"})
    else:
        ship = player.get_ship()
        hp_lost = 10
        ship.set_health(ship.get_health() - hp_lost)
        return json.dumps({"result": "lose_ship_health", "health": ship.get_health()})

@app.route("/bandit_fight", methods=['POST'])
def bandit_fight():
    bandit = game.get_bandit()
    player = game.get_player()
    credits_demanded = bandit.get_credits_demanded()

    universe = game.get_universe()
    universe.set_currentregion(game.get_potential_region())
    ship = game.get_player().get_ship()
    ship.set_fuel(game.get_potential_fuel())

    if bandit.get_result(player.get_fighter_skills(), True):
        credits_won = credits_demanded - random.randint(0, credits_demanded)
        return json.dumps({"result": "success", "credits_won": credits_won})

    player.set_credits(0)
    ship = player.get_ship()
    hp_lost = 10
    ship.set_health(ship.get_health() - hp_lost)

    return json.dumps({"result": "fail", "credits": player.get_credits(),
                       "health_penalty": hp_lost, "health": ship.get_health()})


@app.route("/bandit_flee", methods=['POST'])
def bandit_flee():
    bandit = game.get_bandit()
    player = game.get_player()

    if bandit.get_result(player.get_pilotskills(), False):
        ship = game.get_player().get_ship()
        ship.set_fuel(game.get_potential_fuel())
        return json.dumps({"result": "success"})

    player.set_credits(0)
    ship = player.get_ship()
    hp_lost = 10
    ship.set_health(ship.get_health() - hp_lost)

    universe = game.get_universe()
    #universe.set_currentregion(game.get_potential_region())

    ship = game.get_player().get_ship()
    ship.set_fuel(game.get_potential_fuel())

    return json.dumps({"result": "fail", "credits": player.get_credits(),
                       "health_penalty": hp_lost, "health": ship.get_health()})

@app.route("/police", methods=['GET', 'POST'])
def police():
    player = game.get_player()
    pol = Police()
    demand = pol.generate_requested_items(player.get_inventory())
    return render_template('police.html', demand=json.dumps(demand),
                           fskills=player.get_fighter_skills(), pskills=player.get_pilotskills())

@app.route("/forfeit", methods=['POST'])
def forfeit():
    items = request.form["items"]
    items = json.loads(items)
    print("ITEMS")
    print(items)
    player = game.get_player()
    print(player.get_inventory())
    player.remove_from_inventory(items)
    print(player.get_inventory())

    #police confiscate items and let player go to new region so update
    universe = game.get_universe()

    print("NAME")
    print(game.get_potential_region().get_name())
    universe.set_currentregion(game.get_potential_region())

    ship = game.get_player().get_ship()
    ship.set_fuel(game.get_potential_fuel())

    return json.dumps({"items": player.get_inventory_array_json()})

@app.route("/flee", methods=['POST'])
def flee():
    #whether or not player is successful, region remains same

    player = game.get_player()
    pol = Police()

    #False is for not using fighter skills
    if pol.get_result(player.get_pilotskills(), False):
        ship = game.get_player().get_ship()
        ship.set_fuel(game.get_potential_fuel())
        return json.dumps({"result": "success"})

    #credit penalty is 15-30% of player's credits
    credit_penalty = int(player.get_credits() * (random.randint(15, 30) / 100))
    player.set_credits(player.get_credits() - credit_penalty)

    print(credit_penalty)
    print(player.get_credits())

    #player loses 10 hit points on their ship
    ship = player.get_ship()
    hp_lost = 10
    ship.set_health(ship.get_health() - hp_lost)

    #police confiscate items
    items = request.form["items"]
    items = json.loads(items)
    player.remove_from_inventory(items)

    return json.dumps({"result": "fail", "health_penalty": hp_lost, "health": ship.get_health(),
                       "credit_penalty": credit_penalty, "credits": player.get_credits()})

@app.route("/fight", methods=['POST'])
def fight():

    player = game.get_player()
    pol = Police()

    #if fight was successful
    if pol.get_result(player.get_fighter_skills(), True):

        #fight off police, get to travel to new region so update
        universe = game.get_universe()
        universe.set_currentregion(game.get_potential_region())

        ship = game.get_player().get_ship()
        ship.set_fuel(game.get_potential_fuel())

        return json.dumps({"result": "success"})

    #change current region to random one
    regions = game.get_regions()
    universe = game.get_universe()
    rand = random.randint(0, len(regions) - 1)
    universe.set_currentregion(regions[rand])

    #player loses 40 hit points on their ship
    ship = player.get_ship()
    hp_lost = 40
    ship.set_health(ship.get_health() - hp_lost)

    #police confiscate items
    items = request.form["items"]
    items = json.loads(items)
    player.remove_from_inventory(items)

    return json.dumps({"result": "fail", "health_penalty": hp_lost, "health": ship.get_health()})

@app.route("/trader", methods=['GET', 'POST'])
def trader():
    trader = Trader()
    game.init_trader(trader)
    player = game.get_player()
    item_to_sell = game.get_trader().get_item_to_sell()
    item_amount = game.get_trader().get_random_amount()
    item_price = game.get_trader().get_item_price()
    return render_template('trader.html',
                           item_to_sell=item_to_sell,
                           item_amount=item_amount,
                           inventory=game.get_player().get_inventory(),
                           item_price=item_price,
                           credits=game.get_player().get_credits(),
                           fskills = player.get_fighter_skills(),
                           mskills = player.get_merchant_skills(),
                           health = player.get_ship().get_health()
                          )

@app.route("/attempt_rob", methods=['GET', 'POST'])
def attempt_rob():
    player = game.get_player()
    trader = game.get_trader()
    ship = player.get_ship()
    health = ship.get_health()
    inventory = player.get_inventory()
    fskills = player.get_fighter_skills() #number between [0, 16]

    rob = random.randint(0, 19) < fskills

    if rob is True:
        item = trader.get_item_to_sell()
        amount = random.randint(1, trader.get_random_amount() - 1) #random amount taken from trader
        try:
            player.inventory[item]['Quantity'] += amount
        except:
            player.inventory[item] = {'Quantity': amount}
        player.set_cargo(player.get_cargo() - amount)
        message = 'Ayy! You robbed the poor fool lol! You got some of his items!'
    else:
        #subtracts 10 from health, or resets health to 0
        print(health)
        if health < 10:
            ship.set_health(0)
        else:
            ship.set_health(health - 10)
        message = 'Yikers! You failed to rob the trader! Trader damaged your ship by 10!'

    return json.dumps({"rob_attempt": rob, 
                       "message": message, 
                       "health": ship.get_health(), 
                       "inventory": player.get_inventory()})

# @app.route("/success_rob", methods=['GET', 'POST'])
# def success_rob():
#     player = game.get_player()
#     trader = game.get_trader()
#     item = trader.get_item_to_sell()
#     amount = random.randint(1, trader.get_random_amount()) #random amount taken from trader
#     try:
#         player.inventory[item]['Quantity'] += amount
#     except:
#         player.inventory[item] = {'Quantity': amount}

#     return ""

# @app.route("/success_rob_page", methods=['GET', 'POST'])
# def success_rob_page():
#     return render_template('success_rob.html',
#                            inventory=game.get_player().get_inventory()
#                           )

# @app.route("/fail_rob", methods=['GET', 'POST'])
# def fail_rob():
#     player = game.get_player()
#     ship = player.get_ship()
#     health = ship.get_health()

#     #subtracts 10 from health, or resets health to 0
#     print(health)
#     if health < 10:
#         ship.set_health(0)
#     else:
#         ship.set_health(health - 10)
#     return ""

# @app.route("/fail_rob_page", methods=['GET', 'POST'])
# def fail_rob_page():
#     return render_template('fail_rob.html',
#                            health=game.get_player().get_ship().get_health()
#                           )

@app.route("/attempt_neg", methods=['GET', 'POST'])
def attempt_neg():
    player = game.get_player()
    mskills = player.get_merchant_skills() #number between [0, 16]

    neg = random.randint(0, 19) < mskills

    #successful negotiation
    old_price = game.get_trader().get_item_price()
    if neg is True:
        new_price = round(old_price * 0.6, 2)
        message = "You're super smooth with your convincing skills! Trader lowered his selling price by 40%."
    else:
        new_price = round(old_price * 1.25, 2)
        message = "You're mediocre at negotiating sadly! Trader increased his selling price 25%."

    return json.dumps({"message": message, "new_price": new_price})

@app.route("/buy_trader_item", methods=['GET', 'POST'])
def buy_trader_item():
    player = game.get_player()
    trader = game.get_trader()
    item = trader.get_item_to_sell()
    amount = trader.get_random_amount()
    price = trader.get_item_price()

    player.add_to_inventory([{"Name": item, "Quantity": amount}])
    player.set_credits(player.get_credits() - price)
    print(player.get_inventory())
    return json.dumps({"Inventory": player.get_inventory()})

@app.route("/continue_travel", methods=['GET'])
def continue_travel():
    universe = game.get_universe()
    ship = game.get_player().get_ship()
    #print(game.get_potential_region().get_name())

    universe.set_currentregion(game.get_potential_region()) #current region is now intended region
    ship.set_fuel(game.get_potential_fuel())
    return ""

@app.route("/mechanic", methods=['GET', 'POST'])
def mechanic():
    player = game.get_player()
    ship = player.get_ship()
    eskills = player.get_engineer_skills()

    #init base prices
    game.set_mechanic_prices([10, 20, 30])

    #price calculation
    new_prices = []
    for price in game.get_mechanic_prices():
        
        # price decreases based off eskills
        try:
            new_price = price / (eskills / 4)
        except:
            new_price = price
        new_prices.append(new_price)
    
    game.set_mechanic_prices(new_prices)

    return render_template('mechanic.html',
                            fuel = ship.get_fuel(),
                            credits = player.get_credits(),
                            health = ship.get_health(),
                            prices = game.get_mechanic_prices()
                            )

@app.route("/refuel", methods = ['GET', 'POST'])
def refuel():
    print("refuel")
    add_fuel = int(request.form["fuel"])
    price = int(request.form["price"])
    player = game.get_player()
    ship = player.get_ship()
    message = "True"

    if price > player.get_credits(): #not enough credits
        print("not enough credits to refuel")
        message = "not enough credits to refuel"
    else:
        print(player.get_credits())
        print(ship.get_fuel())

        player.set_credits(player.get_credits() - price) #update credits
        ship.set_fuel(ship.get_fuel() + add_fuel) #update ship fuel
        
        print(player.get_credits())
        print(ship.get_fuel())
    
    return json.dumps({"message": message})

@app.route("/repair", methods = ['GET', 'POST'])
def repair():
    print("repair")

    index = int(request.form["index"])
    add_health = int(request.form["health"])
    player = game.get_player()
    ship = player.get_ship()
    mechanic_prices = game.get_mechanic_prices()
    mechanic_price = mechanic_prices[index]

    message = "True"

    if mechanic_price > player.get_credits(): #not enough credits
        print("not enough credits to refuel")
        message = "not enough credits to repair"
    else:
        print(player.get_credits())
        print(ship.get_health())

        player.set_credits(player.get_credits() - mechanic_price) #update credits
        ship.set_health(ship.get_health() + add_health) #update ship fuel
        
        print(player.get_credits())
        print(ship.get_health())
    
    return json.dumps({"message": message})
        

@app.route("/winnerOfTheGame")
def winner():
    return render_template('winner.html')

@app.route("/newgame")
def newgame():
    game.reset()
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
