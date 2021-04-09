import pymunk as pm
import pygame as pg
import math


class Car:
    """
    Car superclass. Contains functions shared by all children Car classes.
    """
    def __init__(self, space, screen):
        self._space = space
        self._screen = screen
        self.turret_wheel = None
        self.wheels = []
        self.wheel_image = pg.transform.scale(pg.image.load("mr_car_wheel.png"), (42, 42))
        self.wheel_offset = (0, 0)
        self.body = None
        self.image = None
        self.image_offset = (0, 0)
        self.wheel_turn_force = 10000  # default wheel turn force
        self.max_speed = 100  # default max speed
        self.all_wheel_drive = False  # default all-wheel drive setting

    def _create_wheel(self, mass, x_pos, y_pos, radius, elasticity=0.1, friction=0.9):
        """
        Create a wheel.
        :return: None
        """
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia, pm.Body.DYNAMIC)
        body.position = x_pos, y_pos
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = elasticity
        shape.friction = friction
        shape.filter = pm.ShapeFilter(categories=0b1000)

        self._space.add(body, shape)
        return body, shape

    def create_poly(self, mass, x_pos, y_pos, w, h, vs=0, elasticity=0.3, friction=0.9, color=None, rot=0, s_filter=3):
        """
        Create a polygon. Used to make the body of the car.
        :return: Body and Shape objects
        """
        # default 'box' vertices
        if vs == 0:
            vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        radius = 2.0
        # calculate inertia
        inertia = pm.moment_for_poly(mass, vs, (0, 0), radius=radius)
        # polygon body
        body = pm.Body(mass, inertia)
        body.angle = rot
        # connect the vertices to the body
        shape = pm.Poly(body, vs, radius=1)
        # shape2 = pm.Circle(body, 50, (100, 0))
        # position to print onto screen
        body.position = x_pos, y_pos

        shape.elasticity = elasticity
        shape.friction = friction
        shape.filter = pm.ShapeFilter(categories=s_filter)
        if color:
            shape.color = color
        # shape2.filter = pm.ShapeFilter(categories=0b1000)
        self._space.add(body, shape)
        return body, shape
    
    def update(self):
        keys = pg.key.get_pressed()
        # going forward
        if keys[pg.K_d]:
            # limiting velocity to 500
            if self.wheels[0].velocity.int_tuple[0] < self.max_speed:
                self.wheels[0].apply_force_at_world_point((self.wheel_turn_force, 12), (0, 0))
            # all wheel drive
            if self.all_wheel_drive:
                for i in range(1, len(self.wheels)):
                    if self.wheels[i].velocity.int_tuple[0] < self.max_speed:
                        self.wheels[i].apply_force_at_world_point((self.wheel_turn_force, 12), (0, 0))
        # going backward
        elif keys[pg.K_a]:
            if self.wheels[0].velocity.int_tuple[0] > -self.max_speed:
                self.wheels[0].apply_force_at_world_point((-self.wheel_turn_force, 12), (0, 0))
            if self.all_wheel_drive:
                for i in range(1, len(self.wheels)):
                    if self.wheels[i].velocity.int_tuple[0] > -self.max_speed:
                        self.wheels[i].apply_force_at_world_point((-self.wheel_turn_force, 12), (0, 0))

    def draw(self):
        """
        Draws the car body and wheels onto the screen. Limit the x-pos of the car
        to half of the screen width.
        :return: None
        """
        # center coordinates of the car body in pm-space
        car_body_center = self.body.position
        # drawing front and back wheels
        for i in range(len(self.wheels)):
            rot = -math.degrees(self.wheels[i].angle)
            # grab loaded image
            image = pg.transform.rotate(self.wheel_image, rot)
            center = self.wheels[i].position
            rect = image.get_rect(center=image.get_rect(center=center).center)
            # shift the x-pos of the wheel by (x-cord of the car body) - 400
            if car_body_center[0] > 400 + -self.wheel_offset[0]:
                rect.centerx -= car_body_center[0] - 400 + self.wheel_offset[0]
            # draw the car body onto the screen
            self._screen.blit(image, rect)
        # get rotation of the car body or wheel
        car_body_rot = -math.degrees(self.body.angle)
        # grab loaded image
        image = pg.transform.rotate(self.image, car_body_rot)
        center = image.get_rect(center=car_body_center).center
        car_body_rect = image.get_rect(center=(center[0]+self.image_offset[0], center[1]+self.image_offset[1]))
        if car_body_rect.centerx > 400:
            car_body_rect.centerx = 400
        # draw the car body onto the screen in front of the wheels
        self._screen.blit(image, car_body_rect)

