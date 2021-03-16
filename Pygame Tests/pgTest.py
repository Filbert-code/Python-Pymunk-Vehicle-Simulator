import pygame as pg
import sys
from images.Hexagon import Hexagon
import constants
from random import randrange
from random import choice

pg.init()

speed = [2, 2]

screen = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))
clock = pg.time.Clock()
sprites = pg.sprite.Group()

# spawn 4 hexagons
for i in range(4):
    # random spawn location and speed
    sprites.add(Hexagon(randrange(50, 649), randrange(50, 449), choice([-4, 4]), choice([-4, 4])))



while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    sprites.update()

    # iteratoring through the sprites group
    sprite_group = pg.sprite.Group.sprites(sprites)
    sprite_group_len = len(sprite_group)
    for s1 in range(sprite_group_len):
        for s2 in range(s1, sprite_group_len):
            if pg.sprite.collide_mask(sprite_group[s1], sprite_group[s2]):
                sprite_group[s1].velocity[0] *= -1
                sprite_group[s1].velocity[1] *= -1
                sprite_group[s2].velocity[0] *= -1
                sprite_group[s2].velocity[1] *= -1


    screen.fill(constants.BACKGROUND_COLOR)
    sprites.draw(screen)

    # screen.blit(ball_surf, ball_rect)

    pg.display.flip()
    clock.tick(60)  # limiting frames per second to 60
