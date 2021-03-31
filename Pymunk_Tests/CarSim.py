# Python imports
import constants
import math
from RoadBuilder import RoadBuilder
from ObstacleCourse import ObstacleCourse
from Car import Car
from Truck import Truck
from Sportscar import Sportscar

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
        # only draws shapes, no constraints or joints
        # self._draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES

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
        self._dyn_polys = []
        # {pygame_surface/image: ([vertices], [bodies]) --> can have multiple bodies with the same image
        # but number of bodies must match vertices
        self._polys = {}

        wheel_image = pg.image.load("mr_car_wheel.png")
        self._car_images_original = [pg.image.load("mr_car.png"), pg.transform.scale(wheel_image, (42, 42))]

        # SPAWN STUFF
        # self._car = Truck(self._space, 200, 300)
        # self._car.build()
        self._car = Sportscar(self._space, 200, 350)
        self._car.build()

        # declare obstacle course
        self._obc = None
        self._create_obstacle_course()

        # self._create_random_generated_road()

        # Execution control
        self._running, self._pause, self._exit = 1, 0, -1
        self._state = self._running

    def run(self):
        """
        Game loop
        :return:
        """
        pause_text = pg.font.SysFont('Consolas', 32).render('Pause', True, pg.color.Color('White'))
        while True:
            # game running state
            if self._state == self._running:
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
            # paused state
            elif self._state == self._pause:
                self._process_events()
                self._screen.blit(pause_text, (constants.WIDTH/2, constants.HEIGHT/2))
                pg.display.flip()
                self._clock.tick(50)
                pg.display.set_caption("fps: " + str(self._clock.get_fps()))
            # exiting state
            elif self._state == self._exit:
                break

    def update(self):
        """
        Updates the states of all objects and the screen
        :return:
        """
        keys = pg.key.get_pressed()
        # going forward
        if keys[pg.K_d]:
            # limiting velocity to 500
            if self._car.wheels[0].velocity.int_tuple[0] < self._car.max_speed:
                self._car.wheels[0].apply_force_at_world_point((self._car.wheel_turn_force, 12), (0, 0))
            # all wheel drive
            if self._car.all_wheel_drive:
                if self._car.wheels[1].velocity.int_tuple[0] < self._car.max_speed:
                    self._car.wheels[1].apply_force_at_world_point((self._car.wheel_turn_force, 12), (0, 0))
        # going backward
        if keys[pg.K_a]:
            if self._car.wheels[0].velocity.int_tuple[0] > -self._car.max_speed:
                self._car.wheels[0].apply_force_at_world_point((-self._car.wheel_turn_force, 12), (0, 0))
            if self._car.all_wheel_drive:
                if self._car.wheels[1].velocity.int_tuple[0] > -self._car.max_speed:
                    self._car.wheels[1].apply_force_at_world_point((-self._car.wheel_turn_force, 12), (0, 0))

    def _draw(self):
        """
        draws pygame objects/shapes
        :return:
        """
        self._space.debug_draw(self._draw_options)
        # self._draw_road()
        # self._draw_polys()
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
                self._state = self._exit
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self._state:
                self._state = self._pause
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self._state:
                self._state = self._running
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                self._space.remove(self._obc.spring_trap_pin)

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pg.Color("turquoise"))

    def _draw_road(self):
        """
        Draw the road in pygame.
        :return:
        """
        for line in self._static_segments:
            car_centerx = self._car.body.position[0]
            p1 = line.a
            p2 = line.b
            # shift the road the opposite direction of the player's movement to simulate the car is moving
            if car_centerx >= 400:
                x_pos = (p1[0] - car_centerx + 400, p1[1])
                y_pos = (p2[0] - car_centerx + 400, p2[1])
                pg.draw.line(self._screen, (0, 0, 0), x_pos, y_pos, 10)
            else:
                x_pos, y_pos = (p1[0], p1[1]), (p2[0], p2[1])
                pg.draw.line(self._screen, (0, 0, 0), x_pos, y_pos, 10)

    def _draw_car(self):
        """
        Draws the car body and wheels onto the screen. Limit the x-pos of the car
        to half of the screen width.
        :return: None
        """
        # center coordinates of the car body in pm-space
        car_body_center = self._car.body.position
        # get rotation of the car body or wheel
        car_body_rot = -math.degrees(self._car.body.angle)
        # grab loaded image
        image = pg.transform.rotate(self._car.image, car_body_rot)
        car_body_rect = image.get_rect(center=image.get_rect(center=car_body_center).center)
        # car_body_rect.centerx -= offset
        # car_body_rect.centery -= offset
        # shift the x-pos of the body by (x-cord of the car body) - 400
        if car_body_rect.centerx > 400:
            car_body_rect.centerx = 400

        # draw the car body onto the screen
        self._screen.blit(image, car_body_rect)
        # drawing front and back wheels
        for i in range(2):
            rot = -math.degrees(self._car.wheels[i].angle)
            # grab loaded image
            image = pg.transform.rotate(self._car_images_original[1], rot)
            rect = image.get_rect(center=image.get_rect(center=self._car.wheels[i].position).center)
            # shift the x-pos of the wheel by (x-cord of the car body) - 400
            if car_body_center[0] > 400:
                rect.centerx -= car_body_center[0] - 400
            # draw the car body onto the screen
            self._screen.blit(image, rect)

    def _draw_polys(self):
        """
        Blitting the dynamic objects of levels
        :param bodies: pymunk bodies
        :return: None
        """
        car_centerx = self._car.body.position[0]
        # self._polys --> {pygame_surface / image: ([vertices], [bodies])
        for surface in self._polys.keys():
            for body in self._polys[surface]:
                # get rotation of the car body or wheel
                body_rot = -math.degrees(body.angle)
                image = pg.transform.rotate(surface, body_rot)
                # shift the blit of the poly relative to the player's movement
                if car_centerx >= 400:
                    center = (body.position[0] - car_centerx + 400, body.position[1])
                    rect = image.get_rect(center=center)
                    self._screen.blit(image, rect)
                else:
                    center = (body.position[0], body.position[1])
                    rect = image.get_rect(center=center)
                    self._screen.blit(image, rect)

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

    def _create_road(self, static_segs):
        """
        Create a road for the car using Pymunk Segments. Every Segment is static; meaning they can't move.
        :return: None
        """
        # use RoadBuilder class to build a road and return the Segments of that road
        for seg in static_segs:
            self._static_segments.append(seg)

    def _create_random_generated_road(self):
        """
        Create a randomly generated road from the random_terrian... class
        :return:
        """
        rb = RoadBuilder(self._space)
        vertices = rb.random_terrain_vertices_generator((0, constants.HEIGHT), 100, 80)
        body, static_segs = rb.build_road(vertices, 5)
        self._create_road(static_segs)

    def _create_obstacle_course(self):
        """
        Create an obstacle course road and features
        :return:
        """
        self._obc = ObstacleCourse(self._space, self._polys)
        static_segs = self._obc.build()
        self._create_road(static_segs)


if __name__ == "__main__":
    sim = PhysicsSim()
    sim.run()









