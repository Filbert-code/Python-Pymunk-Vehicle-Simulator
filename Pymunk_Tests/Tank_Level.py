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
        self._score = 0
        self._targets = self._swinging_targets([(2400, 0), (3500, 50)])
        self._waterfall_trigger = False
        self._waterfall_target = self._swinging_targets([(4800, 200)])
        self._waterfall_door = None
        self._create_waterfall_door()

    def road(self):
        h = constants.HEIGHT - 5
        vs = [((0, h), (2000, h)), ((2000, h), (2200, h - 100)),
              ((2200, h - 100), (2400, h)),
              ((2400, h), (2800, h - 150)),
              ((2800, h - 150), (3400, h)),
              ((3400, h), (3700, h - 100)),
              ((3700, h - 100), (3900, h - 150)),
              ((3900, h - 150), (4500, h)),
              ((4700, h), (5500, h))
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
        self._seesaw()
        self._bunch_of_balls()

    def _swinging_targets(self, positions):
        """
        Takes a list of vertices; each corresponding to the location of a swinging circle.
        The circle is attached to a static segment. When hit, the circle will change color.
        Returns a list of tuples (circle, circle's position)
        :param positions:
        :return:
        """
        inertia = pm.moment_for_circle(50.0, inner_radius=0, outer_radius=20.0)
        targets = []
        for i in range(len(positions)):
            x, y = positions[i][0], positions[i][1]
            body = pm.Body(50.0, inertia, pm.Body.DYNAMIC)
            circle = pm.Circle(body, 20.0)
            body.position = (x, y+100)
            self._shapes_to_draw['circle'].append((circle, (0, 255, 0)))
            self._space.add(body, circle)
            # make a static object to attach the balloon to
            vs = ((x-150, y), (x+150, y))
            # _road_body, segments = self._rb.build_road(vs, 5)
            static_body = pm.Body(body_type=pm.Body.STATIC)
            seg = pm.Segment(static_body, vs[0], vs[1], radius=5)
            self._shapes_to_draw['segment'].append((seg, (0, 0, 0)))
            self._space.add(static_body, seg)
            constraint = pm.constraints.PinJoint(body, static_body, (0, 0), (x, y))
            self._space.add(constraint)
            targets.append((circle, body.position))
        return targets

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
            body.position = (4600 + randint(-10, 10), constants.HEIGHT-500 + randint(-25, 25))
            ball = pm.Circle(body, radius, (0, 0))
            ball.friction = 0.7
            self._space.add(body)
            self._space.add(ball)
            self._shapes_to_draw['circle'].append((ball, (0, 0, 200)))

    def _create_waterfall_door(self):
        # body, self._waterfall_door = self._c.create_poly(100, 4500, constants.HEIGHT-100, 200, 10, s_filter=3)
        segments = super()._create_road([((4500, constants.HEIGHT), (4700, constants.HEIGHT))])
        self._waterfall_door = segments[0]
        self._shapes_to_draw['segment'].append((segments[0], (140, 65, 140)))

    def _waterfall_update(self):
        if self._waterfall_target[0][0].body.position != self._waterfall_target[0][1]:
            pass
        else:
            self._bunch_of_balls()

    def draw(self):
        super().draw()
        # blit the player's score onto the screen
        score = pg.font.SysFont('Consolas', 32).render('Score: {}'.format(self._score), True, pg.color.Color('Black'))
        self._screen.blit(score, (20, 20))

    def update(self):
        super().update()
        self._waterfall_update()
        for i, target in enumerate(self._targets):
            if target[0].body.position != target[1]:
                for num, circle in enumerate(self._shapes_to_draw['circle']):
                    if circle[0] == target[0]:
                        self._shapes_to_draw['circle'].pop(num)
                        self._targets.pop(i)
                        print('hit')
                        self._shapes_to_draw['circle'].append((circle[0], (255, 0, 0)))
                        self._score += 1
                        break

    def build(self):
        self.road()
        self._obstacle_01()
