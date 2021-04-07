import pymunk as pm
import pygame as pg
from Car import Car
from RoadBuilder import RoadBuilder
import constants


class Level:
    def __init__(self, space, screen):
        self._space = space
        self._screen = screen
        self._rb = RoadBuilder(self._space)
        self._c = Car(self._space, screen)
        self._shapes_to_draw = []

    def _create_road(self, vs):
        _road_body, segments = self._rb.build_road(vs, 5)
        return segments

    def draw(self):
        for shape in self._shapes_to_draw:
            pg.draw.circle(self._screen, (125, 125, 255), center=shape.body.position, radius=shape.radius)
