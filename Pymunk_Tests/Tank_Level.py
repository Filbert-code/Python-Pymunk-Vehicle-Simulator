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
        self._targets = self._create_swinging_targets([(2400, 0), (3500, 50)])
        self._waterfall_trigger = False
        # self._waterfall_target = self._create_swinging_targets([])
        self._collapsible_door_target = None
        self._waterfall_door_target = None
        self._waterfall = True
        self._catapult_target_bodies = None

    def road(self):
        h = constants.HEIGHT - 5
        # vertices of the rough terrain in the middle of the level
        random_road_vs = self._rb.random_terrain_vertices_generator((5500, h), 60, 60)
        # last vertex of the rough terrain road
        last_v = random_road_vs[-1][1]
        vs = [((0, h), (1500, h)), ((1500, h), (1800, h - 50)),
              ((1800, h - 50), (2300, h-200)),
              ((2300, h - 200), (2800, h-200)),
              ((2800, h-200), (3000, h)),
              ((3000, h), (3200, h-200)),
              ((3200, h-200), (3500, h - 200)),
              ((3500, h - 200), (3700, h - 250)),
              ((3700, h - 250), (3900, h-320)),
              ((3900, h-320), (4100, h-320)),
              ((4700, h - 320), (5100, h-320)),
              ((5100, h-320), (5100, 0)),
              ((3900, h), (5500, h)),
              ((3900, h), (3900, h-320)),
              ((last_v[0], last_v[1]), (last_v[0] + 400, h)),
              ((last_v[0] + 600, h), (last_v[0] + 1000, h-100)),
              ((last_v[0] + 1000, h-100), (last_v[0] + 1400, h - 100)),
              ((last_v[0] + 1400, h - 100), (last_v[0] + 1800, h - 150)),
              ((last_v[0] + 1800, h - 150), (last_v[0] + 2000, h - 185)),
              ((last_v[0] + 2000, h - 185), (last_v[0] + 2330, h-280)),
              # segment for waterfall
              ((9000, 0), (9190, 200)),
              ((9000, 0), (9190, 200)),
              ((12300, constants.HEIGHT - 40), (12350, constants.HEIGHT - 40)),
              ((12170, constants.HEIGHT - 105), (12170, constants.HEIGHT - 125)),
              # 12800, constants.HEIGHT - 255
              ]

        vs = vs + random_road_vs
        # returns Segments of the road
        segments = super()._create_road(vs)

        for seg in segments:
            self._shapes_to_draw['segment'].append((seg, (150, 75, 150)))

    def _obstacle_01(self):
        # w, h = 30, 30
        # for i in range(10):
        #     self._c.create_poly(500, 1600, 690 - h * i, w, h)
        self._seesaw(500, 1200, 620, 600, 10)
        self._seesaw(20000, 11800, constants.HEIGHT-155, 1100, 20, angle=math.pi/12, offset=(350, 100))
        self._ball_pit()
        self._collapsible_door()
        self._waterfall_door()
        self._create_giant_ball()
        self._catapult()

        # self._bunch_of_balls()

    def _create_swinging_targets(self, positions, radius=20.0, distance=100, mass=50.0):
        """
        Takes a list of vertices; each corresponding to the location of a swinging circle.
        The circle is attached to a static segment. When hit, the circle will change color.
        Returns a list of tuples (circle, circle's position)
        :param positions:
        :return:
        """
        inertia = pm.moment_for_circle(mass, inner_radius=0, outer_radius=20.0)
        targets = []
        for i in range(len(positions)):
            x, y = positions[i][0], positions[i][1]
            body = pm.Body(mass, inertia, pm.Body.DYNAMIC)
            circle = pm.Circle(body, radius)
            body.position = (x, y+distance)
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
            self._catapult_target_bodies = seg, body
        return targets

    def _check_target_collision(self, targets):
        for i, target in enumerate(targets):
            if target[0].body.position != target[1]:
                for num, circle in enumerate(self._shapes_to_draw['circle']):
                    if circle[0] == target[0]:
                        self._shapes_to_draw['circle'].pop(num)
                        targets.pop(i)
                        print('hit')
                        self._shapes_to_draw['circle'].append((circle[0], (255, 0, 0)))
                        self._score += 1
                        return True
        return False

    def _seesaw(self, mass, x_pos, y_pos, w, h, angle=-math.pi/12, offset=(0, 0)):
        seesaw, shape = self._c.create_poly(mass, x_pos, y_pos, w, h, elasticity=0, friction=1, rot=angle)
        constraint = pm.constraints.PivotJoint(seesaw, pm.Body(0.0, 0.0, pm.Body.STATIC), (x_pos+offset[0], y_pos+offset[1]))
        self._shapes_to_draw['rect'].append((shape, (150, 75, 150), w, h))
        self._space.add(constraint)

    def _collapsible_door(self):
        # create the door body and shape
        h = constants.HEIGHT - 5
        mass = 200
        x_pos, y_pos = (4110 + 70, h-320)
        w, h = 140, 10
        door_shapes = []
        for i in range(4):
            body, door_shape = self._c.create_poly(mass, x_pos + 74*2*i, y_pos, w, h)
            self._shapes_to_draw['rect'].append((door_shape, (0, 0, 0), w, h))
            door_shapes.append(door_shape)
        # add constraints
        const1 = pm.constraints.PivotJoint(door_shapes[0].body, pm.Body(0.0, 1, pm.Body.STATIC), (4110, 395))
        const2 = pm.constraints.PivotJoint(door_shapes[3].body, pm.Body(0.0, 1, pm.Body.STATIC), (4700, 395))
        const3 = pm.constraints.PinJoint(door_shapes[0].body, door_shapes[1].body, (70, 0), (-70, 0))
        const4 = pm.constraints.PinJoint(door_shapes[2].body, door_shapes[3].body, (70, 0), (-70, 0))
        # const5 = pm.constraints.PinJoint(door_shapes[1].body, door_shapes[2].body, (70, 0), (-70, 0))
        self._space.add(const1, const2, const3, const4)
        h = constants.HEIGHT - 5
        # create a static body to keep the door raised. Will be deleted to let the tank through
        segments = super()._create_road([((4100, h-308), (4700, h-308))])
        self._door_lock_segment = segments[0]
        # target for player to shoot at to activate the door
        self._collapsible_door_target = self._create_swinging_targets([(4800, 200)])
        self._targets.append(self._collapsible_door_target[0])

    def _ball_pit(self):
        mass, radius = 15, 6
        inertia = inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        position = (3000, constants.HEIGHT - 50)
        for i in range(250):
            body, ball_shape = self._create_ball(mass, inertia, position[0], position[1], radius, friction=0.9)
            self._shapes_to_draw['circle'].append((ball_shape, (0, 0, 200)))

    def _spawn_balls(self):
        mass, radius = 10, 6
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        _curr_time = pg.time.get_ticks()
        position = (9150 + randint(-50, 50), -10 + randint(-25, 25))
        body, ball_shape = self._create_ball(mass, inertia, position[0], position[1], radius, friction=0.7)
        self._shapes_to_draw['circle'].append((ball_shape, (0, 0, 200)))

    def _waterfall_door(self):
        mass = 1000
        x_pos, y_pos = 9680, 470
        w, h = 400, 10
        rot = math.pi/2 + math.pi/16
        body, door_shape = self._c.create_poly(mass, x_pos, y_pos, w, h, rot=rot)
        self._shapes_to_draw['rect'].append((door_shape, (255, 0, 255), w+20, h))
        const1 = pm.constraints.PivotJoint(body, pm.Body(0.0, 1, pm.Body.STATIC), (9640, 480+190))
        const2 = pm.constraints.DampedSpring(body, pm.Body(0.0, 1, pm.Body.STATIC), (-400, 0), (8150, 1820), 50, 100, 100)
        const3 = pm.constraints.PinJoint(body, pm.Body(0.0, 1, pm.Body.STATIC), (-380, 0), (9800, 720))
        self._space.add(const1, const2, const3)
        self._waterfall_door_lock_segment = const3
        self._waterfall_door_target = self._create_swinging_targets([(9550, 50)])
        self._targets.append(self._waterfall_door_target[0])

    def draw(self):
        super().draw()
        # blit the player's score onto the screen
        score = pg.font.SysFont('Consolas', 32).render('Score: {}'.format(self._score), True, pg.color.Color('Black'))
        self._screen.blit(score, (20, 20))

    def _catapult(self):
        self._catapult_target = self._create_swinging_targets([(12900, 300)])
        self._targets.append(self._catapult_target[0])

    def _create_giant_ball(self):
        giant_ball = self._create_swinging_targets([(16500, 0)], mass=100000, radius=300, distance=500)
        self._targets.append(giant_ball[0])

    def update(self):
        super().update()
        self._check_target_collision(self._targets)
        # update state of the collapsable door
        if self._check_target_collision(self._collapsible_door_target):
            self._space.remove(self._door_lock_segment)
        if self._check_target_collision(self._waterfall_door_target):
            self._space.remove(self._waterfall_door_lock_segment)
            self._waterfall = False
        if self._waterfall:
            self._spawn_balls()
        if self._check_target_collision(self._catapult_target):
            body, shape = self._c.create_poly(600000, 12270, 0, 20, 20)
            self._space.remove(self._catapult_target_bodies[0], self._catapult_target_bodies[1])
            self._shapes_to_draw['segment'].pop(-1)
            self._shapes_to_draw['circle'].pop(-1)
            self._shapes_to_draw['rect'].append((shape, (0, 0, 0), 25, 25))

    def build(self):
        self.road()
        self._obstacle_01()
