# Python imports
import constants
import math

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
        self._screen = pg.display.set_mode((constants.WIDTH + 2600, constants.HEIGHT))
        self._clock = pg.time.Clock()

        # pymunk space
        self._space = pm.Space()
        self._space.gravity = (0, 981.0)
        # enables pymunk's debug draw mode for pygame
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        self._polys = []
        self._wheels = []
        self._car_bodies = []
        # bodies of road segments
        self._wall_bodies = []
        self._bullets = []
        self._static_segments = []

        self._car_images_original = [pg.image.load("mr_car.png"), pg.image.load("mr_car_wheel.png")]

        # SPAWN STUFF
        # self._add_bouncy_walls()
        self._create_car()
        self._create_road()

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
        # self._move_road()
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self._car_bodies[0].apply_force_at_world_point((5000, 12), (0, 0))

        if keys[pg.K_a]:
            self._car_bodies[0].apply_force_at_world_point((-5000, 12), (0, 0))

    def _draw(self):
        """
        draws pygame objects/shapes
        :return:
        """
        # self._draw_polys()
        # self._draw_barriers()
        # self._draw_wheels()
        # self._space.debug_draw(self._draw_options)
        self._draw_barriers()
        self._draw_car()

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
            # elif event.type == pg.KEYDOWN and event.key == pg.K_d:
            #     # radius = self._car_bodies[0].radius
            #     self._car_bodies[0].apply_force_at_world_point((5000, 12), (0, 0))
            # elif event.type == pg.KEYDOWN and event.key == pg.K_a:
            #     self._car_bodies[0].apply_force_at_world_point((-5000, 12), (0, 0))

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
        for line in self._static_segments:
            pg.draw.line(self._screen, (0, 0, 0), line.a, line.b, 10)

    def _draw_car(self):
        # get rotation of the car body
        rot = -math.degrees(self._car_bodies[2].angle)
        # image of the car body (mr car)
        image = pg.transform.rotate(self._car_images_original[0], rot)
        rect = image.get_rect(center=image.get_rect(center=self._car_bodies[2].position).center)
        # draw the car body onto the screen
        self._screen.blit(image, rect)

        rot = -math.degrees(self._car_bodies[0].angle)
        # load wheel image
        back_wheel_image = pg.transform.rotate(self._car_images_original[1], rot)
        rect = back_wheel_image.get_rect(center=image.get_rect(center=self._car_bodies[0].position).center)
        self._screen.blit(back_wheel_image, rect)
        rot = -math.degrees(self._car_bodies[1].angle)
        # load wheel image
        back_wheel_image = pg.transform.rotate(self._car_images_original[1], rot)
        rect = back_wheel_image.get_rect(center=image.get_rect(center=self._car_bodies[1].position).center)
        self._screen.blit(back_wheel_image, rect)


    def _draw_wheels(self):
        for wheel in self._wheels:
            pg.draw.circle(self._screen, pg.Color((255, 0, 0)), wheel.body.position, wheel.radius)

    def _draw_polys(self):
        for poly in self._polys:
            bb = poly.bb
            r = pg.Rect(bb.left, bb.top, bb.right-bb.left, bb.top-bb.bottom)
            pg.draw.rect(self._screen, pg.Color((255, 0, 0)), r)

    def _create_walls(self, *vertices, radius):
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
        self._space.add(static_body)
        self._space.add(*static_lines)
        for line in static_lines:
            self._wall_bodies.append(line)

        return static_lines

    def _create_poly(self, x_pos, y_pos, w, h):
        # create vertices
        vs = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        mass = 400.0
        radius = 2.0
        # calculate inertia
        inertia = pm.moment_for_poly(mass, vs, (0, 0), radius=radius)
        # polygon body
        body = pm.Body(mass, inertia)

        # connect the vertices to the body
        shape = pm.Poly(body, vs, radius=radius)
        # position to print onto screen
        body.position = x_pos, y_pos
        shape.elasticity = 0.3
        shape.friction = 0.9

        self._space.add(body, shape)
        self._polys.append(shape)
        return body, shape

    def _create_wheel(self, x_pos, y_pos, radius):
        """
                Create a wheel.
                :return: None
                """
        mass = 20
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia, pm.Body.DYNAMIC)
        body.position = x_pos, y_pos
        # body.apply_force_at_local_point((100000, 0), (0, 0))
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.3
        shape.friction = 0.9
        self._space.add(body, shape)
        self._wheels.append(shape)
        return body, shape

    def _create_road(self):
        vs = []
        for i in range(6):
            v = ((i*200, constants.HEIGHT), ((i+1)*200, constants.HEIGHT))
            vs.append(v)

        bumps_vs = [((600, 600), (800, 575)), ((1200, 600), (1300, 550)), ((2000, 600), (2300, 500))]
        for v in bumps_vs:
            vs.append(v)

        for i in range(17):
            v = ((i*200, constants.HEIGHT), ((i+1)*200, constants.HEIGHT))
            vs.append(v)

        static_body = pm.Body(body_type=pm.Body.STATIC)
        radius = 5
        static_segments = []
        for i, v in enumerate(vs):
            seg = pymunk.Segment(static_body, vs[i][0], vs[i][1], radius)
            seg.elasticity = 0.95
            seg.friction = 0.9
            static_segments.append(seg)

        self._space.add(static_body)
        self._space.add(*static_segments)
        for seg in static_segments:
            self._static_segments.append(seg)

    def _create_car(self):
        car_width, car_height = 120, 60
        starting_pos = (100, constants.HEIGHT/2 + 100)
        car_body, shape = self._create_poly(starting_pos[0], starting_pos[1], car_width, car_height)
        back_wheel, shape = self._create_wheel(starting_pos[0] - 60, starting_pos[1] + 60, 25)
        front_wheel, shape = self._create_wheel(starting_pos[0] + 60, starting_pos[1] + 60, 25)
        # attaching the car wheels to the car body using Constraints
        car_back_wheel_constraint = pm.constraints.PinJoint(car_body, back_wheel, (-20, 30), (0, 0))
        cb_support = pm.constraints.PinJoint(car_body, back_wheel, (-60, 30), (0, 0))
        car_front_wheel_constraint = pm.constraints.PinJoint(car_body, front_wheel, (20, 30), (0, 0))
        cf_support = pm.constraints.PinJoint(car_body, front_wheel, (60, 30), (0, 0))
        self._space.add(car_back_wheel_constraint)
        self._space.add(cb_support)
        self._space.add(car_front_wheel_constraint)
        self._space.add(cf_support)
        self._car_bodies = back_wheel, front_wheel, car_body


if __name__ == "__main__":
    sim = PhysicsSim()
    sim.run()









