import pygame as pg
import sys

pg.init()

size = width, height = 800, 600
speed = [2, 2]
black = 0, 0, 0
BLUE = 0, 150, 0
BACKGROUND_COLOR = 155, 155, 155

screen = pg.display.set_mode(size)
clock = pg.time.Clock()
# ballrect = ball.get_rect()

ball_surf = pg.Surface((100, 100))
ball_rect = ball_surf.get_rect()

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    ball_rect = ball_rect.move(speed)
    if ball_rect.left < 0 or ball_rect.right > width:
        speed[0] = -speed[0]
    if ball_rect.top < 0 or ball_rect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(BACKGROUND_COLOR)

    screen.blit(ball_surf, ball_rect)

    pg.display.flip()
    clock.tick(60)  # limiting frames per second to 60
