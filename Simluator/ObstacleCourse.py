import pymunk as pm
import pygame as pg
from Car import Car
from RoadBuilder import RoadBuilder
from Level import Level
import constants


class ObstacleCourse(Level):
    def __init__(self, space, screen, car, polys):
        super().__init__(space, screen, car)
        self._space = space
        self._screen = screen
        self._rb = rb = RoadBuilder(self._space)
        # create a Car instance to use it's box creation function
        self._c = Car(self._space, screen)
        self._road_body = None
        self.spring_trap_pin = None
        self.polys = polys
        self.box_fort_image = pg.image.load("images/box_fort_img.png")

    def _create_road(self):
        h = constants.HEIGHT - 5
        vs = [((0, h), (670, h)), ((930, h), (2000, h)), ((2000, h), (2200, h-50)),
              ((2200, h-50), (2400, h-200)),
              ((3400, h-150), (3600, h-75)),
              ((3600, h - 75), (3800, h)),
              ((3800, h), (5000, h)),
              # ((0, constants.HEIGHT), (400, constants.HEIGHT-250))
              ]
        self._road_body, segments = self._rb.build_road(vs, 5)
        return segments

    def _box_fort(self):
        # first line of boxes
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        fort_height = 0
        radius = 35
        starting_pos = 50
        fort_length = 350
        color = (50, 120, 240, 255)  # blue
        image1 = pg.image.load("images/box_fort_img.png")
        list_of_bodies = []
        for i in range(10):
            b1, s1 = self._c.create_poly(50, 50, constants.HEIGHT - radius * i, radius, radius, friction=1, color=color)
            b2, s2 = self._c.create_poly(50, 50 + fort_length, constants.HEIGHT - radius * i, radius, radius, friction=1, color=color)
            fort_height = constants.HEIGHT - radius * i
            # self._shapes_to_draw['rect'].append(b1, (255, 0, 0), radius, radius)
            # self._shapes_to_draw['rect'].append(b2, (255, 0, 0), radius, radius)
            list_of_bodies.append(b1)
            list_of_bodies.append(b2)
        b, s = self._c.create_poly(200, starting_pos + fort_length / 2, fort_height - radius, fort_length, 35, color=color)
        image2 = pg.image.load("images/box_fort_roof_img.png")
        self.polys[image1] = list_of_bodies
        self.polys[image2] = [b]


    def _spring_trap(self):
        # create the spring body
        mass = 500
        width, length = 250, 10
        body, shape = self._c.create_poly(mass, 800, 715, width, length)
        # create the springs
        x, y = (800, 720)
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
        image = pg.image.load("images/wooden_spring_trap.png")
        self.polys[image] = [body]

    def build(self):
        segments = self._create_road()
        # self._box_fort()
        self._spring_trap()
        return segments
