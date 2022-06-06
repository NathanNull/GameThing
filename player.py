import pygame
import world
from block import all_blocks

rand_sprite = 'sprites/0.png'

class Player(world.PhysicsObject):
    def __init__(self, x , y, scale):
        super().__init__(x, y, pygame.image.load(rand_sprite), [all_blocks])

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.grounded:
            self.push((0,-10))
        if keys[pygame.K_a]:
            self.push((-1,0))
        if keys[pygame.K_d]:
            self.push((1,0))

        # TODO: make this line work properly, it doesn't
        # right now and I'm too tired to figure out why
        #world.screen_world_pos = self.rect.center

        return super().update()

    def draw(self, surface):
        surface.blit(self.image, self.screen_rect)
        pygame.draw.rect(surface, (255,0,0), self.screen_rect, 5)