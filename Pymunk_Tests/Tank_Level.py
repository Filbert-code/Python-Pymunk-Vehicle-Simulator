import pymunk as pm
import pygame as pg
from Car import Car
from Level import Level
from RoadBuilder import RoadBuilder
import constants


class Tank_Level(Level):
    def __init__(self, space, screen):
        super().__init__(space, screen)
        self._space = space
        self._screen = screen

    def road(self):
        h = constants.HEIGHT - 5
        vs = [((0, h), (2000, h)), ((2000, h), (2200, h - 50)),
              ((2200, h - 50), (2400, h - 80)),
              ((2400, h - 80), (2800, h - 50)),
              ((2800, h - 50), (3400, h)),
              ((3400, h), (3700, h - 100)),
              ((3700, h - 100), (3900, h - 150)),
              ((3900, h - 150), (4500, h)),
              # ((0, constants.HEIGHT), (400, constants.HEIGHT-250))
              ]
        # returns Segments of the road
        return super()._create_road(vs)

    def _obstacle_01(self):
        # w, h = 30, 30
        # for i in range(10):
        #     self._c.create_poly(500, 1600, 690 - h * i, w, h)
        self._kinematic_obj()

    def _kinematic_obj(self):
        inertia = pm.moment_for_circle(50.0, inner_radius=0, outer_radius=20.0)
        body = pm.Body(50.0, inertia, pm.Body.DYNAMIC)
        circle = pm.Circle(body, 20.0)
        body.position = (1600, 200)
        self._shapes_to_draw.append(circle)
        self._space.add(body)
        self._space.add(circle)
        # make a static object to attach the balloon to
        vs = ((1450, 100), (1750, 100))
        # _road_body, segments = self._rb.build_road(vs, 5)
        static_body = pm.Body(body_type=pm.Body.STATIC)
        seg = pm.Segment(static_body, vs[0], vs[1], 5)
        self._space.add(static_body, seg)
        # create a dampedspring
        constraint = pm.constraints.PinJoint(body, static_body, (0, 0), (1600, 100))
        print(body.position, static_body.position)
        self._space.add(constraint)

    def draw(self):
        super().draw()

    def build(self):
        segments = self.road()
        self._obstacle_01()
        return segments
