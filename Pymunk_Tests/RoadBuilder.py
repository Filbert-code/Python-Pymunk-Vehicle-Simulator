import pymunk as pm
from random import randrange
import math


class RoadBuilder:
    def __init__(self, space):
        self._space = space

    def build_road(self, vs, radius):
        """
        :param vs: Vertices that make up the roads
        :param radius: radius of the road Segments
        :return: The road Segment objects
        """
        # create the road Segments using the given vertices
        static_body = pm.Body(body_type=pm.Body.STATIC)
        static_segments = []
        for v in vs:
            seg = pm.Segment(static_body, v[0], v[1], radius)
            seg.elasticity = 0.50
            seg.friction = 0.90
            static_segments.append(seg)

        self._space.add(static_body)
        self._space.add(*static_segments)
        return static_segments

    def random_terrain_generator(self, vs, length, total_segments):
        """
        Randomly generates a road that builds towards the positive x-direction with
        each segment being a fixed length
        :param total_segments: total number of segments to be made
        :param length: length of the road Segment
        :param vs: Starting vertex
        :return: The Body of road Segments
        """
        # Example: vs = (0, 0)
        vertices = [vs]
        x_deltas = []
        y_deltas = []
        # starting from 1 to be able to append new vertices to the vertices list that already contains 1

        for seg_num in range(1, total_segments):
            delta_y = randrange(-length, length)
            delta_x = math.sqrt(length**2 - delta_y**2)
            # append a new vertex using the coordinates of the previous vertex
            prev_vertex = vertices[seg_num - 1]
            new_vertex = prev_vertex[0] + delta_x, prev_vertex[1] + delta_y
            vertices.append(new_vertex)



