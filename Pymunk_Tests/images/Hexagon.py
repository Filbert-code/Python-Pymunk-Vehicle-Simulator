import pygame as pg
import constants


class Hexagon(pg.sprite.Sprite):
    def __init__(self, x, y, velx, vely):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("../../Pygame Tests/hexagon.png")
        self.image = pg.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.centerx, self.rect.centery = (x, y)
        self.velocity = [velx, vely]

    def update(self):
        if self.rect.right >= constants.WIDTH or self.rect.left <= 0:
            self.velocity[0] *= -1
        if self.rect.bottom >= constants.HEIGHT or self.rect.top <= 0:
            self.velocity[1] *= -1
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
