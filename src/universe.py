import random
from region import Region


class Universe:
    def __init__(self, planet_names, tech_levels):
        self.region_list = []

        #represents the set of all x-coordinates of all existing planets in the universe
        self.planetxcoords = []

        #represents the set of all y-coordinates of all existing planets in the universe
        self.planetycoords = []

        for planet_name in planet_names:
            xcoord = random.randint(-200, 200)
            ycoord = random.randint(-200, 200)

            validxcoord = False
            while not validxcoord:
                validxcoord = True
                for x_val in self.planetxcoords:
                    #Check if the coords are within 5 for any of the existing planets
                    if abs(xcoord - x_val) <= 5:
                        #Recalculate a new x value and check again
                        xcoord = random.randint(-200, 200)
                        validxcoord = False
                        #kick out of for loop and rerun through the while loop
                        break

            validycoord = False
            while not validycoord:
                validycoord = True
                for y_val in self.planetycoords:
                    #Check if the coords are within 5 for any of the existing planets
                    if abs(ycoord - y_val) <= 5:
                        #Recalculate a new y value and check again
                        ycoord = random.randint(-200, 200)
                        validycoord = False
                        #kick out of for loop and rerun through the while loop
                        break
            self.region_list.append(Region(xcoord, ycoord, random.choice(tech_levels), planet_name))
            self.planetxcoords.append(xcoord)
            self.planetycoords.append(ycoord)
        #random region to hold game winning item
        self.winningitem_containing_region = self.region_list[random.randint(0, 9)]

        self.currentregion = self.region_list[random.randint(0, 9)]

    def intoarrayjsonform(self):
        array = []
        for region in self.region_list:
            json = {
                "Coordinates": region.get_coords(),
                "Name": region.get_name(),
                "TechLevel": region.get_techlevel()
            }
            array.append(json)
        return array

    def get_regionlist(self):
        return self.region_list

    def get_currentregion(self):
        return self.currentregion

    def set_currentregion(self, newregion):
        self.currentregion = newregion
    
    def get_winningitem_region(self):
        return self.winningitem_containing_region

    def calc_distance(self, region_1, region_2):
        x_diff = region_1.x_coord - region_2.x_coord
        y_diff = region_1.y_coord - region_2.y_coord
        x_diff = x_diff ** 2
        y_diff = y_diff ** 2
        return round((x_diff + y_diff) ** .5)