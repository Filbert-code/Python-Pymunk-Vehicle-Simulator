import pymunk as pm
from Car import Car


class Truck(Car):
    """
    Create a Truck body and wheels and insert into the Space.
    Return all the information needed to blit the truck image onto the screen.
    """
    def __init__(self, space, x_pos, y_pos):
        super().__init__(space)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def create_body_wheels(self):
        w = 200
        h = 80
        shape_filter = pm.ShapeFilter(categories=0b1000)
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        truck_body, shape = self._create_poly(600, self.x_pos, self.y_pos, w, h)
        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        truck_back_wheel = self._create_wheel(50, self.x_pos - w/2, self.y_pos + h / 2, h / 2)
        truck_front_wheel = self._create_wheel(50, self.x_pos + w / 2, self.y_pos + h / 2, h / 2)

    def build(self):
        self.create_body_wheels()

