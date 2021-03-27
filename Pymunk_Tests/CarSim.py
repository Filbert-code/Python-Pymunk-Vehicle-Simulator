# Python imports
import constants
import math
from RoadBuilder import RoadBuilder
from Car import Car
from Truck import Truck

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
        self._space.gravity = (0, 981.0)
        # enables pymunk's debug draw mode for pygame
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # mouse interactivity
        self._mouse_joint = None
        self._mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        # bodies of road segments
        self._static_segments = []

        self._car_images_original = [pg.image.load("mr_car.png"), pg.image.load("mr_car_wheel.png")]

        # SPAWN STUFF
        # self._create_car()
        truck = Truck(self._space, 300, 300)
        self._truck_wheels = truck.build()

        self._create_road()

        # Execution control
        self._running = True

    def run(self):
        """
        Game loop
        :return:
        """
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
            self._truck_wheels[0].apply_force_at_world_point((50000, 12), (0, 0))
            self._truck_wheels[1].apply_force_at_world_point((50000, 12), (0, 0))

        if keys[pg.K_a]:
            self._truck_wheels[0].apply_force_at_world_point((-50000, 12), (0, 0))
            self._truck_wheels[1].apply_force_at_world_point((-50000, 12), (0, 0))

    def _draw(self):
        """
        draws pygame objects/shapes
        :return:
        """
        self._space.debug_draw(self._draw_options)
        # self._draw_road()
        # self._draw_car()

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

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pg.Color("white"))

    def _draw_road(self):
        """
        Draw the road in pygame.
        :return:
        """
        for line in self._static_segments:
            car_centerx = self._truck_wheels[2].position[0]
            p1 = line.a
            p2 = line.b
            pg.draw.line(self._screen, (0, 0, 0), (p1[0] - car_centerx + 400, p1[1]), (p2[0] - car_centerx + 400, p2[1]), 10)

    def _draw_car(self):
        """
        Draws the car body and wheels onto the screen. Limit the x-pos of the car
        to half of the screen width.
        :return: None
        """
        # center coordinates of the car body in pm-space
        car_body_center = self._truck_wheels[2].position
        # get rotation of the car body or wheel
        car_body_rot = -math.degrees(self._truck_wheels[2].angle)
        # grab loaded image
        image = pg.transform.rotate(self._car_images_original[0], car_body_rot)
        car_body_rect = image.get_rect(center=image.get_rect(center=car_body_center).center)
        # shift the x-pos of the body by (x-cord of the car body) - 400
        if car_body_rect.centerx > 400:
            car_body_rect.centerx = 400
        # draw the car body onto the screen
        self._screen.blit(image, car_body_rect)
        # drawing front and back wheels
        for i in range(2):
            rot = -math.degrees(self._truck_wheels[i].angle)
            # grab loaded image
            image = pg.transform.rotate(self._car_images_original[1], rot)
            rect = image.get_rect(center=image.get_rect(center=self._truck_wheels[i].position).center)
            # shift the x-pos of the wheel by (x-cord of the car body) - 400
            if car_body_center[0] > 400:
                rect.centerx -= car_body_center[0] - 400
            # draw the car body onto the screen
            self._screen.blit(image, rect)

    def _create_poly(self, x_pos, y_pos, w, h):
        """
        Create a polygon. Used to make the body of the car.
        :param x_pos: x coordinate of the center of the body
        :param y_pos: y coordinate of the center of the body
        :param w: body width
        :param h: body height
        :return: Body and Shape objects
        """
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
        return body, shape

    def _create_road(self):
        """
        Create a road for the car using Pymunk Segments. Every Segment is static; meaning they can't move.
        :return: None
        """
        vs = []
        # vertices for bumps
        bumps_vs = [((600, 600), (900, 575)), ((1200, 600), (1300, 550)), ((2000, 600), (2300, 500))]
        for v in bumps_vs:
            vs.append(v)
        # vertices for a flat road throughout the whole level
        for i in range(17):
            v = ((i*200, constants.HEIGHT), ((i+1)*200, constants.HEIGHT))
            vs.append(v)
        # use RoadBuilder class to build a road and return the Segments of that road
        rb = RoadBuilder(self._space)

        # TESTS
        vertices = rb.random_terrain_vertices_generator((0, constants.HEIGHT), 100, 80)
        static_segs = rb.build_road(vertices, 5)
        for seg in static_segs:
            self._static_segments.append(seg)

        # static_segs = rb.build_road(vs, 5)
        # for seg in static_segs:
        #     self._static_segments.append(seg)

    def _create_car(self):
        """
        Create the car's body and wheels. All Bodies are added to the space.
        PinJoint Constraints are made to attached the wheels to the car; they are added to the space as well.
        :return:
        """
        car_width, car_height = 120, 60
        starting_pos = (100, constants.HEIGHT / 2 + 100)
        # starting_pos = (constants.WIDTH/2+300, constants.HEIGHT/2 + 100)
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









