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
        w = 200
        h = 80
        shape_filter = pm.ShapeFilter(categories=0b1000)
        # mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9
        truck_body, shape = self._create_poly(200, self.x_pos, self.y_pos, w, h)
        # mass, x_pos, y_pos, radius, elasticity=0.3, friction=0.9
        truck_back_wheel, shape = self._create_wheel(20, self.x_pos - w/2, self.y_pos + h / 2, h / 2)
        truck_front_wheel, shape = self._create_wheel(20, self.x_pos + w / 2, self.y_pos + h / 2, h / 2)
        self.create_wheel_contraints(truck_body, truck_back_wheel, truck_front_wheel)

    def create_wheel_contraints(self, truck_body, truck_back_wheel, truck_front_wheel):
        g, p = (80, 10)
        back_wheel_dspring = pm.constraints.DampedSpring(truck_body, truck_back_wheel, (-80, 20), (0, 0), 20, 200, 1)
        front_wheel_dspring = pm.constraints.DampedSpring(truck_body, truck_front_wheel, (80, 20), (0, 0), 20, 200, 1)
        back_wheel_slide_joint_1 = pm.constraints.SlideJoint(truck_body, truck_back_wheel, (-40, 20), (0, 0), g, p)
        back_wheel_slide_joint_2 = pm.constraints.SlideJoint(truck_body, truck_back_wheel, (-100, 20), (0, 0), g, p)
        front_wheel_slide_joint_1 = pm.constraints.SlideJoint(truck_body, truck_front_wheel, (40, 20), (0, 0), g, p)
        front_wheel_slide_joint_2 = pm.constraints.SlideJoint(truck_body, truck_front_wheel, (100, 20), (0, 0), g, p)
        self._space.add(back_wheel_dspring)
        self._space.add(front_wheel_dspring)
        self._space.add(back_wheel_slide_joint_1)
        self._space.add(back_wheel_slide_joint_2)
        self._space.add(front_wheel_slide_joint_1)
        self._space.add(front_wheel_slide_joint_2)


    def build(self):
        self.create_body_wheels()
