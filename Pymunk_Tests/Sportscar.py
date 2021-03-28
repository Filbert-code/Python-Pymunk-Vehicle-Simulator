import pymunk as pm
from Car import Car


class Sportscar(Car):
    """
    Create a Truck body and wheels and insert into the Space.
    Return all the information needed to blit the truck image onto the screen.
    """
    def __init__(self, space, x_pos, y_pos):
        super().__init__(space)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self._body = None
        self._wheels = []

    def create_body_wheels(self):
        w = 250
        h = 70
        shape_filter = pm.ShapeFilter(categories=0b1000)
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        vs = [(-40, 34), (-40, 0), (-25, -35), (0, -35), (55, 12), (66, 34)]
        self._body, shape = self._create_poly(1000, self.x_pos, self.y_pos, w, h, vs=vs)
        # vs = [(), (), (), (), ()]
        # car_shape_1 = pm.Poly(car_body, vs, radius=1)
        # vs = [(), (), (), (), ()]
        # car_shape_2 = pm.Poly(car_body, vs, radius=1)
        # vs = [(), (), (), (), ()]
        # car_shape_3 = pm.Poly(car_body, vs, radius=1)
        # vs = [(), (), (), (), ()]
        # car_shape_4 = pm.Poly(car_body, vs, radius=1)
        # vs = [(), (), (), (), ()]
        # car_shape_5 = pm.Poly(car_body, vs, radius=1)
        # vs = [(), (), (), (), ()]
        # car_shape_6 = pm.Poly(car_body, vs, radius=1)
        # self._space.add(car_shape_1)
        # self._space.add(car_shape_2)
        # self._space.add(car_shape_3)
        # self._space.add(car_shape_4)
        # self._space.add(car_shape_5)
        # self._space.add(car_shape_6)

        # create car wheels
        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        back_wheel, shape = self._create_wheel(200, self.x_pos - 79, self.y_pos + 25, 21)
        front_wheel, shape = self._create_wheel(200, self.x_pos + 74, self.y_pos + 25, 21)
        self._wheels.append(back_wheel)
        self._wheels.append(front_wheel)
        # self.create_wheel_contraints(truck_body, truck_back_wheel, truck_front_wheel)
        # return truck_back_wheel, truck_front_wheel, truck_body

    # def create_wheel_contraints(self, truck_body, truck_back_wheel, truck_front_wheel):
    #     spring_strength = 170000
    #
    #     back_wheel_dspring_1 = pm.constraints.DampedSpring(
    #         truck_body, truck_back_wheel, (-108, 20), (0, 0), 42, spring_strength, 1
    #     )
    #     back_wheel_dspring_slide_joint_1 = pm.constraints.SlideJoint(
    #         truck_body, truck_back_wheel, (-108, 20), (0, 0), 42, 48
    #     )
    #     back_wheel_dspring_2 = pm.constraints.DampedSpring(
    #         truck_body, truck_back_wheel, (-50, 20), (0, 0), 42, spring_strength, 1
    #     )
    #     back_wheel_dspring_slide_joint_2 = pm.constraints.SlideJoint(
    #         truck_body, truck_back_wheel, (-50, 20), (0, 0), 42, 48
    #     )
    #     front_wheel_dspring_1 = pm.constraints.DampedSpring(
    #         truck_body, truck_front_wheel, (45, 20), (0, 0), 42, spring_strength, 1
    #     )
    #     front_wheel_dspring_slide_joint_1 = pm.constraints.SlideJoint(
    #         truck_body, truck_front_wheel, (45, 20), (0, 0), 42, 48
    #     )
    #     front_wheel_dspring_2 = pm.constraints.DampedSpring(
    #         truck_body, truck_front_wheel, (103, 20), (0, 0), 42, spring_strength, 1
    #     )
    #     front_wheel_dspring_slide_joint_2 = pm.constraints.SlideJoint(
    #         truck_body, truck_front_wheel, (103, 20), (0, 0),42, 48
    #     )
    #
    #     back_wheel_slide_joint = pm.constraints.SlideJoint(
    #         truck_body, truck_back_wheel, (-79, 20), (0, 0), 30, 35
    #     )
    #     front_wheel_slide_joint = pm.constraints.SlideJoint(
    #         truck_body, truck_front_wheel, (74, 20), (0, 0), 30, 35
    #     )
    #     self._space.add(back_wheel_dspring_1)
    #     self._space.add(back_wheel_dspring_2)
    #     self._space.add(front_wheel_dspring_1)
    #     self._space.add(front_wheel_dspring_2)
    #     self._space.add(back_wheel_slide_joint)
    #     self._space.add(front_wheel_slide_joint)
    #     self._space.add(back_wheel_dspring_slide_joint_1)
    #     self._space.add(back_wheel_dspring_slide_joint_2)
    #     self._space.add(front_wheel_dspring_slide_joint_1)
    #     self._space.add(front_wheel_dspring_slide_joint_2)

    def build(self):
        return self.create_body_wheels()
