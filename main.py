import pygame as pg
from game_utils import *

pg.init()  # initialising pygame
pg.mixer.init()

game = Game()
game.run()
