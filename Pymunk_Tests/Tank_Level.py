import pymunk as pm
import pygame as pg
from Car import Car
from Level import Level
from RoadBuilder import RoadBuilder
import constants
import math
from random import randint


class Tank_Level(Level):
    def __init__(self, space, screen, car):
        super().__init__(space, screen, car)
        self._space = space
        self._screen = screen
        self._car = car
        self._timer = pg.time.get_ticks()

    def road(self):
        h = constants.HEIGHT - 5
        vs = [((0, h), (600, h)), ((800, h), (2000, h)), ((2000, h), (2200, h - 100)),
              ((2200, h - 100), (2400, h)),
              ((2400, h), (2800, h - 150)),
              ((2800, h - 150), (3400, h)),
              ((3400, h), (3700, h - 100)),
              ((3700, h - 100), (3900, h - 150)),
              ((3900, h - 150), (4500, h)),
              # ((0, constants.HEIGHT), (400, constants.HEIGHT-250))
              ]
        # returns Segments of the road
        segments = super()._create_road(vs)
        for seg in segments:
            self._shapes_to_draw['segment'].append((seg, (150, 75, 150)))

    def _obstacle_01(self):
        # w, h = 30, 30
        # for i in range(10):
        #     self._c.create_poly(500, 1600, 690 - h * i, w, h)
        self._kinematic_obj()
        self._seesaw()
        self._bunch_of_balls()

    def _kinematic_obj(self):
        inertia = pm.moment_for_circle(50.0, inner_radius=0, outer_radius=20.0)
        body = pm.Body(50.0, inertia, pm.Body.DYNAMIC)
        circle = pm.Circle(body, 20.0)
        body.position = (1600, 200)
        self._shapes_to_draw['circle'].append((circle, (0, 255, 0)))
        self._space.add(body, circle)
        # make a static object to attach the balloon to
        vs = ((1450, 100), (1750, 100))
        # _road_body, segments = self._rb.build_road(vs, 5)
        static_body = pm.Body(body_type=pm.Body.STATIC)
        seg = pm.Segment(static_body, vs[0], vs[1], radius=5)
        self._shapes_to_draw['segment'].append((seg, (0, 0, 0)))
        self._space.add(static_body, seg)
        constraint = pm.constraints.PinJoint(body, static_body, (0, 0), (1600, 100))
        self._space.add(constraint)

    def _seesaw(self):
        w, h = 600, 10
        seesaw, shape = self._c.create_poly(500, 1200, 620, w, h, elasticity=0, friction=1, rot=-math.pi/12)
        constraint = pm.constraints.PivotJoint(seesaw, pm.Body(0.0, 0.0, pm.Body.STATIC), (1200, 620))
        self._shapes_to_draw['rect'].append((shape, (150, 75, 150), w, h))
        self._space.add(constraint)

    def _bunch_of_balls(self):
        radius = 7
        mass = 10
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        _curr_time = pg.time.get_ticks()
        if _curr_time - self._timer > 25:
            self._timer = _curr_time
            self._bunch_of_balls()
        # for i in range(1):
            body = pm.Body(mass, inertia, pm.Body.DYNAMIC)
            body.position = (700 + randint(-10, 10), constants.HEIGHT-500+ randint(-25, 25))
            ball = pm.Circle(body, radius, (0, 0))
            ball.friction = 0.7
            self._space.add(body)
            self._space.add(ball)
            self._shapes_to_draw['circle'].append((ball, (0, 0, 200)))

    def draw(self):
        super().draw()
        # self._bunch_of_balls()

    def build(self):
        self.road()
        self._obstacle_01()
