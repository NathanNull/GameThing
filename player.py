import pygame
import world
from block import all_blocks
import gamestates
from config import SCR_SIZE
from utils import add, mul

rand_sprite = 'sprites/0.png'

class Player(world.PhysicsObject):
    def __init__(self, x , y, scale):
        super().__init__(x, y, pygame.image.load(rand_sprite), [all_blocks])
        self.spawn = (x,y)
        self.flip = False
        self.blocks = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.grounded:
            self.push((0,-13))
        if keys[pygame.K_a]:
            self.push((-1,0))
            self.flip = True
        if keys[pygame.K_d]:
            self.push((1,0))
            self.flip = False

        # TODO: make this line work properly, it doesn't
        # right now and I'm too tired to figure out why
        world.screen_world_pos = add(self.rect.center, mul(SCR_SIZE, -0.5))

        if self.rect.y >= SCR_SIZE[1]*2:
            print("died")
            gamestates.kill(self)

        return super().update()

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip, False), self.screen_rect)