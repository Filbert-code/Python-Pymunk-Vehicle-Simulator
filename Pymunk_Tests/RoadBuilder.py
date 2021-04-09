import pymunk as pm
from random import randrange
import math
import constants


class RoadBuilder:
    def __init__(self, space):
        self._space = space

    def build_road(self, vs, radius, color=(0, 0, 0, 0)):
        """
        :param color: color of the road
        :param vs: Vertices that make up the roads
        :param radius: radius of the road Segments
        :return: The road Segment objects
        """
        # create the road Segments using the given vertices
        static_body = pm.Body(body_type=pm.Body.STATIC)
        static_segments = []
        for v in vs:
            seg = pm.Segment(static_body, v[0], v[1], radius)
            seg.elasticity = 0.10
            seg.friction = 0.90
            seg.color = color
            seg.filter = pm.ShapeFilter(categories=3)
            static_segments.append(seg)

        self._space.add(static_body)
        self._space.add(*static_segments)
        return static_body, static_segments

    def random_terrain_vertices_generator(self, vs, length, total_segments):
        """
        Randomly generates a road that builds towards the positive x-direction with
        each segment being a fixed length
        :param total_segments: total number of segments to be made
        :param length: length of the road Segment
        :param vs: Starting vertex
        :return: The vertices of the random terrain
        """
        vertices = [vs]
        # starting from 1 to be able to append new vertices to the vertices list that already contains 1
        for seg_num in range(1, total_segments*2):
            # most steep : 1, very flat: > 2
            steepness = 3
            # x-value has to be the same every other point to make the segments connect
            if seg_num % 2 == 1:
                delta_y = randrange(int(-length/steepness), int(length/steepness))
                delta_x = math.sqrt(length ** 2 - delta_y ** 2)
            else:
                delta_x = 0
                delta_y = 0
            # append a new vertex using the coordinates of the previous vertex
            prev_vertex = vertices[seg_num - 1]
            # make sure the delta_y value never create a point below the screen
            if prev_vertex[1] + int(delta_y) > constants.HEIGHT:
                delta_y = constants.HEIGHT - prev_vertex[1]
            # create the new vertex
            new_vertex = prev_vertex[0] + int(delta_x), prev_vertex[1] + int(delta_y)
            vertices.append(new_vertex)
        # put the vertices into pairs
        vertex_pairs = []
        for i in range(0, total_segments*2, 2):
            vertex_pairs.append((vertices[i], vertices[i+1]))
        return vertex_pairs




