import pygame
import random
from world import WorldGroup, WorldObject
from config import SCR_SIZE

GREEN = (62, 215, 62)


class Block(WorldObject):
    def __init__(self, x, y, scale):
        img = pygame.Surface([scale, scale])
        img.fill(GREEN)
        super().__init__(x, y, img)

        self.max_break_time = 30
        self.break_time = 30

    def update(self):
        #Get mouse position
        pos = pygame.mouse.get_pos()

        #Check if the mouse is over the button and respond
        if self.screen_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        if self.clicked:
            self.break_time -= 1
            if self.break_time <= 0:
                self.kill()
                return self._last_scr_pos
        else:
            self.break_time = self.max_break_time
        return super().update()

class BlockGroup(WorldGroup):
    def __init__(self, range=pygame.Rect((0,0),SCR_SIZE), size=45, gen=True):
        super().__init__()
        self.range = range
        self.size = 45
        self.blocks = []
        if gen:
            self.generate(self)

    def add_at(self, x, y, block):
        self.add(block)
        self.blocks[int(x)][int(y)] = block
        block.center = (self.range.left+(x*self.size),self.range.top+(y*self.size))
    def generate(self, size=45):
        h_size = 45/2
        self.size = 45
        y_pos = [p for p in range((SCR_SIZE[1]//2), (SCR_SIZE[1]+self.size), self.size)]
        for x in range(-self.size, SCR_SIZE[0]+self.size, self.size):
            for i, y in enumerate(y_pos):
                if random.random() < (i+1)/len(y_pos):
                    self.add_at(block=Block(x=x+h_size, y=y, scale=self.size*0.9),x=x+h_size, y=y)

all_blocks = BlockGroup()
