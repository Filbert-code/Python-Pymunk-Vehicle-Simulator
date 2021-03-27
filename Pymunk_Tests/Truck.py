import pymunk as pm
from Car import Car


class Truck(Car):
    """
    Create a Truck body and wheels and insert into the Space.
    Return all the information needed to blit the truck image onto the screen.
    """
    def __init__(self, space, x_pos, y_pos):
        super().__init__(space)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def create_body_wheels(self):
        w = 250
        h = 80
        shape_filter = pm.ShapeFilter(categories=0b1000)
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        vs = [(-15, -h/2), (30, -h/2), (50, -20), (-20, 0), (-20, h/2), (50, h/2)]
        truck_body, shape = self._create_poly(3000, self.x_pos, self.y_pos, w, h, vs=vs)
        vs = [(50, -20), (62, -10), (62, 20), (50, 20)]
        truck_shape_1 = pm.Poly(truck_body, vs, radius=1)
        vs = [(62, -10), (62, 20), (98, -5), (98, 20)]
        truck_shape_2 = pm.Poly(truck_body, vs, radius=1)
        vs = [(98, -5), (125, 0), (125, 40), (98, 40)]
        truck_shape_3 = pm.Poly(truck_body, vs, radius=1)
        vs = [(-55, 40), (-55, 0), (-20, 0), (-20, 40)]
        truck_shape_4 = pm.Poly(truck_body, vs, radius=1)
        vs = [(-103, 20), (-103, 0), (-55, 20), (-55, 0)]
        truck_shape_5 = pm.Poly(truck_body, vs, radius=1)
        vs = [(-125, 0), (-125, 40), (-103, 0), (-103, 40)]
        truck_shape_6 = pm.Poly(truck_body, vs, radius=1)
        self._space.add(truck_shape_1)
        self._space.add(truck_shape_2)
        self._space.add(truck_shape_3)
        self._space.add(truck_shape_4)
        self._space.add(truck_shape_5)
        self._space.add(truck_shape_6)

        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        truck_back_wheel, shape = self._create_wheel(200, self.x_pos - 79, self.y_pos + 25, 21)
        truck_front_wheel, shape = self._create_wheel(200, self.x_pos + 74, self.y_pos + 25, 21)
        self.create_wheel_contraints(truck_body, truck_back_wheel, truck_front_wheel)
        return truck_back_wheel, truck_front_wheel, truck_body

    def create_wheel_contraints(self, truck_body, truck_back_wheel, truck_front_wheel):
        spring_strength = 70000

        back_wheel_dspring_1 = pm.constraints.DampedSpring(
            truck_body, truck_back_wheel, (-108, 20), (0, 0), 42, spring_strength, 1
        )
        back_wheel_dspring_slide_joint_1 = pm.constraints.SlideJoint(
            truck_body, truck_back_wheel, (-108, 20), (0, 0), 42, 48
        )
        back_wheel_dspring_2 = pm.constraints.DampedSpring(
            truck_body, truck_back_wheel, (-50, 20), (0, 0), 42, spring_strength, 1
        )
        back_wheel_dspring_slide_joint_2 = pm.constraints.SlideJoint(
            truck_body, truck_back_wheel, (-50, 20), (0, 0), 42, 48
        )
        front_wheel_dspring_1 = pm.constraints.DampedSpring(
            truck_body, truck_front_wheel, (45, 20), (0, 0), 42, spring_strength, 1
        )
        front_wheel_dspring_slide_joint_1 = pm.constraints.SlideJoint(
            truck_body, truck_front_wheel, (45, 20), (0, 0), 42, 48
        )
        front_wheel_dspring_2 = pm.constraints.DampedSpring(
            truck_body, truck_front_wheel, (103, 20), (0, 0), 42, spring_strength, 1
        )
        front_wheel_dspring_slide_joint_2 = pm.constraints.SlideJoint(
            truck_body, truck_front_wheel, (103, 20), (0, 0),42, 48
        )

        back_wheel_slide_joint = pm.constraints.SlideJoint(
            truck_body, truck_back_wheel, (-79, 20), (0, 0), 30, 35
        )
        front_wheel_slide_joint = pm.constraints.SlideJoint(
            truck_body, truck_front_wheel, (74, 20), (0, 0), 30, 35
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
