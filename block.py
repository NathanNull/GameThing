import pygame
import random
import world
from config import SCR_SIZE

GREEN = (62, 215, 62)

all_blocks = world.WorldGroup()

class Block(world.WorldObject):
    def __init__(self, x, y, scale):
        img = pygame.Surface([scale, scale])
        img.fill(GREEN)
        world.WorldObject.__init__(self, x, y, img)

        self.tagged = False

        all_blocks.add(self)

    def update(self):
        if self.tagged:
            x = self.rect.x
            if x%2==0:
                self.rect.x += 1
            else:
                self.rect.x -= 1
        
        return super().update()

def generate(size):
    h_size = size//2
    y_pos = [p for p in range(SCR_SIZE[1]//2, SCR_SIZE[1]+size, size)]
    for x in range(-size, SCR_SIZE[0]+size, size):
        for i, y in enumerate(y_pos):
            if random.random() < (i+1)/len(y_pos):
                Block(x+h_size, y, size*0.9)