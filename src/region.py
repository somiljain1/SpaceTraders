class Region:
    def __init__(self, x_coord, y_coord, techlevel, name):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.techlevel = techlevel
        self.name = name

    def get_name(self):
        return self.name

    def get_techlevel(self):
        return self.techlevel

    def get_coords(self):
        return str(self.x_coord) + ", " + str(self.y_coord)

    def print_info(self):
        print("The planet is called " + self.name +
              ". \nIt is located at x-coordinate " +
              str(self.x_coord) + " and y coordinates " + str(self.y_coord))
