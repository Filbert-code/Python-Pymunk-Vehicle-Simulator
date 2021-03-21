import constants
import pygame as pg
from PhysiscsSim import PhysicsSim

# pymunk imports
import pymunk as pm
import pymunk.pygame_util


def _create_walls(space, wall_bodies, *vertices, radius):
    """
    Creates walls using static Segments
    :param vertices: a comp. list of vertices
    :param radius: the radius of the walls
    :return: a list of pymunk Segment objects corresponding to the walls
    """
    static_body = pm.Body(body_type=pm.Body.STATIC)
    static_lines = []
    for v in vertices:
        static_lines.append(pymunk.Segment(static_body, v[0], v[1], radius))

    for line in static_lines:
        line.elasticity = 0.95
        line.friction = 0.9
    space.add(static_body)
    space.add(*static_lines)
    for line in static_lines:
        wall_bodies.append(line)

    return static_lines


class DrawTool:
    def __init__(self):
        pass

