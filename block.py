import pygame
import world

GREEN = (62, 215, 62)

all_blocks = world.WorldGroup()

class Block(world.WorldObject):
    def __init__(self, x, y, scale):
        img = pygame.Surface([scale, scale])
        img.fill(GREEN)
        world.WorldObject.__init__(self, x, y, img)

        all_blocks.add(self)