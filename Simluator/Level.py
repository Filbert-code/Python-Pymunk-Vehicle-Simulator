import pymunk as pm
import pygame as pg
from Car import Car
from RoadBuilder import RoadBuilder
import constants
import math


class Level:
    def __init__(self, space, screen, car):
        self._space = space
        self._screen = screen
        self._car = car
        self._rb = RoadBuilder(self._space)
        self._c = Car(self._space, screen)
        # different generic shapes include: rectangle, circle, and segment(line)
        self._shapes_to_draw = {'rect': [], 'circle': [], 'segment': []}

    def _create_road(self, vs):
        _road_body, segments = self._rb.build_road(vs, 5)
        return segments

    def _create_ball(self, _mass, _inertia, _x_pos, _y_pos, _radius, friction=0.9, elasticity=0.3):
        body = pm.Body(_mass, _inertia, pm.Body.DYNAMIC)
        body.position = (_x_pos, _y_pos)
        shape = pm.Circle(body, _radius, (0, 0))
        shape.friction = friction
        shape.elasticity = elasticity
        self._space.add(body)
        self._space.add(shape)
        return body, shape

    def draw(self):
        # draw all rectangle shapes
        for shape_list in self._shapes_to_draw['rect']:
            shape = shape_list[0]
            w, h = shape_list[2], shape_list[3]
            # creating a surface object
            surface = pg.Surface((w, h), pg.SRCALPHA)
            surface.fill(shape_list[1])
            rot = -math.degrees(shape.body.angle)
            # rotate the surface
            rotated_surface = pg.transform.rotate(surface, rot)
            # get the rect of the surface
            rect = rotated_surface.get_rect(center=shape.body.position)
            if self._car.body.position[0] > 420:
                rect.x -= self._car.body.position[0] - 420
            self._screen.blit(rotated_surface, (rect.x, rect.y))
        # draw all circle shapes
        for shape_list in self._shapes_to_draw['circle']:
            shape = shape_list[0]
            x, y = shape.body.position
            if self._car.body.position[0] > 420:
                x -= self._car.body.position[0] - 420
            pg.draw.circle(self._screen, shape_list[1], center=(x, y), radius=shape.radius)
        # draw all segment(line) shapes
        for shape_list in self._shapes_to_draw['segment']:
            shape = shape_list[0]
            left = shape.a
            right = shape.b
            if self._car.body.position[0] > 420:
                offset = self._car.body.position[0] - 420
                left = (left[0]-offset, left[1])
                right = (right[0]-offset, right[1])
            pg.draw.line(self._screen, shape_list[1], left, right, int(shape.radius)*2)

    def update(self):
        for val in self._shapes_to_draw.keys():
            for num, shape_list in enumerate(self._shapes_to_draw[val]):
                shape = shape_list[0]
                if shape.body.position[1] > 720:
                    self._shapes_to_draw[val].pop(num)
                    self._space.remove(shape)


