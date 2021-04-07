# Python imports
import constants
import math
from RoadBuilder import RoadBuilder
from ObstacleCourse import ObstacleCourse
from Tank_Level import Tank_Level
from Truck import Truck
from Sportscar import Sportscar
from Tank import Tank
from Menu import Menu
from Level import Level

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
        self._screen = pg.display.set_mode((constants.WIDTH+640, constants.HEIGHT+360))
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
        self._dt = 1.0 / 120.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 2

        # mouse interactivity
        self._mouse_joint = None
        self._mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        # bodies of road segments
        self._static_segments = []
        # {pygame_surface/image: ([vertices], [bodies]) --> can have multiple bodies with the same image
        # but number of bodies must match vertices
        self._polys = {}

        # SPAWN STUFF
        # self._car = Truck(self._space, self._screen, 200, 550)
        # self._car = Sportscar(self._space, self._screen, 200, 550)
        self._car = Tank(self._space, self._screen, constants.WIDTH/2-200, constants.HEIGHT-50)
        self._car.build()
        self._active_car = 0  # index of active car: sportscar=0, truck=1

        # declare obstacle course
        # self._obc = None
        # self._create_obstacle_course()
        # self._active_level = 0  # index of active level: obstacle course=0, mountain=1
        self._level = None
        self._create_tank_obstacle_course()

        # menu
        self._btn_clicked = None  # array to keep track of which arrow button is pressed
        self._menu = Menu(self._screen)

        # Execution control
        self._running, self._pause, self._exit, self._menu_state = 1, 2, 3, 4
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
            # menu state
            elif self._state == self._menu_state:
                self._process_events()
                self._clear_screen()
                self._draw()
                self._menu.draw_menu(self._btn_clicked)
                pg.display.flip()
                # Delay fixed time between frames
                self._clock.tick(50)
                pg.display.set_caption("fps: " + str(self._clock.get_fps()))
            # paused state
            elif self._state == self._pause:
                self._process_events()
                self._screen.blit(pause_text, (constants.WIDTH / 2 - 32, constants.HEIGHT / 2 - 16))
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
        # self._car.update()
        pass

    def _draw(self):
        """
        draws pygame objects/shapes
        :return:
        """
        self._space.debug_draw(self._draw_options)
        self._draw_road()
        # self._draw_polys()
        self._car.draw()
        self._level.draw()

    def _process_time(self):
        """
        step forward in pymunk time
        :return:
        """
        for x in range(self._physics_steps_per_frame):
            self._car.update()
            self._space.step(self._dt)

    def _process_events(self):
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._state = self._exit
            # game state event handler
            if self._state == self._running or self._state == self._pause:
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self._state == self._running:
                    self._state = self._pause
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self._state == self._pause:
                    self._state = self._running
                elif event.type == pg.KEYDOWN and event.key == pg.K_m:
                    self._state = self._menu_state
                elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                    self._space.remove(self._obc.spring_trap_pin)
                # check if a Tank has been instantiated and fire a shot
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if isinstance(Tank, type):
                        self._car.shoot_projectile()
            # menu event handler
            elif self._state == self._menu_state:
                if event.type == pg.KEYDOWN and event.key == pg.K_m:
                    self._state = self._running
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self._menu_button_event()
                elif event.type == pg.MOUSEBUTTONUP:
                    self._menu.selection_updated = 0
                    self._btn_clicked = None

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pg.Color("turquoise"))

    def _menu_button_event(self):
        self._menu.mouse_button_down = 1
        x, y = pg.mouse.get_pos()
        # top_left, top_right, bot_left, bot_right
        button_positions = self._menu.btn_positions
        # using two hit-boxes to check if an arrow button was clicked
        for btn_num, button in enumerate(button_positions):
            centerx, centery = button
            # checking if user pressed the Apply or Reset buttons
            # reset button
            if btn_num == 4:
                if centerx - 50 <= x <= centerx + 50 and centery - 50 <= y <= centery + 50:
                    self._btn_clicked = [1 if i == btn_num else 0 for i in range(6)]
                    self._reset_button_pressed()
                    break
            # apply button
            elif btn_num == 5:
                if centerx - 50 <= x <= centerx + 50 and centery - 50 <= y <= centery + 50:
                    self._btn_clicked = [1 if i == btn_num else 0 for i in range(6)]
                    self._apply_button_pressed()
                    break
            # checking if arrow buttons are pressed
            if centerx - 16 <= x <= centerx + 10 and centery - 15 <= y <= centery + 15 or \
                    centerx + 10 <= x <= centerx + 19 and centery - 18 <= y <= centery + 18:
                # an array of zeros and a one, the one integer indicates which button is pressed
                self._btn_clicked = [1 if i == btn_num else 0 for i in range(6)]
                break

    def _reset_button_pressed(self):
        """
        Delete all objects in Space and create new instances of the current car and current
        level. This is triggered when the user presses the reset button in the menu.
        :return:
        """
        self._static_segments = []
        self._polys = {}
        self._space = pm.Space()
        self._space.gravity = (0, 981.0)
        if self._menu.current_car == 0:
            self._car = Sportscar(self._space, self._space, 200, 550)
            self._active_car = 0
        else:
            self._car = Truck(self._space, self._screen, 200, 550)
            self._active_car = 1
        self._car.build()
        if self._menu.current_level == 0:
            self._create_obstacle_course()
            self._active_level = 0
        else:
            self._create_random_generated_road()
            self._active_level = 1

    def _apply_button_pressed(self):
        """
        Delete all objects in Space and create new instances of the selected car and selected
        level. This is triggered when the user presses the apply button in the menu.
        :return:
        """
        self._static_segments = []
        self._polys = {}
        self._space = pm.Space()
        self._space.gravity = (0, 981.0)
        if self._active_car == 0:
            self._car = Sportscar(self._space, self._screen, 200, 550)
        else:
            self._car = Truck(self._space, self._screen, 200, 550)
        self._car.build()
        if self._active_level == 0:
            self._create_obstacle_course()
        else:
            self._create_random_generated_road()

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

    def _draw_polys(self):
        """
        Blitting the dynamic objects of levels
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
        self._level = ObstacleCourse(self._space, self._screen, self._polys)
        static_segs = self._obc.build()
        self._create_road(static_segs)

    def _create_tank_obstacle_course(self):
        """
                Create an obstacle course for the tank
                :return:
                """
        self._level = Tank_Level(self._space, self._screen, self._car)
        static_segs = self._level.build()
        self._create_road(static_segs)

if __name__ == "__main__":
    sim = PhysicsSim()
    sim.run()
