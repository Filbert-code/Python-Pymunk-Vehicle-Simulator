import pygame as pg
import pymunk as pm

if __name__ == "__main__":
    image = pg.image.load("images/box_fort_img.png")
    vertices = [(-95, -16), (-110, -16), (-113, 26), (-95, 30)]
    bodies = [pm.Body(pm.Body.STATIC), pm.Body(pm.Body.STATIC)]
    d = {}
    d[image] = (vertices, bodies)

    for key in d.keys():
        print(d[key])
