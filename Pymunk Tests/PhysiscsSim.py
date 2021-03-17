# Python imports
import random
import constants

# Library imports
import pygame as pg

# pymunk imports
import pymunk as pm
import pymunk.pygame_util


class PhysicsSim:
    def __init__(self):
        # initialize pygame
        pg.init()
        # create a surface to draw on
        self._screen = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self._clock = pg.time.Clock()

        # pymunk space
        self._space = pm.Space()
        self._space.gravity = (0, 900.0)
        # enables pymunk's debug draw mode for pygame
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # Static lines, coords used to draw pygame lines
        self._static_barriers = []

        # Static barrier walls (lines) that prevent objects from leaving the scene
        self._add_static_scenery()

        self._polys = []
        self._wheels = []
        self._car_wheels = []

        # self._create_pinjoint()
        self._create_car()

        # Execution control
        self._running = True

    def run(self):
        while self._running:
            # Progress time forward
            self._process_time()
            self._process_events()
            self.update()
            self._clear_screen()
            self._draw()
            pg.display.flip()
            # Delay fixed time between frames
            self._clock.tick(50)
            pg.display.set_caption("fps: " + str(self._clock.get_fps()))

    def update(self):
        """
        Updates the states of all objects and the screen
        :return:
        """

    def _draw(self):
        """
        draws pygame objects/shapes
        :return:
        """
        # self._draw_polys()
        # self._draw_barriers()
        # self._draw_wheels()
        self._space.debug_draw(self._draw_options)

    def _process_time(self):
        """
        step forward in pymunk time
        :return:
        """
        for x in range(self._physics_steps_per_frame):
            self._space.step(self._dt)

    def _process_events(self):
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            # exit the window with the escape key
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self._running = False
            # process left-mouse click events
            elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed(3)[0]:
                m_pos = pg.mouse.get_pos()
                self._create_wheel(m_pos[0], m_pos[1])
            # process right-mouse click events
            elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed(3)[2]:
                m_pos = pg.mouse.get_pos()
                self._create_poly(m_pos[0], m_pos[1], 10, 10)
            elif event.type == pg.KEYDOWN and event.key == pg.K_d:
                self._car_wheels[0].apply_force_at_world_point((100000, 0), (0, 0))
            elif event.type == pg.KEYDOWN and event.key == pg.K_a:
                self._car_wheels[0].apply_force_at_world_point((-100000, 0), (0, 0))

        # rapid fire
        # if pg.mouse.get_pressed(3)[0]:
        #     m_pos = pg.mouse.get_pos()
        #     self._create_poly(m_pos[0], m_pos[1])

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pg.Color("white"))

    def _draw_barriers(self):
        for line in self._static_barriers:
            pg.draw.line(self._screen, (0, 0, 0), line["start"], line["end"], 1)

    def _draw_wheels(self):
        for wheel in self._wheels:
            pg.draw.circle(self._screen, pg.Color((255, 0, 0)), wheel.body.position, wheel.radius)

    def _draw_polys(self):
        for poly in self._polys:
            x = int(poly.body.position[0])
            y = int(poly.body.position[1])
            bb = poly.bb
            r = pg.Rect(bb.left, bb.top, bb.right-bb.left, bb.top-bb.bottom)
            pg.draw.rect(self._screen, pg.Color((255, 0, 0)), r)

    def _add_static_scenery(self):
        """
        Create the static bodies.
        :return: None
        """
        # dict for storing position and radius for pygame lines/barriers
        pg_lines = []
        line1, line2, line3, line4 = {"start": (0, 0), "end": (0, constants.HEIGHT), "radius": 10}, \
                                     {"start": (0, 0), "end": (constants.WIDTH, 0), "radius": 10}, \
                                     {"start": (0, constants.HEIGHT-4), "end": (constants.WIDTH, constants.HEIGHT-4), "radius": 10}, \
                                     {"start": (constants.WIDTH, 0), "end": (constants.WIDTH, constants.HEIGHT), "radius": 10}
        pg_lines.append(line1)
        pg_lines.append(line2)

        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, line1["start"], line1["end"], line1["radius"]),
            pymunk.Segment(static_body, line2["start"], line2["end"], line2["radius"]),
            pymunk.Segment(static_body, line3["start"], line3["end"], line3["radius"]),
            pymunk.Segment(static_body, line4["start"], line4["end"], line4["radius"]),
        ]
        for line in static_lines:
            line.elasticity = 0.5
            line.friction = 0.9
        self._space.add(*static_lines)
        for line in pg_lines:
            self._static_barriers.append(line)

    def _create_poly(self, x_pos, y_pos, w, h):
        # create vertices
        vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        mass = 50.0
        radius = 2.0
        # calculate inertia
        inertia = pm.moment_for_poly(mass, vs, (0, 0), radius=radius)
        # polygon body
        body = pm.Body(mass, inertia)

        # connect the vertices to the body
        shape = pm.Poly(body, vs, radius=radius)
        # position to print onto screen
        body.position = x_pos, y_pos
        shape.elasticity = 0.9
        shape.friction = 0.95

        self._space.add(body, shape)
        self._polys.append(shape)
        return body, shape

    def _create_wheel(self, x_pos, y_pos):
        """
                Create a wheel.
                :return: None
                """
        mass = 10
        radius = 50
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia, pm.Body.DYNAMIC)
        body.position = x_pos, y_pos
        # body.apply_force_at_local_point((100000, 0), (0, 0))
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.5
        shape.friction = 0.9
        self._space.add(body, shape)
        self._wheels.append(shape)
        return body, shape

    def _create_pinjoint(self):
        body1, shape1 = self._create_wheel(constants.WIDTH/2, constants.HEIGHT/2)
        body2, shape2 = self._create_wheel(constants.WIDTH/2+100, constants.HEIGHT/2+50)
        c = pm.constraints.PinJoint(body1, body2, (0, 0), (0, 0))
        self._space.add(c)

    def _create_car(self):
        car_width = 200
        car_height = 100
        car_body, shape = self._create_poly(constants.WIDTH/2, constants.HEIGHT/2, car_width, car_height)
        back_wheel, shape = self._create_wheel(constants.WIDTH/2 - 75, constants.HEIGHT/2 + 120)
        front_wheel, shape = self._create_wheel(constants.WIDTH/2 + 75, constants.HEIGHT/2 + 120)
        car_back_wheel_constraint = pm.constraints.PinJoint(car_body, back_wheel, (-60, 45), (0, 0))
        cb_support = pm.constraints.PinJoint(car_body, back_wheel, (-80, 45), (0, 0))
        car_front_wheel_constraint = pm.constraints.PinJoint(car_body, front_wheel, (60, 45), (0, 0))
        cf_support = pm.constraints.PinJoint(car_body, front_wheel, (80, 45), (0, 0))
        self._space.add(car_back_wheel_constraint)
        self._space.add(cb_support)
        self._space.add(car_front_wheel_constraint)
        self._space.add(cf_support)
        self._car_wheels = back_wheel, front_wheel


if __name__ == "__main__":
    sim = PhysicsSim()
    sim.run()









