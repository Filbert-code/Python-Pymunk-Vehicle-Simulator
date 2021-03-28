import pymunk as pm
import pygame as pg
from Car import Car
from RoadBuilder import RoadBuilder
import constants


class ObstacleCourse:
    def __init__(self, space):
        self._space = space

    def _create_road(self):
        rb = RoadBuilder(self._space)
        vs = [((0, constants.HEIGHT), (2000, constants.HEIGHT))]
        rb.build_road(vs, 5)

    def _box_fort(self):
        # create a Car instance to use it's box creation function
        c = Car(self._space)
        rb = RoadBuilder(self._space)

        # first line of boxes
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        fort_height = 0
        radius = 50
        starting_pos = 50
        fort_length = 350
        for i in range(10):
            c.create_poly(50, 50, constants.HEIGHT - radius * i, radius, radius)
            c.create_poly(50, 50 + fort_length, constants.HEIGHT - radius * i, radius, radius)
            fort_height = constants.HEIGHT - radius * i
        vs = [((starting_pos, fort_height), (starting_pos + fort_length, fort_height))]




    def build(self):
        self._create_road()
        self._box_fort()
