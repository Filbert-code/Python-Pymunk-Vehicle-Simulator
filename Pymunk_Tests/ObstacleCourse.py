import pymunk as pm
import pygame as pg
from Car import Car
from RoadBuilder import RoadBuilder
import constants


class ObstacleCourse:
    def __init__(self, space):
        self._space = space
        self._rb = rb = RoadBuilder(self._space)
        # create a Car instance to use it's box creation function
        self._c = Car(self._space)
        self._road_body = None
        self.spring_trap_pin = None

    def _create_road(self):
        vs = [((0, constants.HEIGHT), (2000, constants.HEIGHT))]
        self._road_body, segments = self._rb.build_road(vs, 5)

    def _box_fort(self):
        # first line of boxes
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        fort_height = 0
        radius = 35
        starting_pos = 50
        fort_length = 350
        for i in range(10):
            self._c.create_poly(50, 50, constants.HEIGHT - radius * i, radius, radius, friction=1)
            self._c.create_poly(50, 50 + fort_length, constants.HEIGHT - radius * i, radius, radius, friction=1)
            fort_height = constants.HEIGHT - radius * i
        left = (starting_pos, fort_height)
        right = (starting_pos + fort_length, fort_height)
        self._c.create_poly(200, starting_pos + fort_length / 2, fort_height - radius, fort_length, 35)

    def _spring_trap(self):
        # create the spring body
        mass = 500
        width, length = 250, 0.01
        body, shape = self._c.create_poly(mass, 800, 595, width, length)
        # create the springs
        x, y = (800, 600)
        strength = 200000
        rest_length = 100
        spring_1 = pm.constraints.DampedSpring(body, self._road_body, (0, 0), (x, y + 20), rest_length, strength, 1)
        spring_2 = pm.constraints.DampedSpring(body, self._road_body, (-50, 0), (x - 50, y + 20), rest_length, strength, 1)
        spring_3 = pm.constraints.DampedSpring(body, self._road_body, (50, 0), (x + 50, y + 20), rest_length, strength, 1)
        # create stabilizer slider joints
        stabilizer_1 = pm.constraints.SlideJoint(body, self._road_body, (-75, 0), (x + 75, y + 20), 0, 180)
        stabilizer_2 = pm.constraints.SlideJoint(body, self._road_body, (75, 0), (x - 75, y + 20), 0, 180)
        self.spring_trap_pin = pm.constraints.PinJoint(body, self._road_body, (0, 0), (x, y))
        self._space.add(spring_1, spring_2, spring_3, stabilizer_1, stabilizer_2)
        self._space.add(self.spring_trap_pin)

    def build(self):
        self._create_road()
        # self._box_fort()
        self._spring_trap()
