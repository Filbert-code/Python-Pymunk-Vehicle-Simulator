

# Python imports
import random
import constants

# Library imports
import pygame as pg

# pymunk imports
import pymunk
import pymunk.pygame_util


class Simulation(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """

    def __init__(self) -> None:
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pg
        pg.init()
        self._screen = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self._clock = pg.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static lines, coords used to draw pygame lines
        self._static_barriers = []

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Balls that exist in the world
        self._balls = []

        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = 10

    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            self._process_events()
            self._update_balls()
            self._clear_screen()
            self._draw_objects()
            pg.display.flip()
            # Delay fixed time between frames
            self._clock.tick(50)
            pg.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        # dict for storing position and radius for pygame lines/barriers
        pg_lines = []
        line1, line2, line3, line4 = {"start": (-10, 0), "end": (-10, constants.HEIGHT), "radius": 10}, \
                                     {"start": (0, -10), "end": (constants.WIDTH, -10), "radius": 10}, \
                                     {"start": (0, constants.HEIGHT+10), "end": (constants.WIDTH, constants.HEIGHT+10), "radius": 10}, \
                                     {"start": (constants.WIDTH, -10), "end": (constants.WIDTH+10, constants.HEIGHT), "radius": 10}
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

    def _process_events(self) -> None:
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
            # save a screenshot with the p-key
            elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                pg.image.save(self._screen, "bouncing_balls.png")
            # process mouse click events
            elif event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed(3)[0]:
                m_pos = pg.mouse.get_pos()
                self._create_ball(m_pos[0], m_pos[1])

        if pg.mouse.get_pressed(3)[0]:
            m_pos = pg.mouse.get_pos()
            self._create_ball(m_pos[0], m_pos[1])

    def _update_balls(self) -> None:
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """

        # Remove balls that fall below 100 vertically
        # balls_to_remove = [ball for ball in self._balls if ball.body.position.y > 500]
        # for ball in balls_to_remove:
        #     self._space.remove(ball, ball.body)
        #     self._balls.remove(ball)

    def _create_ball(self, x_pos, y_pos) -> None:
        """
        Create a ball.
        :return: None
        """
        mass = 10
        radius = 5
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x_pos, y_pos
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self._space.add(body, shape)
        self._balls.append(shape)

    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pg.Color("white"))

    def _draw_barriers(self):
        for line in self._static_barriers:
            pg.draw.line(self._screen, (0, 0, 0), line["start"], line["end"], line["radius"]+10)

    def _draw_balls(self):
        for ball in self._balls:
            pg.draw.circle(self._screen, pg.Color((255, 0, 0)), ball.body.position, ball.radius)

    def _draw_objects(self) -> None:
        """
        Draw the objects.
        :return: None
        """
        # self._space.debug_draw(self._draw_options)
        self._draw_barriers()
        self._draw_balls()


if __name__ == "__main__":
    game = Simulation()
    game.run()
