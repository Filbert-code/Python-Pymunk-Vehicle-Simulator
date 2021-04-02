import pygame as pg
import pymunk as pm

if __name__ == "__main__":
    btn = 3
    arr = [1, 0, 0, 0, 0, 0]
    num = arr.index(1)
    arr = [1 if i == num-1 else 0 for i in range(6)]
    if arr.count(1) == 0:
        arr = [0, 0, 0, 0, 0, 1]
    print(arr)
