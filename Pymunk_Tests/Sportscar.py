import pymunk as pm
import pygame as pg
from Car import Car


class Sportscar(Car):
    """
    Create a Sportscar body and wheels and insert into the Space.
    Return all the information needed to blit the truck image onto the screen.
    """
    def __init__(self, space, x_pos, y_pos):
        super().__init__(space)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.body = None
        self.wheels = []
        self.wheel_turn_force = 36000
        self.max_speed = 1200
        self.all_wheel_drive = False
        self.image = pg.image.load("images/Sportscar1.2.png")
        # offset for the center of the car

    def create_body_wheels(self):
        w = 250
        h = 70
        shape_filter = pm.ShapeFilter(categories=0b1000)
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        vs = [(-37, 34), (-37, 0), (-25, -35), (0, -35), (55, -12), (66, 34)]
        self.body, shape = self.create_poly(1000, self.x_pos, self.y_pos, w, h, vs=vs)
        vs = [(55, -12), (66, 34), (73, -13), (73, 28)]
        car_shape_1 = pm.Poly(self.body, vs, radius=1)
        vs = [(73, -13), (73, 0), (91, -12), (124, -9), (130, 0)]
        car_shape_2 = pm.Poly(self.body, vs, radius=1)
        vs = [(124, -9), (130, 0), (146, 3), (150, 34), (130, 34)]
        car_shape_3 = pm.Poly(self.body, vs, radius=1)
        vs = [(-25, -35), (-37, 0), (-91, -16), (-91, 0)]
        car_shape_4 = pm.Poly(self.body, vs, radius=1)
        vs = [(-91, -16), (-91, 31), (-95, 30), (-95, -16)]
        car_shape_5 = pm.Poly(self.body, vs, radius=1)
        vs = [(-95, -16), (-110, -16), (-113, 26), (-95, 30)]
        car_shape_6 = pm.Poly(self.body, vs, radius=1)
        vs = [(-95, -16), (-89, -19), (-117, -24), (-110, -16)]
        car_shape_7 = pm.Poly(self.body, vs, radius=1)
        vs = [(-110, -16), (-113, 26), (-124, 15)]
        car_shape_8 = pm.Poly(self.body, vs, radius=1)
        self._space.add(car_shape_1)
        self._space.add(car_shape_2)
        self._space.add(car_shape_3)
        self._space.add(car_shape_4)
        self._space.add(car_shape_5)
        self._space.add(car_shape_6)
        self._space.add(car_shape_7)
        self._space.add(car_shape_8)

        # create car wheels
        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        back_wheel, shape = self._create_wheel(200, self.x_pos - 70, self.y_pos + 27, 21, friction=2)
        front_wheel, shape = self._create_wheel(200, self.x_pos + 99, self.y_pos + 27, 21, friction=2)
        self.wheels.append(back_wheel)
        self.wheels.append(front_wheel)
        self.create_wheel_contraints(self.body, self.wheels[0], self.wheels[1])

    def create_wheel_contraints(self, body, back_wheel, front_wheel):
        spring_strength = 270000

        back_wheel_dspring_1 = pm.constraints.DampedSpring(
            body, back_wheel, (-91, 0), (0, 0), 42, spring_strength, 1
        )
        back_wheel_dspring_slide_joint_1 = pm.constraints.SlideJoint(
            body, back_wheel, (-91, 0), (0, 0), 42, 48
        )
        back_wheel_dspring_2 = pm.constraints.DampedSpring(
            body, back_wheel, (-33, 0), (0, 0), 42, spring_strength, 1
        )
        back_wheel_dspring_slide_joint_2 = pm.constraints.SlideJoint(
            body, back_wheel, (-33, 0), (0, 0), 42, 48
        )
        back_wheel_slide_joint = pm.constraints.SlideJoint(
            body, back_wheel, (-62, 0), (0, 0), 30, 35
        )
        front_wheel_dspring_1 = pm.constraints.DampedSpring(
            body, front_wheel, (74, 0), (0, 0), 42, spring_strength, 1
        )
        front_wheel_dspring_slide_joint_1 = pm.constraints.SlideJoint(
            body, front_wheel, (74, 0), (0, 0), 42, 48
        )
        front_wheel_dspring_2 = pm.constraints.DampedSpring(
            body, front_wheel, (132, 0), (0, 0), 42, spring_strength, 1
        )
        front_wheel_dspring_slide_joint_2 = pm.constraints.SlideJoint(
            body, front_wheel, (132, 0), (0, 0),42, 48
        )
        front_wheel_slide_joint = pm.constraints.SlideJoint(
            body, front_wheel, (103, 0), (0, 0), 30, 35
        )
        self._space.add(back_wheel_dspring_1)
        self._space.add(back_wheel_dspring_2)
        self._space.add(front_wheel_dspring_1)
        self._space.add(front_wheel_dspring_2)
        self._space.add(back_wheel_slide_joint)
        self._space.add(front_wheel_slide_joint)
        self._space.add(back_wheel_dspring_slide_joint_1)
        self._space.add(back_wheel_dspring_slide_joint_2)
        self._space.add(front_wheel_dspring_slide_joint_1)
        self._space.add(front_wheel_dspring_slide_joint_2)

    def build(self):
        return self.create_body_wheels()
