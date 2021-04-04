import pymunk as pm
import pygame as pg
from Car import Car
import math


class Tank(Car):
    """
    Create a Truck body and wheels and insert into the Space.
    Return all the information needed to blit the truck image onto the screen.
    """
    def __init__(self, space, x_pos, y_pos):
        super().__init__(space)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.body = None
        self.wheels = []
        self.wheel_turn_force = 50000
        self.max_speed = 500
        self.all_wheel_drive = True
        self._track_posx = x_pos - 100
        self._track_posy = y_pos
        # self.image = pg.image.load("images/")
        # offset for the center of the car

    def create_static_segment(self, vs, radius=5):
        static_body = pm.Body(body_type=pm.Body.STATIC)
        seg = pm.Segment(static_body, vs[0], vs[1], radius)
        seg.elasticity = 0.10
        seg.friction = 0.90
        self._space.add(static_body)
        self._space.add(seg)
        return static_body

    def create_body_wheels(self):
        w = 20
        h = 6
        mass = 30
        shape_filter = pm.ShapeFilter(categories=0b1000)
        print(self._track_posx, self._track_posy)
        tank_body, shape = self.create_poly(2000, self._track_posx + 140, self._track_posy-80, 460, 40)
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        track_bodies_bottom = []
        for num in range(12):
            body, shape = self.create_poly(mass, self._track_posx + num*28, self._track_posy, w, h)
            track_bodies_bottom.append(body)
        end_point_1 = self.create_track_constraints(track_bodies_bottom)
        track_bodies_top = []
        for num in range(14):
            body, shape = self.create_poly(mass, self._track_posx-50 + num * 28, self._track_posy-40, w, h)
            track_bodies_top.append(body)
        end_point_2 = self.create_track_constraints(track_bodies_top, offset=(-50, -40))

        body1, shape = self.create_poly(mass, self._track_posx+337, self._track_posy-29, w, h, rot=-11*math.pi/16)
        track_constraint1 = pm.constraints.PivotJoint(body1, track_bodies_top[-1] , (self._track_posx+330, self._track_posy-40))
        body2 , shape = self.create_poly(mass, self._track_posx+334, self._track_posy-6, w, h, rot=12*math.pi/16)
        track_constraint2 = pm.constraints.PivotJoint(body1, body2, (self._track_posx+345, self._track_posy-16))
        track_constraint3 = pm.constraints.PivotJoint(body2, track_bodies_bottom[-1], (self._track_posx+324, self._track_posy))
        self._space.add(track_constraint1, track_constraint2, track_constraint3)

        body1, shape = self.create_poly(mass, self._track_posx-72, self._track_posy-28, w, h, rot=11 * math.pi / 16)
        track_constraint1 = pm.constraints.PivotJoint(body1, track_bodies_top[0], (self._track_posx-63, self._track_posy-39))
        body2, shape = self.create_poly(mass, self._track_posx-69, self._track_posy-7, w, h, rot=-12 * math.pi / 16)
        track_constraint2 = pm.constraints.PivotJoint(body1, body2, (self._track_posx-77, self._track_posy-17))
        body3, shape = self.create_poly(mass, self._track_posx-47, self._track_posy-3, w, h, rot=-2 * math.pi / 16)
        track_constraint3 = pm.constraints.PivotJoint(body2, body3, (self._track_posx-59, self._track_posy+2))
        body4, shape = self.create_poly(mass, self._track_posx-24, self._track_posy-4, w, h, rot=2 * math.pi / 16)
        track_constraint4 = pm.constraints.PivotJoint(body3, body4, (self._track_posx-35, self._track_posy-8))
        track_constraint5 = pm.constraints.PivotJoint(body4, track_bodies_bottom[0], (self._track_posx-12, self._track_posy))
        self._space.add(track_constraint1, track_constraint2, track_constraint3, track_constraint4, track_constraint5)

        x, y = self._track_posx, self._track_posy
        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        wheel1, shape = self._create_wheel(50, x - 54, y - 20, 15)
        wheel2, shape = self._create_wheel(50, x + 321, y - 20, 15)
        wheel3, shape = self._create_wheel(50, x - 8, y - 5, 15)
        # wheel4, shape = self._create_wheel(50, self.x_pos + 74, self.y_pos - 20, 21)
        # wheel5, shape = self._create_wheel(50, self.x_pos + 74, self.y_pos - 20, 21)
        # wheel6, shape = self._create_wheel(50, self.x_pos + 74, self.y_pos - 20, 21)
        # wheel7, shape = self._create_wheel(50, self.x_pos + 74, self.y_pos - 20, 21)
        # wheel8, shape = self._create_wheel(50, self.x_pos + 74, self.y_pos - 20, 21)
        # wheel9, shape = self._create_wheel(50, self.x_pos + 74, self.y_pos - 20, 21)
        self.wheels.append(wheel1)
        self.wheels.append(wheel2)
        # self.wheels.append(wheel3)
        # self.wheels.append(wheel4)
        # self.wheels.append(wheel5)
        # self.wheels.append(wheel6)
        # self.wheels.append(wheel7)
        # self.wheels.append(wheel8)
        # self.wheels.append(wheel9)
        # self.create_wheel_contraints(self.body, back_wheel, front_wheel)

        const1 = pm.constraints.PinJoint(tank_body, wheel1, (-220, 0), (0, 0))
        const2 = pm.constraints.PinJoint(tank_body, wheel2, (220, 0), (0, 0))
        const3 = pm.constraints.PinJoint(tank_body, wheel1, (0, 0), (0, 0))
        const4 = pm.constraints.PinJoint(tank_body, wheel2, (0, 0), (0, 0))
        const5 = pm.constraints.PinJoint(tank_body, wheel3, (-145, 0), (0, 0))
        const6 = pm.constraints.PinJoint(wheel1, wheel3, (0, 0), (0, 0))
        self._space.add(const1, const2, const3, const4, const5, const6)

    def create_track_constraints(self, track_bodies, offset=(0, 0)):
        end_coords = (0, 0)
        for i, body in enumerate(track_bodies):
            if i == len(track_bodies) - 1:
                break
            pivot_x = self._track_posx + 14 + i * 28 + offset[0]
            pivot_y = self._track_posy+offset[1]
            track_constraint = pm.constraints.PivotJoint(track_bodies[i], track_bodies[i + 1], (pivot_x, pivot_y))
            self._space.add(track_constraint)
            end_coords = (pivot_x + 28, pivot_y)
        return end_coords


    def create_wheel_contraints(self, truck_body, truck_back_wheel, truck_front_wheel):
        pass

    def build(self):
        static_body = self.create_static_segment(
            [(self.x_pos - 400, self.y_pos + 20), (self.x_pos + 400, self.y_pos + 20)])
        return self.create_body_wheels()
