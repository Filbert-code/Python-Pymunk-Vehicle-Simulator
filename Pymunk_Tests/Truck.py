import pymunk as pm
import Car


class Truck(Car):
    """
    Create a Truck body and wheels and insert into the Space.
    Return all the information needed to blit the truck image onto the screen.
    """
    def __init__(self, x_pos, y_pos):
        super(self).__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos

    def create_body(self):
        pass