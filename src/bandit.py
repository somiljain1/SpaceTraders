import random

modifier = 0.25

class Bandit():
    def __init__(self):
        self.credits_demanded = random.randint(0, 100)

    def get_credits_demanded(self):
        return self.credits_demanded

    def get_result(self, player_skills, is_fight):
        if is_fight:
            #weight fighter skills higher as they only are used for
            #this and pilot skills are more universal
            player_skills *= 2

        rand = random.random()
        chance = modifier + player_skills / 16

        return chance > rand
