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
        self.wheel_turn_force = 30000
        self.max_speed = 150
        self.all_wheel_drive = True
        self._track_posx = x_pos - 100
        self._track_posy = y_pos
        self.turret_wheel_angle = 0
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
        w = 12
        h = 4
        mass = 200
        shape_filter = pm.ShapeFilter(categories=0b1000)
        print(self._track_posx, self._track_posy)
        tank_body, shape = self.create_poly(5000, self._track_posx + 140, self._track_posy-80, 90, 40, elasticity=0)
        w2, h2 = 180, 40
        vs = [(-w2 / 2, -h2 / 2), (w2 / 2, -h2 / 2), (w2 / 2, h2 / 2), (-w2 / 2, h2 / 2)]
        tank_shape1 = pm.Poly(tank_body, vs, radius=1, transform=pm.Transform.translation(-135, 0))
        self._space.add(tank_shape1)
        self.body = tank_body
        self.turret_wheel, self.turret_wheel_shape = self._create_wheel(5000, self._track_posx + 208, self._track_posy-80, 18, elasticity=0, friction=1)
        turret_wheel_const1 = pm.constraints.PinJoint(tank_body, self.turret_wheel, (0, -20), (0, 0))
        turret_wheel_const2 = pm.constraints.PinJoint(tank_body, self.turret_wheel, (0, 20), (0, 0))
        tank_turret, shape = self.create_poly(200, self._track_posx + 310, self._track_posy-80, 140, 13, elasticity=0)
        turret_const1 = pm.constraints.PivotJoint(self.turret_wheel, tank_turret, (self._track_posx + 208, self._track_posy-80))
        turret_const2 = pm.constraints.GearJoint(self.turret_wheel, tank_turret, 0.0, 300.0)
        self._space.add(turret_wheel_const1, turret_wheel_const2, turret_const1, turret_const2)

        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        track_bodies_bottom = []
        for num in range(22):
            body, shape = self.create_poly(mass, self._track_posx-25 + num*14, self._track_posy, w, h, elasticity=0)
            track_bodies_bottom.append(body)
        end_point_1 = self.create_track_constraints(track_bodies_bottom, offset=(-25, 0))
        track_bodies_top = []
        for num in range(26):
            body, shape = self.create_poly(mass, self._track_posx-50 + num * 14, self._track_posy-40, w, h, elasticity=0)
            track_bodies_top.append(body)
        end_point_2 = self.create_track_constraints(track_bodies_top, offset=(-50, -40))

        body1, shape = self.create_poly(mass, self._track_posx+304, self._track_posy-31, w+2, h, rot=11*math.pi/16, elasticity=0)
        track_constraint1 = pm.constraints.PivotJoint(body1, track_bodies_top[-1] , (self._track_posx+307, self._track_posy-39))
        body2 , shape = self.create_poly(mass, self._track_posx+295, self._track_posy-18, w+2, h, rot=12*math.pi/16, elasticity=0)
        track_constraint2 = pm.constraints.PivotJoint(body1, body2, (self._track_posx+302, self._track_posy-24))
        body3, shape = self.create_poly(mass, self._track_posx + 284, self._track_posy - 5, w+2, h,rot=12 * math.pi / 16, elasticity=0)
        track_constraint3 = pm.constraints.PivotJoint(body2, body3, (self._track_posx + 290, self._track_posy - 11))
        track_constraint4 = pm.constraints.PivotJoint(body3, track_bodies_bottom[-1], (self._track_posx+280, self._track_posy))
        self._space.add(track_constraint1, track_constraint2, track_constraint3, track_constraint4)

        body1, shape = self.create_poly(mass, self._track_posx-57, self._track_posy-32, w, h, rot=-11 * math.pi / 16, elasticity=0)
        track_constraint1 = pm.constraints.PivotJoint(body1, track_bodies_top[0], (self._track_posx-59, self._track_posy-39))
        body2, shape = self.create_poly(mass, self._track_posx-48, self._track_posy-21, w, h, rot=-12 * math.pi / 16, elasticity=0)
        track_constraint2 = pm.constraints.PivotJoint(body1, body2, (self._track_posx-53, self._track_posy-26))
        body3, shape = self.create_poly(mass, self._track_posx-38, self._track_posy-8, w+2, h, rot=-11 * math.pi / 16, elasticity=0)
        track_constraint3 = pm.constraints.PivotJoint(body2, body3, (self._track_posx-40, self._track_posy-13))
        track_constraint4 = pm.constraints.PivotJoint(body3, track_bodies_bottom[0], (self._track_posx-32, self._track_posy))
        self._space.add(track_constraint1, track_constraint2, track_constraint3, track_constraint4)

        x, y = self._track_posx, self._track_posy
        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        # small_wheel1, shape = self._create_wheel(50, x - 10, y - 45, 14, elasticity=0, friction=1)
        # small_wheel2, shape = self._create_wheel(50, x + 245, y - 50, 12, elasticity=0, friction=1)
        small_wheel3, shape = self._create_wheel(50, x + 76, y - 42, 14, elasticity=0, friction=1)
        small_wheel4, shape = self._create_wheel(50, x + 160, y - 42, 14, elasticity=0, friction=1)
        wheel1, shape = self._create_wheel(50, x - 46, y - 20, 15, elasticity=0, friction=1)
        wheel2, shape = self._create_wheel(50, x + 295, y - 20, 15, elasticity=0, friction=1)
        wheel3, shape = self._create_wheel(50, x + 138, y - 3, 18, elasticity=0, friction=1)
        wheel4, shape = self._create_wheel(50, x + 180, y - 3, 18, elasticity=0, friction=1)
        wheel5, shape = self._create_wheel(50, x + 96, y - 3, 18, elasticity=0, friction=1)
        wheel6, shape = self._create_wheel(50, x + 264, y - 3, 16, elasticity=0, friction=1)
        wheel7, shape = self._create_wheel(50, x + 12, y - 3, 18, elasticity=0, friction=1)
        wheel8, shape = self._create_wheel(50, x + 222, y - 3, 18, elasticity=0, friction=1)
        wheel9, shape = self._create_wheel(50, x + 54, y - 3, 18, elasticity=0, friction=1)
        # self.wheels.append(small_wheel1)
        # self.wheels.append(small_wheel2)
        self.wheels.append(small_wheel3)
        self.wheels.append(small_wheel4)
        self.wheels.append(wheel1)
        self.wheels.append(wheel2)
        self.wheels.append(wheel3)
        self.wheels.append(wheel4)
        self.wheels.append(wheel5)
        self.wheels.append(wheel6)
        self.wheels.append(wheel7)
        self.wheels.append(wheel8)
        self.wheels.append(wheel9)
        _min = 74
        _max = 82
        # top-left small wheel
        # small_const1 = pm.constraints.PinJoint(wheel1, small_wheel1, (0, 0), (0, 0))
        # small_const2 = pm.constraints.PinJoint(wheel2, small_wheel1, (0, 0), (0, 0))
        # small_const3 = pm.constraints.SlideJoint(tank_body, small_wheel1, (-160, 0), (0, 0), 40, 40)
        # small_const4 = pm.constraints.PinJoint(tank_body, small_wheel1, (0, 0), (0, 0))
        # # top-right small wheel
        # small_const5 = pm.constraints.PinJoint(wheel1, small_wheel2, (0, 0), (0, 0))
        # small_const6 = pm.constraints.PinJoint(wheel2, small_wheel2, (0, 0), (0, 0))
        # small_const7 = pm.constraints.SlideJoint(tank_body, small_wheel2, (105, 0), (0, 0), 38, 38)
        # small_const8 = pm.constraints.PinJoint(tank_body, small_wheel2, (0, 0), (0, 0))
        # middle-left small wheel
        small_const9 = pm.constraints.PinJoint(wheel1, small_wheel3, (0, 0), (0, 0))
        small_const10 = pm.constraints.PinJoint(wheel2, small_wheel3, (0, 0), (0, 0))
        small_const11 = pm.constraints.PinJoint(tank_body, small_wheel3, (-64, 0), (0, 0))
        small_const12 = pm.constraints.PinJoint(tank_body, small_wheel3, (0, 0), (0, 0))
        # middle-right small wheel
        small_const13 = pm.constraints.PinJoint(wheel1, small_wheel4, (0, 0), (0, 0))
        small_const14 = pm.constraints.PinJoint(wheel2, small_wheel4, (0, 0), (0, 0))
        small_const15 = pm.constraints.PinJoint(tank_body, small_wheel4, (22, 0), (0, 0))
        small_const16 = pm.constraints.PinJoint(tank_body, small_wheel4, (0, 0), (0, 0))
        # connect far-left and far-right wheel
        # const0 = pm.constraints.PinJoint(wheel2, wheel1, (0, 0), (0, 0))
        # far-left wheel
        const1 = pm.constraints.PinJoint(tank_body, wheel1, (-220, 0), (0, 0))
        const3 = pm.constraints.PinJoint(tank_body, wheel1, (0, 0), (0, 0))
        # far-right wheel
        const2 = pm.constraints.PinJoint(tank_body, wheel2, (220, 0), (0, 0))
        const4 = pm.constraints.PinJoint(tank_body, wheel2, (0, 0), (0, 0))
        # middle wheel
        const5 = pm.constraints.SlideJoint(tank_body, wheel3, (0, 0), (0, 0), _min, _max)
        const6 = pm.constraints.PinJoint(tank_body, wheel3, (-100, 0), (0, 0))
        const7 = pm.constraints.PinJoint(tank_body, wheel3, (100, 0), (0, 0))
        # middle right
        const8 = pm.constraints.SlideJoint(tank_body, wheel4, (42, 0), (0, 0), _min, _max)
        const9 = pm.constraints.PinJoint(tank_body, wheel4, (42-100, 0), (0, 0))
        const10 = pm.constraints.PinJoint(tank_body, wheel4, (42+100, 0), (0, 0))
        # middle left
        const11 = pm.constraints.SlideJoint(tank_body, wheel5, (-42, 0), (0, 0), _min, _max)
        const12 = pm.constraints.PinJoint(tank_body, wheel5, (-42-100, 0), (0, 0))
        const13 = pm.constraints.PinJoint(tank_body, wheel5, (-42+100, 0), (0, 0))
        # second from far right
        const14 = pm.constraints.SlideJoint(tank_body, wheel6, (126, 0), (0, 0), _min, _max)
        const15 = pm.constraints.PinJoint(tank_body, wheel6, (126-100, 0), (0, 0))
        const16 = pm.constraints.PinJoint(tank_body, wheel6, (126+100, 0), (0, 0))
        # second from far left
        const17 = pm.constraints.SlideJoint(tank_body, wheel7, (-126, 0), (0, 0), _min, _max)
        const18 = pm.constraints.PinJoint(tank_body, wheel7, (-126-100, 0), (0, 0))
        const19 = pm.constraints.PinJoint(tank_body, wheel7, (-126+100, 0), (0, 0))
        #
        const20 = pm.constraints.SlideJoint(tank_body, wheel8, (84, 0), (0, 0), _min, _max)
        const21 = pm.constraints.PinJoint(tank_body, wheel8, (84-100, 0), (0, 0))
        const22 = pm.constraints.PinJoint(tank_body, wheel8, (84+100, 0), (0, 0))
        # second from far left
        const23 = pm.constraints.SlideJoint(tank_body, wheel9, (-84, 0), (0, 0), _min, _max)
        const24 = pm.constraints.PinJoint(tank_body, wheel9, (-84-100, 0), (0, 0))
        const25 = pm.constraints.PinJoint(tank_body, wheel9, (-84+100, 0), (0, 0))
        # self._space.add(small_const1, small_const2, small_const3, small_const4)
        # self._space.add(small_const5, small_const6, small_const7, small_const8)
        self._space.add(small_const9, small_const10, small_const11, small_const12)
        self._space.add(small_const13, small_const14, small_const15, small_const16)
        self._space.add( const1, const2, const3, const4, const5, const6, const7)
        self._space.add(const8, const9, const10, const11, const12, const13, const14, const15, const16)
        self._space.add(const17, const18, const19)
        self._space.add(const20, const21, const22)
        self._space.add(const23, const24, const25)

    def create_track_constraints(self, track_bodies, offset=(0, 0)):
        end_coords = (0, 0)
        for i, body in enumerate(track_bodies):
            if i == len(track_bodies) - 1:
                break
            pivot_x = self._track_posx + 8 + i * 14 + offset[0]
            pivot_y = self._track_posy+offset[1]
            track_constraint = pm.constraints.PivotJoint(track_bodies[i], track_bodies[i + 1], (pivot_x, pivot_y))
            track_constraint.max_force = 80000000
            self._space.add(track_constraint)
            end_coords = (pivot_x + 28, pivot_y)
        return end_coords

    def create_wheel_contraints(self, truck_body, truck_back_wheel, truck_front_wheel):
        pass

    def build(self):
        self.create_static_segment(
            [(self.x_pos - 400, self.y_pos + 20), (self.x_pos + 300, self.y_pos + 20)])
        self.create_static_segment(
            [(self.x_pos + 300, self.y_pos + 20), (self.x_pos + 600, self.y_pos - 100)])
        self.create_static_segment(
            [(self.x_pos + 600, self.y_pos - 100), (self.x_pos + 900, self.y_pos + 20)])
        return self.create_body_wheels()
