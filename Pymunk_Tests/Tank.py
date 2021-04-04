import pymunk as pm
import pygame as pg
from Car import Car


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
        shape_filter = pm.ShapeFilter(categories=0b1000)
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        track_bodies_bottom = []
        for num in range(10):
            body, shape = self.create_poly(10, self._track_posx + num*24, self._track_posy, w, h)
            track_bodies_bottom.append(body)
        end_point_1 = self.create_track_constraints(track_bodies_bottom)
        track_bodies_top = []
        for num in range(10):
            body, shape = self.create_poly(10, self._track_posx + num * 24, self._track_posy-40, w, h)
            track_bodies_top.append(body)
        end_point_2 = self.create_track_constraints(track_bodies_top, offset=(0, -40))
        print(end_point_1, end_point_2)
        track_constraint = pm.constraints.PivotJoint(track_bodies_bottom[-1], track_bodies_top[-1], (end_point_1[0], 340))
        self._space.add(track_constraint)
        track_constraint = pm.constraints.PivotJoint(track_bodies_bottom[0], track_bodies_top[0],(track_bodies_bottom[0].position[0], 340))
        self._space.add(track_constraint)




        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        wheel1, shape = self._create_wheel(200, self.x_pos - 79, self.y_pos - 20, 21)
        wheel2, shape = self._create_wheel(200, self.x_pos + 74, self.y_pos - 20, 21)
        wheel3, shape = self._create_wheel(200, self.x_pos + 74, self.y_pos - 20, 21)
        wheel4, shape = self._create_wheel(200, self.x_pos + 74, self.y_pos - 20, 21)
        wheel5, shape = self._create_wheel(200, self.x_pos + 74, self.y_pos - 20, 21)
        self.wheels.append(wheel1)
        self.wheels.append(wheel2)
        self.wheels.append(wheel3)
        self.wheels.append(wheel4)
        self.wheels.append(wheel5)
        # self.create_wheel_contraints(self.body, back_wheel, front_wheel)

    def create_track_constraints(self, track_bodies, offset=(0, 0)):
        end_coords = (0, 0)
        for i, body in enumerate(track_bodies):
            if i == len(track_bodies) - 1:
                break
            pivot_x = self._track_posx + 12 + i * 24 + offset[0]
            pivot_y = self._track_posy+offset[1]
            track_constraint = pm.constraints.PivotJoint(track_bodies[i], track_bodies[i + 1], (pivot_x, pivot_y))
            self._space.add(track_constraint)
            end_coords = (pivot_x + 24, pivot_y)
        return end_coords


    def create_wheel_contraints(self, truck_body, truck_back_wheel, truck_front_wheel):
        pass

    def build(self):
        static_body = self.create_static_segment(
            [(self.x_pos - 400, self.y_pos + 20), (self.x_pos + 400, self.y_pos + 20)])
        return self.create_body_wheels()
